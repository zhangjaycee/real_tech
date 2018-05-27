# IRQ 中断

摘自[1]:

>
> 在linux里，中断处理分为顶半（top half），底半(bottomhalf)，在顶半里处理优先级比较高的事情，要求占用中断时间尽量的短，在处理完成后，就激活底半，有底半处理其余任务。底半的处理方式主要有soft_irq,tasklet,workqueue三种，他们在使用方式和适用情况上各有不同。soft_irq用在对底半执行时间要求比较紧急或者非常重要的场合，主要为一些subsystem用，一般driver基本上用不上。tasklet和work queue在普通的driver里用的相对较多，主要区别是tasklet是在中断上下文执行,而workqueue是在process上下文，因此可以执行可能sleep的操作。
> 2.6.30里，在ingo molnar的RT tree里存在有一段时间的interruptthread终于merge到mainline了。此时如果使用request_threaded_irq申请的中断，handler不是在中断上下文里执行，而是在新创建的线程里执行，这样，该handler非常像执行workqueue，拥有所有workqueue的特性，但是省掉了创建,初始化，调度workqueue的繁多步骤。处理起来非常简单。


[1] https://blog.csdn.net/batoom/article/details/8645021