# Linux I/O 模型

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

> [Linux IO模式及 select、poll、epoll详解]  (https://segmentfault.com/a/1190000003063859?utm_source=Weibo&utm_medium=shareLink&utm_campaign=socialShare&from=timeline&isappinstalled=0)

### edge-triggered & level-trigered

> http://www.cnblogs.com/liloke/archive/2011/04/12/2014205.html
> http://blog.csdn.net/josunna/article/details/6269235