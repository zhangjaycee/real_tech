# Linux Storage Stack 存储栈

## IO函数调用一般流程

```
(VFS层)
(文件系统层)
(Page Cache层)
submit_bh (生成bio结构) -> submit_bio(提交bio结构到通用块层)
(通用块层及IO调度)
(驱动层)
```


## 存储栈图：

![](https://www.thomas-krenn.com/de/wikiDE/images/e/e0/Linux-storage-stack-diagram_v4.10.png)

[1] High Performance Storage Devices in the Linux Kernel, https://www.slideshare.net/kerneltlv/high-performance-storage-devices-in-the-linux-kernel

[2] Linux Storage Stack Diagram, https://www.thomas-krenn.com/en/wiki/Linux_Storage_Stack_Diagram