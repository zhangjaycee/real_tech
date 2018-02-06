#  Log-structured & Copy-on-write

## 1. log-structured、copy-on-write和redirect-on-write

copy-on-write和redirect-on-write在快照中都很常用。前者指写数据时，将被快照的数据拷贝到别处，然后在原位置覆盖写；后者redirect-on-write指直接将新的数据块写到空白处，这样就避免了拷贝(对原数据块一次读和一次写)，不过应该要建立新的映射。

log-structured结构最初是FS中用于将随机写转为追加顺序写的结构，CoW、RoW与之相似的地方是由于性能问题，被拷贝的数据或新写的数据也一般也会顺序追加都后边。所以CoW、RoW是为了达到快照的目的而进行原数据块拷贝或新数据块异地写，并未规定一定要顺序追加地写。log-structured是为了以顺序追加写来优化磁盘的写性能，并不一定是因为要实现快照技术。

LFS用了log-structured技术。

WAFL、Btrfs和ZFS的快照都是用了RoW技术。LVM的快照用了Cow技术。

qcow2是QEMU Copy on Write Version 2的简称，但其快照机制更类似RoW技术，只不过write时，它是将原数据从backing image拷贝到了新的image file里，这样保证了对进行快照的backing image的读操作。

---

[1] What is the difference between log structured filesystems and copy on write filesystems?, https://www.quora.com/What-is-the-difference-between-log-structured-filesystems-and-copy-on-write-filesystems

[2] zfs & btrfs are ROW not COW – redirect-on-write, not copy-on-write

[3] Snapshots? Don’t have a C-O-W about it!, https://storagegaga.wordpress.com/tag/redirect-on-write/

## 2. Log-structured

#### 文件系统中的 Logging FS 和 Log-Structured FS

* Logging(Journaling) Filesystem

Logging Filesystem(日志文件系统，又名journaling filesystem)和Log-Structured Filesystem(日志结构文件系统)是两种东西。

我们熟悉的logging filesystem(journaling filesystem)包括ext3, ext4等。他们是为了保证数据的一致性，默认将metadata“存两次”，第一次存时作为日志存储，第二次是真正存到需要存的地方。先存一遍的原因是为了在掉电等意外发生时，保证metadata的一致性，防止文件系统发生错误(比如断电时日志没有存完，下次开机时可以直接扔掉没存完的日志，原位置的数据并没有因为只有部分被覆盖而发生错误)。

日志文件系统除了对metadata存两遍的Ordered模式外，还支持Journal模式(data和metadata都存两遍)和Writeback模式(只有metadata写两遍，不同于Journal模式的是，第二遍写完时并不保证data已经落盘)。

* Log-Structured Filesystem
这也算是文件系统的一大类，其特点是追加写。所有的写操作都变成了顺序写，带来的后果是顺序读操作可能都变成随机读了。
> While the log-structured architecture was an electrifying new idea, it ultimately turned out to be impractical for production use, despite the concerted efforts of many computer science researchers. Today, no major production file system is log-structured. 

LWN中一篇介绍文件系统的文章[3]中说这种结构并没有被广泛应用。相反，这种结构在SSD中却是很常见。[1][2]


#### SSD中的Log-Structured

由于SSD的写放大效应，导致SSD的写操作较读操作昂贵，所以Log-Structured这种结构天生的适用于SSD[2]。

论文[4]中还提到了Log-Structured的重叠现象，说的是应用层、FS层和SSD硬件层如果都采用了这种结构，会导致互相的不利影响，导致性能下降、容量损失和寿命损失。


#### log structured merge tree

HBase、levelDB 都用这种树，适合于写大于读的数据库。


---

[1] Rosenblum, Mendel, and John K. Ousterhout. "The design and implementation of a log-structured file system." ACM Transactions on Computer Systems (TOCS) 10.1 (1992): 26-52.

[2] Log-structured file systems: There's one in every SSD, https://lwn.net/Articles/353411/

[3] KHB: A Filesystems reading list, https://lwn.net/Articles/196292/

[4] Yang, Jingpei, et al. "Don't Stack Your Log On My Log." INFLOW. 2014.

[5] UTLK

[6] PLKA

[7] Log Structured Merge Tree, https://www.slideshare.net/ssuser7e134a/log-structured-merge-tree

## 3. Copy-on-write (COW)

### qcow2镜像格式中的COW


---
[1] qcow2 doc, https://github.com/qemu/qemu/blob/master/docs/interop/qcow2.txt

[2] Q. Chen, L. Liang, Y. Xia, and H. Chen, “Mitigating Sync Amplification for Copy-on-write Virtual Disk,” 14th USENIX Conf. File Storage Technol. (FAST 16), pp. 241–247, 2016.