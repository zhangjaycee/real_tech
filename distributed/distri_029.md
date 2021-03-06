# PM系统编程模型

PM是很特殊的设备，它既是内存接口，又有非易失的存储特性。因此：**作为内存**，它即面临内存所特有的cache coherence等问题；**作为存储**，它也面临外存系统所特有的崩溃一致性、持久化等问题。

因此，构建一个基于PM的存储系统也所要考虑的问题是比较多的。近年来，学术界大量文章都在关注PM存储系统或者PM编程模型，比如PM感知文件系统、PM KV存储、PM事务框架等。

本文分为**原子性、持久化和崩溃一致性**三小节，讨论了PM系统编程的一些必须注意的点。文章整体基于我之前所写调研综述的相关部分，并进行了精简和修改。本文参考了很多文章并加入了自己的理解，若有问题，恳请指正。


### 1. 原子性 (Atomic Updating)

这里的原子性指的是原子更新粒度(原子操作)或并发时的原子可见性(隔离性)，而非ACID事务的原子性。虽然ACID事务的原子性也是需要借助原子操作实现，这里的原子性更类似与ACID中的I(isolation, 隔离性)。

PM是内存接口，其原子性操作和内存类似，因此其访问原子性也和内存一样，在无锁保护的情况下， x86 平台上支持8、16 或 64 字节原⼦性更新：

* **8 字节原子更新:** 64 位处理器的 store 命令都是 8 字节粒度的原⼦更新。 

* **16 字节原子更新:** 现代处理器可以使⽤加 LOCK 前
缀的 cmpxchg16b 指令实现 16 字节的原⼦写。

* **64 字节 (cacheline 粒度) 原子更新:** 利⽤硬件事务型内存 (hardware transactional memory, HTM) 可以实现 64 字节的原⼦更新。Intel 平台对应的技术称 为 RTM(Restricted Transactional Memory)，RTM 可以在事务内保证可以保证某个 cacheline 的所有数据不被刷⼊内存。要原⼦地更新某个 cacheline，⾸先⽤ XBEGIN 开始⼀个 RTM 事务，然后在是事务内对⽬标 cacheline 进⾏所需的修改，最后写 XEND 结束这个事务。在事务完成后，再进⾏ clflush 等命令，保证被修改过的 cacheline 就被原⼦地写回PM。

内存中的数据结构存在多线程并发访问的问题，PM数据结构也同样这样的问题，除了借助上述原子性更新设计无锁数据结构和加锁等方法外，近期工作中还常用HTM事务的方式保证数据结构的并发访问。如前文所述，Intel平台的HTM技术被称为TSX或RTM；IBM POWER8等平台的也支持类似的技术。使用HTM时，程序员以XBEGIN和XEND开始或结束一个事务，事务中可以执行需要保护的代码。HTM从硬件上事务相关的各个cacheline的原子可见性。若事务直到XEND都没有发生冲突，则所有的修改将被提交，若中途发生冲突，所有修改将被丢弃，事务将尝试从XBEGIN重新执行。很多PM相关工作也将HTM用于PM+DRAM混合数据结构的DRAM部分。

虽然HTM可以保证某个事务执行过程中一个或多个cacheline的原子可见(或并发安全)，但是在XEND之后，这些cacheline仍处于不可控状态，如前文所讨论，cache与PM之间的传输粒度为64字节，所以同一事务中的多个cacheline仍然无法被原子地写回PM；另外，也不能依靠电容保护的cache刷新来保证断电时的持久性，因为断电时，单一事务不一定已经完成，这种持久化会违背事务的原子可见性。

### 2. 持久化 (Durability)

然而，对PM的store操作后并不能保证数据肯定存储到PM上，这是因为CPU和PM之间还有几层cache，要保证持久化，我们需要用flush / fence相关的指令。

当使用PM时，CPU对内存的store操作可能会暂存在硬件管理的cache或者write buffer中，若用户我强制刷cacheline到内存，无法保证store操作的数据何时写到内存中。在原来的情况下，内存为掉电易失的DRAM，所以刷或者不刷cacheline只可能牵扯到系统的性能，而不会影响系统的正确性；但是在使用PM时，由于持久化的存储是我们的目标之一，我们就要额外注重数据持久化的时机，以进行更精确的控制。

在使用块设备时，类似的问题一致存在。写操作一般会被缓存到系统的page cache中，因此需要用户调用fsync等函数来进行磁盘同步，让数据真正持久化地存储到磁盘上。解决PM cache数据写回的问题和块设备同步磁盘问题的思路是类似的，只不过方法不同。如下图，在x86平台中，当数据离开CPU cache进入PM或者进入电容保护的持久区(虚线框)，便意味着数据已经被持久化，因此只要使用将数据刷出cache并写回PM的指令，就可以保证相应数据持久化存储到PM了。

[[distri_029_001.png]]

