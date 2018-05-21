# 文件系统的一致性问题 (crash consistency)

在存储系统中都会存在(数据库、文件系统、dedup系统 ...)，即系统遭遇断电、
崩溃等情况时，相关联的数据没有全部持久化导致的不一致。

根本原因是存储系统中底层的一次I/O，无法保证上层的一次
请求的相关联的数据的原子写入，所以需要上层的机制保证一
致性。 (相关联的数据一般指metadata和data，如文件系统中的inode和用户数据)

常用的保证一致性的方法: WAL(Write ahead logging, 也叫journaling), 
CoW(Copy-on-Write, 也叫shadow paging), log-structuring, 
soft updates。

## Journaling

本wiki的[[Log-Structured、Copy-on-Write和Redirect-on-Write|distri_005]]条目介绍了logging(journaling)和log-structing的区别。

Journaling 即 Write-ahead logging，以Ext3文件系统为例，其log机制和数据库中所说的redo log类似[1]。先写log，再写数据，如果发生crash，恢复时redo即可。除了对metadata存两遍的ext3默认的Ordered模式外，还支持Journal模式(data和metadata都存两遍)和Writeback模式(只有metadata写两遍，不同于Ordered模式的是，第二遍写完时并不保证data已经落盘，而Ordered模式中，要等数据块落盘之后再将metadata落盘)。

---
[1] https://pdfs.semanticscholar.org/presentation/2d01/803c1c7c21f3e7c4b1a2230b2e78a00d0897.pdf

## Log-structuring

其特点是追加写。所有的写操作都变成了顺序写，带来的后果是顺序读操作可能都变成随机读了。

## Copy-on-write (shadow paging)

## Soft Updates