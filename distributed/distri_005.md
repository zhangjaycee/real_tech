# 文件系统/数据库/SSD设备中的各种日志(Log)

## 文件系统中的 Logging FS 和 Log-Structured FS

* Logging(Journaling) Filesystem

Logging Filesystem(日志文件系统，又名journaling filesystem)和Log-Structured Filesystem(日志结构文件系统)是两种东西。

我们熟悉的logging filesystem(journaling filesystem)包括ext3, ext4等。他们是为了保证数据的一致性，默认将metadata“存两次”，第一次存时作为日志存储，第二次是真正存到需要存的地方。先存一遍的原因是为了在掉电等意外发生时，保证metadata的一致性，防止文件系统发生错误(比如断电时日志没有存完，下次开机时可以直接扔掉没存完的日志，原位置的数据并没有因为只有部分被覆盖而发生错误)。

日志文件系统除了对metadata存两遍的Ordered模式外，还支持Journal模式(data和metadata都存两遍)和Writeback模式(只有metadata写两遍，不同于Journal模式的是，第二遍写完时并不保证data已经落盘)。

* Log-Structured Filesystem
这也算是文件系统的一大类，其特点是追加写。所有的写操作都变成了顺序写，带来的后果是顺序读操作可能都变成随机读了。
> While the log-structured architecture was an electrifying new idea, it ultimately turned out to be impractical for production use, despite the concerted efforts of many computer science researchers. Today, no major production file system is log-structured. 

LWN中一篇介绍文件系统的文章[3]中说这种结构并没有被广泛应用。相反，这种结构在SSD中却是很常见。[1][2]


## SSD中的Log-Structured

由于SSD的写放大效应，导致SSD的写操作较读操作昂贵，所以Log-Structured这种结构天生的适用于SSD[2]。

论文[4]中还提到了Log-Structured的重叠现象，说的是应用层、FS层和SSD硬件层如果都采用了这种结构，会导致互相的不利影响，导致性能下降、容量损失和寿命损失。

## 数据库中的undo log和redo log

---

### 参考

[1] Rosenblum, Mendel, and John K. Ousterhout. "The design and implementation of a log-structured file system." ACM Transactions on Computer Systems (TOCS) 10.1 (1992): 26-52.

[2] Log-structured file systems: There's one in every SSD, https://lwn.net/Articles/353411/

[3] KHB: A Filesystems reading list, https://lwn.net/Articles/196292/

[4] Yang, Jingpei, et al. "Don't Stack Your Log On My Log." INFLOW. 2014.

[3] UTLK

[4] PLKA