由于一般在使用PM时，是通过内存映射的方式进行的，所以使用操作系统实现的msync函数是可行的(msync和fsync具有相同的语义)。除此之外，用户也可以直接调用x86平台的cache刷新指令进行数据同步。

|**指令** | **说明** |
|-|-|
|CLFLUSH| 几乎所有CPU都支持，但没有任何并发性，串行地执行|
|CLFLUSHOPT + SFENCE | 比CLFLUSH新，但是不是串行执行的，因此需要SFENCE |
|CLWB + SFENCE | 相对CLFLUSHOPT，可以在刷入PM后仍然让cache保持有效，局部性较好的数据使用此命令可以提升性能 |
|NT stores + SFENCE | 即non-temporal store，直接跳过cache的store命令，因此不需要刷新cache |
|WBINVD | 只能在内核模式用，将所有CPU的cache 刷入PM，一般不用，太影响性能 |

上表列出了其他的cache刷新指令，它们的行为各有不同，需要依据场景进行选择。除表中最后一项外，其他指令都是可以在用户空间直接使用的。在用户控件调用cacheline刷新指令的好处是不用切换到内核态，且用户能更清楚地知道哪块数据需要马上写回PM，所以用户的控制更精细，刷新指令的性能也要好于msync。但是，一些PM感知文件系统也需要msync的控制权，因为数据刷入PM若需要造成PM感知文件系统的metadata改变，那么用户空间使用cacheline刷新指令将导致PM感知文件系统metadata的不一致。所以用户程序应该仅在确保文件系统安全的情况下才使用cacheline刷新指令。

### 3. 崩溃一致性

首先，本文定义两种存储系统崩溃一致性模型的定义：

PM作为一个非易失设备，为PM设计存储软件系统时，也面临存储系统普遍存在的崩溃一致性问题(Crash Consistency)，这个问题同时涉及PM的持久性和原子性问题。

崩溃一致性的简介可以参考我之前的文章 [2]。简单说，存储系统的崩溃一致性其实类似数据库系统事务要实现的ACID性质，我们可以把存取请求看成事务。Atomicity即保证请求完全成功或者完全失败，Consistency即保证存储系统中所有元数据之间甚至元数据和数据之间是一致的或者说合理的，Isolation即在并发的情况下，保证两次请求互相不会看到各自执行到一半的状态，Durability即保证存储系统的某次请求若执行完成则相关的数据一定已经被写到存储设备中。在使用非易失的PM设备情况下，我们就是要在上两小节所述的原子性和持久化条件下实现存储系统的“崩溃一致性”。

#### 3.1. 崩溃一致性模型

首先，我们提出两种存储系统崩溃一致性模型的定义：

**顺序写(ordered write)模型：** 规定一组原子的数据存储单元间有一定的因果顺序(或依赖关系)，先存的数据不依赖于后存的数据，因此，当数据按这个顺序存储到存储设备的过程中，无论何时发生断电或崩溃，系统仍是一致的。

早期的Unix文件系统FFS便是以同步写的方式保证写的顺序性，但是同步导致的阻塞降低了性能；与这种低效但一致的机制相反，若挂载FFS时加入async选项，FFS的所有写操作便异步且无序地进行，虽然这样性能会很好，但顺序一致性无法保证，系统崩溃可能会导致文件系统的损坏。Soft updates方案则是将同步顺序写改为异步顺序写，兼顾了性能和一致性。SoupFS就是在Soft updates方案基础上针对PM进行改进的PM感知文件系统。 

**事务(transactional)模型：** 规定某一组原子的数据单元间是存在相互依赖关系的，先存的数据和后存的数据相互依赖，因此，只有保证整组数据全部存到磁盘或者全部没有存到存储设备，系统才是一致的。

由于原子写粒度小于整组数据大小或者数据分散于多个写单元这两种情况是非常常见的，使用事务模型就需要额外的机制保证事务一致性，比如logging(journaling)、log-structuring、copy-on-write等。

显然，**顺序写模型**对一致性的要求弱于**事务模型**。而且，事务模型一般就是建立在顺序写模型基础上的(比如日志要先于数据写到磁盘上)。使用哪种模型要取决于所存数据的实际依赖关系和系统设计者对系统一致性的需求。例如，要保证文件系统的bitmap和inode两种metadata之间的一致性就必须采用事务模型，因为文件系统中bitmap的用于指示存储空间的分配状况，各个文件的inode也存储有各个文件的大小及数据块位置，那么这两种数据便存在相互依赖关系，在用户对某个文件的写操作导致文件增大时，bitmap和inode需要同时改变，在这次用户操作前后的一致性就必须采用事务模型保证。

