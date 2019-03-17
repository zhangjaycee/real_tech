# Linux Storage Stack 存储I/O栈

## I/O一般经过的Linux I/O 层次

```
(VFS层)
(文件系统层)
(Page Cache层)
submit_bh (生成bio结构) -> submit_bio(提交bio结构到通用块层)
(通用块层及IO调度)
(驱动层)
```


## 一次存储I/O会有多少次内存拷贝 [3][4]

对于 read/write 调用，一般有 `存储外设--page cache--用户缓冲区` 两次拷贝；但对于用 `O_DIRECT` 的情况，只有`存储外设--用户缓冲区`这一次拷贝。

对于 mmap 调用，只有`存储外设--page cache`一次拷贝，因为用户的访问直接映射了page cache中相应的page。



## 存储栈图：

![](https://www.thomas-krenn.com/de/wikiDE/images/e/e0/Linux-storage-stack-diagram_v4.10.png)

[1] High Performance Storage Devices in the Linux Kernel, https://www.slideshare.net/kerneltlv/high-performance-storage-devices-in-the-linux-kernel

[2] Linux Storage Stack Diagram, https://www.thomas-krenn.com/en/wiki/Linux_Storage_Stack_Diagram

[3] Does mmap directly access the page cache, or a copy of the page cache? https://www.quora.com/Does-mmap-directly-access-the-page-cache-or-a-copy-of-the-page-cache

[4] 聊聊Linux IO, http://0xffffff.org/2017/05/01/41-linux-io/
