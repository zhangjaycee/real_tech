# 中断(IRQ)、软中断和信号

中断分为一般的**硬件中断**，内核中处于性能模拟硬件中断的**软中断**，还有模拟中断机制用于进程通信的**信号**(signal)。[3]

### 硬中断和软中断

硬件中断时，其他的进程会被暂停，因此，内核中实现了软中断来解决这个问题，tasklet和workqueue基于软中断实现，是驱动中较常用的延迟执行硬件中断逻辑的方法。2.6.29后，threaded interrupt handlers被merge到主线。tasklet不支持sleep。

摘自[1]:

>
> 在linux里，中断处理分为顶半（top half），底半(bottomhalf)，在顶半里处理优先级比较高的事情，要求占用中断时间尽量的短，在处理完成后，就激活底半，有底半处理其余任务。底半的处理方式主要有soft_irq,tasklet,workqueue三种，他们在使用方式和适用情况上各有不同。soft_irq用在对底半执行时间要求比较紧急或者非常重要的场合，主要为一些subsystem用，一般driver基本上用不上。tasklet和work queue在普通的driver里用的相对较多，主要区别是tasklet是在中断上下文执行,而workqueue是在process上下文，因此可以执行可能sleep的操作。
> 
> 2.6.30里，在ingo molnar的RT tree里存在有一段时间的interruptthread终于merge到mainline了。此时如果使用request_threaded_irq申请的中断，handler不是在中断上下文里执行，而是在新创建的线程里执行，这样，该handler非常像执行workqueue，拥有所有workqueue的特性，但是省掉了创建,初始化，调度workqueue的繁多步骤。处理起来非常简单。
> ```cpp
> int request_threaded_irq(unsigned int irq, irq_handler_t handler, irq_handler_t thread_fn, unsigned long irqflags, const char *devname, void *dev_id)
> ```
> 
> 和request_irq非常类似，irq是中断号， handler是在发生中断时，首先要执行的code，非常类似于顶半，该函数最后会return IRQ_WAKE_THREAD来唤醒中断线程，一般设为NULL，用系统提供的默认处理。thread_fn，是要在线程里执行的handler，非常类似于底半。 后三个参数基本和request_irq相同。irqsflags新增加了一个标志，IRQF_ONESHOT，用来标明是在中断线程执行完后在打开该中断，该标志非常有用，否则中断有可能一直在顶半执行，而不能处理中断线程。例如对于gpio level中断，如果不设置该位，在顶半执行完成后，会打开中断，此时由于电平没有变化，马上有执行中断，永远没有机会处理线程。
> 
> 下边一个实际例子来说明它的应用。在手机平台中，检测耳机的插入一般是通过耳机插孔中机械变化导致一个baseband gpio的电平的变化，在该gpio中断里进行耳机插入处理。但是耳机插入一般都有个抖动的过程，需要消抖处理。最简单的办法是在中断发生后，延时一段时间（例如200ms），然后再检查GPIO状态是否稳定来确定是否有效插入。如果用老的中断方式，不得不用workqueue的方式，你需要在顶半里激活一个delay 200ms的workqueue，然后在workqueue里检查。用线程化的处理方式，你仅仅需要在thread_fn里sleep 200ms，然后在检查即可。看，事情就这么简单！

### 信号


[1] https://blog.csdn.net/batoom/article/details/8645021

[2] Moving interrupts to threads, https://lwn.net/Articles/302043/

[3] 信号和中断的比较 + 中断和异常的比较, https://www.cnblogs.com/charlesblc/p/6277810.html