# Linux I/O 模型

## 理解同步/异步和阻塞/非阻塞？

（以下为目前的理解方式）

**同步**的一般含义是两个及以上的事件同时在执行，而**异步**则相反。在通信中，同步通信指的是信号按照时钟的频率传输信号，所以信号和时钟是同步的；在I/O编程模型中，指的应该是"当前进程"与"I/O设备与内存之间数据传输过程"的同步，即当数据正在从I/O设备往内存传，要进行这次I/O的进程也是在做这个事情。

**阻塞**的含义是“堵”或者“等”，就比如我把一件事交给你办，你办不出来我不让你走。阻塞/非阻塞IO一般用在网络编程中，IO设备没有准备好所请求的信息时，IO请求的调用是否返回。若不返回一直等下去，则是阻塞的；若马上返回一个错误值表示现在还没准备好，控制权又交回给进程，那就是非阻塞的，但是一般有请求就说明对要进行IO的内容有需求，即使非阻塞IO在IO失败时把控制权交回给了进程，进程也一般采用**轮询**的形式不断进行非阻塞IO请求直到成功，这种非阻塞的形式更灵活，也更方便同时轮询多个IO设备。


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