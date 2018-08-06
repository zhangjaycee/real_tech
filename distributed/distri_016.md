# 文件系统的崩溃一致性 (crash consistency)

Crash Consistency问题在存储系统中都会存在(数据库、文件系统、dedup系统 ...)，即系统遭遇断电、崩溃等情况时，相关联的数据没有全部持久化导致的不一致。

### 崩溃到底为何导致文件系统不一致

下表整理自OSTEP笔记[1]，我们假设了一个有data和inode、bitmap两种metadata的简单文件系统，下表给出了一些可能导致不一致的情况，其中N表示断电时没有写完，F表示断电时已经完成：

| 数据块 | inode块 |bitmap块|一致性|备注|
|--------|--------|-------|----|---|
|N|N|N|一致|相当于什么也没干，FS一致，虽然写没有成功|
|N|N|F|不一致（bitmap和实际占用空间）|若bitmap记录了分配了新空间，可能导致“空间泄露”（道理类似内存泄漏），|
|N|F|N|不一致（inode指针和实际存储位置）|这时inode指向了并未更新的数据块，后续的读操作会返回一堆“垃圾”数据|
|N|F|F|不一致|同上，可能读到“垃圾”数据|
|  F  |    N    |    N |一致|虽然写请求没有成功，但因为bitmap和inode都没变，写入数据块只是相当于白写了，没有引起不一致|
|F|N|F|不一致|由于inode没有更新，可能读不到更新的数据块|
|F|F|N|不一致（bitmap空闲空间和实际所用空间）|未更新的bitmap可能导致再次申请时覆盖有效数据|
|F|F|F|一致|请求正常完成了|

多种metadata之间的一致性通常最麻烦：如上表的inode和bitmap，他们之间存在相同冗余信息（bitmap可以从inode推导出，但是这个推导是要遍历所有inode的，bitmap的作用就是用冗余的信息换取性能），并且由于并非在一个磁盘块，无法原子地同时更新，所以如果掉电时只有两者之一成功更新了，那么它们之间相同的信息便存在了不一致。metadata和data之间也存在不一致的情况：如上表中，若两种metadata都更新好了，但是data写到一半掉电了，那么下次开机后根据metadata读data时就会读到坏的数据，因此可以称为不一致。

追究其根本原因，是存储系统中底层硬件的一次磁盘I/O(512字节)，无法保证上层的一次请求的相关联的所有data和metadata的原子写入；反过来想，如果上层的每次请求中data和metadata都连在一起且小于512字节，那么就不用额外的一致性机制保证Crash Consistency。

### 保证一致性的方法--以WAL为例

由于硬件或者底层的原子写单元和上层存储系统一次请求所涉及的更改不匹配，所以我们只能在上层存储系统中用额外的手段保证crash consistency，常用的方法有: WAL(Write ahead logging, 也叫logging或journaling), CoW(Copy-on-Write, 也叫shadow paging), log-structuring, ordered write, soft updates等等。本文只简单举例说明一下WAL这种最常见的方法如何保证crash consistency：

比如，WAL为了保证bitmap和inode等不同种metadata之间一致性，在更改metadata时，一定要先将这些metadata写入到磁盘上的log区域，然后再对目标位置的metadata进行更改，这样，如果系统在写log时掉电了，原始的metadata没有影响，如果在写原位置metadata时掉电了，又可以在开机时从log进行重做(所以文件系统中的WAL类似于DBMS中的redo log)。

### 不同人对一致性有不同的认识

对于一个对任何事要求都很低的人来说，也许只有文件系统由于crash而被破坏了、不能再正常使用了才是不一致；他可能认为仅仅metadata和data的不一致可能并不算不一致，因为文件系统还会正常工作，只是被FS服务的用户或应用得到了错误的数据，谁叫他把电线拔了呢😂。因此对一致性的定义、对一致性强弱的要求也是因人而异，因系统设计目标而异的。

