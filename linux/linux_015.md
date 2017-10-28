# Linux Block Layer中的I/O队列和调度器


## I/O Scheduler

#### 调度算法

* Anticipatory("预期", 默认算法):

* CFQ: 多个请求队列，用hash将一个进程号的请求发到一个请求队列（因此，一个进程常发到一个队列）。

* deadline:

## blk-mq 相关(multi-queue)

[Linux Multi-Queue Block IO Queueing Mechanism (blk-mq)]
https://www.thomas-krenn.com/en/wiki/Linux_Multi-Queue_Block_IO_Queueing_Mechanism_(blk-mq)

[kernel 3.10内核源码分析--块设备层request plug/unplug机制]
 http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=14528823&id=4778396

