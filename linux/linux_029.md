# 中断(IRQ)、软中断和信号

### 中断、异常和信号

广义上的中断信号(interrupt signal)是指一个可以改变处理器原本指令执行顺序的事件。分为同步和异步中断，Intel把同步中断称为中断(interrupt)，异步中断称为异常(exception)。

**中断**(interrupt)是与硬件相关的，可以由定时器、I/O设备或者处理期间中断(inter-processor interrupt, IPI)产生。

**异常**(exception)一般是用户程序的错误产生的，当一个异常发生时，内核向引起一次样的进程发送一个**信号**(signal)，然后被注册的或者默认的信号处理程序会处理这个信号。

有一种例外的异常是缺页(page fault)，缺页异常是由内核处理的，内核是利用了这种异常更有效的管理硬件资源。"Device not available"也用于将新值装入浮点寄存器。[4]


### 内核在处理中断信号中所扮演的角色

**中断** 会“强行”代替正在运行的进程在内核态执行中断处理程序，注意：中断处理程序运行期间：

* 不能被切换的(**永不阻塞**)
* 不能被自己打断(**不可重入**)
* 但可以被其他中断处理程序打断(**可以嵌套**，如下图)

[[linux_029_001.png]]

由于**中断**是非阻塞且不可能重入的，因此一般要求中断处理是极快的，只有紧急的处理会被实时执行。那么可以延迟的非紧急处理过程，通常以**bottom half(也叫底半、可延迟函数、软中断？)**的形式交给**soft_irq(软中断)、tasklet、workqueue、interrupt thread**等执行。

**异常** 与用户进程更相关，因为若内核没有BUG，多数异常可以由Linux内核解释并发某些信号给进程，信号处理程序就是由这个用户进程运行的，因此异常(信号)处理程序可以被调度(切换)。注意：page fault异常时例外，它产生自内核，所以page fault处理程序在内核中，但它不会进一步引起其他的异常。


### 硬中断/软中断、顶半/底半

中断分为一般的**硬件中断**，内核中处于性能模拟硬件中断的**软中断**，还有模拟中断机制用于进程通信的**信号**(signal)。[3] 上边一节所说的“中断”即可以理解为硬中断，“可延迟函数”、“底半”等可以理解为软中断。

(硬)中断时，其他的进程会被暂停，因此，内核中实现了软中断来缓解这个问题，让进程只暂停极短事件。tasklet和workqueue基于soft_irq软中断实现，是驱动中较常用的延迟执行硬件中断逻辑的方法。在(硬)中断处理程序中同步阻塞执行的称为顶半（top half），以软中断形式异步延迟执行的称为底半(bottom half)。注意：

* **soft_irq软中断**时可以多个CPU并发执行的

* 同一种**tasklet**只可以串行执行，因此不必写成可重入函数，方便了驱动开发。

* soft_irq和tasklet可以被称为可延迟函数[4]，类似于(硬)中断，它们都是不能重入、可以被其他中断嵌套、并且不能被抢占调度的，所以编程时会比较简单，不用考虑一些数据同步和保护问题。

* **workqueue工作队列** 运行于进程上下文，而非上两种可延迟函数一样运行于中断上下文。区别是，进程上下文是可以切换的，而中断上下文不可切换。不过，由于他们都运行与内核态，无论是可延迟函数(soft_irq和tasklet)或是workqueue都不能访问用户态地址空间。

* 2.6.29后，threaded interrupt handlers被merge到主线，它支持tasklet所不支持sleep。[1]


(以下摘自[1]:)

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


---

[1] https://blog.csdn.net/batoom/article/details/8645021

[2] Moving interrupts to threads, https://lwn.net/Articles/302043/

[3] 信号和中断的比较 + 中断和异常的比较, https://www.cnblogs.com/charlesblc/p/6277810.html

[4] UTLK Chap. 4
