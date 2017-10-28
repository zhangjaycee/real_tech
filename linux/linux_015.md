# Linux Block Layer中的I/O队列和调度器


## I/O Scheduler

#### 调度算法



* CFQ(complete fairness queue): 多个请求队列，用hash将一个进程号的请求发到一个请求队列（因此，一个进程常发到一个队列）。

* deadline: 有4个请求队列。其中有一对分别是读写请求队列；另一对是按最后期限排列的读写请求队列。

注意：这里读请求的超时时间(比如500ms)一般比写请求的超时时间长(比如5s)，这是由于读一般都是阻塞调用的。

* Anticipatory("预期", 默认算法[2]): 类似deadline，但加入了一些启发式准则。

* noop(no operation): 简单的FIFO，直接插入到调度队列的末尾。

[1] Using the Deadline IO Scheduler, https://access.redhat.com/solutions/32376

[2] UTLK

## blk-mq 相关(multi-queue)

[Linux Multi-Queue Block IO Queueing Mechanism (blk-mq)]
https://www.thomas-krenn.com/en/wiki/Linux_Multi-Queue_Block_IO_Queueing_Mechanism_(blk-mq)

[kernel 3.10内核源码分析--块设备层request plug/unplug机制]
 http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=14528823&id=4778396

