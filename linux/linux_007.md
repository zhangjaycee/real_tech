# Linux I/O 模型

## 理解同步/异步和阻塞/非阻塞？

（以下为目前的理解方式）

#### 同步/异步

**同步**的一般含义是两个及以上的事件同时在执行。比如在通信中，同步通信指的是信号按照时钟的频率传输信号，这里的同步指的是发送和接收端的时钟频率调成了同步状态。

那么，在I/O模型中，**同步** 指的应该是数据传输时，发起请求的当前线程与数据传输之间的状态是同步的，当"I/O请求线程"调用请求函数后会阻塞在请求函数上，直到请求最终完成才会返回。换句话说，数据在被传输时，当前线程也的确实是在进行数据传输这件事而没有去干别的。

对应的，**异步** 指的是当前线程与数据传输之间的异步，线程进行完IO请求后，函数立即返回，所有其它工作并不是由当前线程完成的，而是由内核或者其他线程完成后通知当前进程的。

#### 阻塞/非阻塞 (网络I/O)

**阻塞**的含义是“堵”或者“等”，就比如我把一件事交给你办，你办不出来我不让你走。

阻塞/非阻塞IO一般用在网络编程中，而不存在磁盘I/O中[2]。阻塞和非阻塞是对同步IO的一种细分(同级别的分类还包括信号驱动I/O和I/O多路复用)，指的是数据并未准备好时，是阻塞等待不返回还是立即返回错误信号。

IO设备没有准备好所请求的信息时，IO请求的调用是否返回。若不返回一直等下去，则是 **阻塞的**；若马上返回一个错误值表示现在还没准备好，控制权又交回给进程，那就是 **非阻塞的**。

非阻塞一般结合 **轮询**，因为请求即需求，一般不会因数据没准备好的一次失败的非阻塞调用而丧失对数据的需求，因此失败的非阻塞IO在把控制权交回给当前线程后，当前线程一般还会不断的进行相同多个请求调用只到IO成功，这也就是**轮询**的一种形式。这种非阻塞的形式更灵活，类似的同步IO方式还有信号驱动IO与IO复用。还有一种实现非阻塞IO的目的的方式是用多个线程进行阻塞IO。

---
[1] Unix网络编程

[2] https://www.cnblogs.com/hustxujinkang/p/5072270.html

[3] https://github.com/littledan/linux-aio

## libaio

libaio是POSIX异步IO之外的一种aio，只支持O_DIRECT。其他几种[1]：

> **Thread pool of synchronous I/O threads**. This can work for many use cases, and it may be easier to program with. Unlike with AIO, all functions can be parallelized via a thread pool. Some users find that a thread pool does not work well due to the overhead of threads in terms of CPU and memory bandwidth usage from context switching. This comes up as an especially big problem with small random reads on high-performance storage devices.
>
> **POSIX AIO**. Another asynchronous I/O interface is POSIX AIO. It is implemented as part of glibc. However, the glibc implementation uses a thread pool internally. For cases where this is acceptable, it might be better to use your own thread pool instead. Joel Becker implemented a version of POSIX AIO based on the Linux AIO mechanism described above. IBM DeveloperWorks has a good introduction to POSIX AIO.
>
> **epoll**. Linux has limited support for using epoll as a mechanism for asynchronous I/O. For reads to a file opened in buffered mode (that is, without O_DIRECT), if the file is opened as O_NONBLOCK, then a read will return EAGAIN until the relevant part is in memory. Writes to a buffered file are usually immediate, as they are written out with another writeback thread. However, these mechanisms don’t give the level of control over I/O that direct I/O gives.

---
[1] https://github.com/littledan/linux-aio

## I/O多路复用 (网络IO常用) select/poll/epoll

[[linux_007_001.png]]

---

[1] Linux IO模式及 select、poll、epoll详解  (https://segmentfault.com/a/1190000003063859?utm_source=Weibo&utm_medium=shareLink&utm_campaign=socialShare&from=timeline&isappinstalled=0)

[2] Unix网络编程卷一

### edge-triggered & level-trigered

> http://www.cnblogs.com/liloke/archive/2011/04/12/2014205.html
> http://blog.csdn.net/josunna/article/details/6269235