比如，ext4是一种基于WAL的文件系统，具体提供了3种logging模式：journal, ordered(default), writeback。这三种方法对一致性的强度依次减弱，可以帮助我们理解为什么不同人、不同场景需要不同强度的一致性：journal是把所有data、metadata先进行logging[2]；ordered是用ordered write的方法保证data和metadata的一致性，用logging保证不同类别metadata之间的一致性，ordered write指但是先写data完成，再写metadata的顺序，data因此也不用进行logging；writeback则不管data和metadata的先后顺序，data也不写log，可能刚刚提到的要求很低的人和对性能要求更高的人才会用这个参数吧。

```
摘自kernel文档[2]
data=journal		All data are committed into the journal prior to 
                        being written into the main file system.  Enabling
			this mode will disable delayed allocation and
			O_DIRECT support.

data=ordered	(*)	All data are forced directly out to the main file
			system prior to its metadata being committed to the
			journal.

data=writeback		Data ordering is not preserved, data may be written
			into the main file system after its metadata has been
			committed to the journal.
```

---
[1] http://blog.jcix.top/2018-02-24/ostep_note3/#71_Crash_Consistency

[2] https://www.kernel.org/doc/Documentation/filesystems/ext4.txt

## Journaling

本wiki的[[Log-Structured、Copy-on-Write和Redirect-on-Write|distri_005]]条目介绍了logging(journaling)和log-structing的区别。

Journaling 即 Write-ahead logging，以Ext3文件系统为例，其log机制和数据库中所说的redo log类似[1]。先写log，再写数据，如果发生crash，恢复时redo即可。除了对metadata存两遍的ext3默认的Ordered模式外，还支持Journal模式(data和metadata都存两遍)和Writeback模式(只有metadata写两遍，不同于Ordered模式的是，第二遍写完时并不保证data已经落盘，而Ordered模式中，要等数据块落盘之后再将metadata落盘)。

---
[1] https://pdfs.semanticscholar.org/presentation/2d01/803c1c7c21f3e7c4b1a2230b2e78a00d0897.pdf

## Log-structuring

其特点是追加写。所有的写操作都变成了顺序写，带来的后果是顺序读操作可能都变成随机读了。

## Copy-on-write (shadow paging)

## Soft Updates

[1]中以两种FFS实现为例，介绍了soft updates的设计理念。在最开始的FFS中，所有操作时同步的，即任何一个文件操作都要阻塞到实际磁盘修改完成才返回，同时，所有写更改也按照必要的顺序进行，这样保证了crash consistency。而后来有了FFS-async，即异步的FFS，与原来的版本对应，操作不是同步的，性能最好，但是可能掉电后文件系统就坏了，无法恢复。

soft updates位于FFS和FFS-async两者之间，同样是异步的延迟写操作，但是可以保证crash consistency。思想是让app看到的都是最新的metadata，让disk看到的都是一致的metadata，并且一致的metadata可以不是最新的。方法是将最新的metadata放到内存中延迟刷入磁盘，在刷入时要保证一定的顺序以保证crash consistency。

**Soft Updates的依赖问题：** Soft updates的难点就在怎么把内存中的各个metadata块按照能保证crash consistency的顺序刷入磁盘。为此提出了用记录以来(dependency)的方法进行排序。具体流程是：
1. 先以任意方法选一个刷写block顺序
2. 按dependency list进行检查
3. 若发现被选中的block中的metadata有依赖其他block中的数据（需要其他block先写），那么这个block中的metadata部分会被rollback到以前的safe-state，当所有所需的rollback完成后，最开始选中的被rollback处理后的block会被写到磁盘。当一个block写完后，满足的dependency会被删除，然后所有被rollback的值会被恢复。

并且soft update总结了order的规范：[2]
1. 数据结构分配好、初始化好之后再指过去。
2. 重用一块空间时要把其他指向它的指针先去掉。
3. 更改一项活跃的资源时，不要在改完之前将老的指针丢掉。

这种方法rollback/roll forward的方法肯定会导致写放大。因为有rollback就必然在后边添加roll forward的请求，如果roll forward 无法与其他请求在一个块，那么roll forward的这次写就必然是多出来的写放大。


---
[1] M. I. Seltzer et al., “Journaling versus Soft Updates: Asynchronous Meta-data Protection in File Systems,” 2000.
[2] M. Dong and H. Chen, “Soft Updates Made Simple and Fast on Non-volatile Memory,” Atc, 2017.