很多存储系统中会**结合两种模型**。例如，ext4是一种基于WAL(write ahead logging)的文件系统，具体提供了3种logging模式：journal, ordered(default), writeback。这三种方法对一致性的强度依次减弱，其中journal是把所有data、metadata先进行logging，即对data和metadata都采用事务一致性模型；ordered是用顺序一致性模型保证data和metadata之间的一致性，用事务模型保证不同类别metadata之间的一致性，即先写data完成，再写metadata，并且对metadata进行logging。

#### 3.2 保证PM存储系统一致性所面临的难题

虽然对于某种存储系统，我们可以用不同的崩溃一致性模型或不同的一致性强度为系统设计合适的一致性机制，但是我们并不能直接将适用于块设备的一致性机制直接移植到PM，这是内存系统和I/O系统硬件或架构不同导致的，原因主要有三个方面：

**原子持久化粒度和传输粒度不匹配问题：** 使用块设备时，块设备是与内存进行数据传输的，他们间的原子持久化单元512字节；PM的原子持久化粒度(failure-atomic)是8字节。但在保证崩溃一致性的问题上，PM与块设备不只是原子持久化大小不同：块设备的传输和持久化单元都是512字节，PM与cache的传输粒度是64字节，大于原子持久化粒度8字节，这是因为虽然CPU位宽是64比特，当前处理器和内存的cache flush指令却是对应8次数据传输，也就是数据传输的粒度是64比特 × 8 = 64字节。

这与前文所述的原子更新粒度并不等价，我们可以用当前平台普遍的8字节、加LOCK前缀的cmpxchg16b指令的16字节和用RTM(HTM)保护的64字节为更新粒度。但是进行持久化时，16字节或64字节的传输依然可能被断电或崩溃打断。


**non-TSO平台store指令乱序执行问题[5]：** 而且由于PM接入内存总线，需要注意硬件平台的内存一致性协议，x86等平台使用TSO(total store ordering)协议，所有store指令之间不会被打乱执行顺序。所有store指令之间不会被打乱执行顺序。arm等平台使用协议可以对应地称为non-TSO，即store指令之间也可能被打乱顺序，这时不只是cacheline刷新指令后需要加fence指令，必要时store命令后也要加fence指令。(fence指令的开销虽然不能忽视，但相对cacheline刷新指令开销要小很多。)

**Cacheline刷新不可控问题[6]：** 另外，cacheline还存在过早自动刷新的问题，在文献[6]中称之为“premature cache evictions”。由于cache替换策略是由硬件实现的，
虽然cache和PM间以cacheline为粒度，但若不使用RTM事务加以保证，即使不调用cache刷新指令，cacheline也可能随时被刷出cache，因此要注意，若使用顺序写模型，每次进行(8字节、16字节或RTM保护的64字节)原子更新都要以clflush+sfence进行刷新。否则可能会发生错误：比如，我们先后store了位于两个cacheline的变量A和B，若没有在store A之后加入clflush+sfence，B所在的cacheline可能会被先于A所在cacheline被刷入PM，这时若A还在cacheline并发生了断电，那么下次启动时，只有B在内存中，A不在内存中，不符合store的顺序。在易失的DRAM中是没有这个问题的，因为DRAM断电易失，CPU到cache若已经考虑了store A先于store B，就不用再考虑cache到DRAM的顺序问题。

所以在为PM设计使用顺序写模型的存储系统时，需要注意一下几点：
1. 每个原子更新的数据单元小于8字节、16字节或64字节；
2. 若以8字节或16字节进行原子更新(即直接store指令更新)且在non-TSO平台下，要在每个store命令之后加入fence指令，防止store指令被乱序执行。
3. 要及时刷新其所在的cacheline并加fence指令防止cacheline刷新被乱序执行；

使用事务模型时，在需要保证刷新cacheline顺序时，同样需要注意上述问题。

---

### 部分参考文献


[1] Rudoff, Andy. "Persistent memory programming." Login: The Usenix Magazine 42 (2017): 34-40.

[2] 存储系统的崩溃一致性问题 (Crash Consistency), [http://blog.jcix.top/2018-08-06/crash_consistency/](http://blog.jcix.top/2018-08-06/crash_consistency/)

[3] Arpaci-Dusseau, Remzi H., and Andrea C. Arpaci-Dusseau. Operating systems: Three easy pieces. Arpaci-Dusseau Books LLC, 2018.

[4] S. R. Dulloor et al., “System software for persistent memory,” Proc. Ninth Eur. Conf. Comput. Syst. - EuroSys ’14, pp. 1–15, 2014.

[5] D. Hwang, W.-H. Kim, Y. Won, and B. Nam, “Endurable Transient Inconsistency in Byte-Addressable Persistent B+-Tree,” 16th USENIX Conf. File Storage Technol. (FAST 18), pp. 187–200, 2018.

[6] E. R. Giles, K. Doshi, and P. Varman, “SoftWrAP: A lightweight framework for transactional support of storage class memory,” MSST 15, vol. 2015–Augus, 2015.