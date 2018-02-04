# OSTEP Part1(Virtualization) 笔记

大部分截图来自原书，贴出书的官方主页： 《[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)》
(作者Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau)。感谢原作者这么好的书。

## 第一节 进程的抽象

#### 1. 策略和机制

Policy在mechanism（策略和机制）在操作系统中通常是分开设计的。比如如何切换上下文是一个low-level的mechanism，指底层的方法或者协议。当前时刻应该让哪个进程运行更好是一个high-level的policy的问题，指一些“智能”的调度。


#### 2. 虚拟化和OS

OS本身就可以看做是“虚拟机”(virtual machine)。系统通过在可以被接受的合理开销（时间、空间）范围内，将计算机CPU、内存、存储等资源进行虚拟化（抽象），目的是为了用户的方便使用。

**CPU虚拟化** 主要体现在将任务抽象为 **进程(process)** ，将资源按进程隔离，然后多个进程轮转使用计算资源； **内存虚拟化** 主要体现在 **虚拟地址空间(virtual address space 或 adress space)** ；而对于持久化的 **存储** ，OS让文件共享，没有那么多私有隔离，OS假定用户会用文件来共享数据。 (？？？？)

## 第二节 进程API

#### 2.1 fork和exec

* exec()函数组和fork()的区别是，exec执行以后就再也不会返回


# OSTEP Part3(Persistence) 笔记

大部分截图来自原书，贴出书的官方主页： 《[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)》
(作者Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau)。感谢原作者这么好的书。

## 第一节 I/O Device

#### 1.1 IO 总线

**一般情况下，** IO设备的性能较差(慢)，所以用Peripheral IO Bus，为什么不用像显卡一样用的PCI呢？因为1)越快的总线越短，这样空间不够插；2)越快的总线制作成本越高，如果存储设备照总线的性能差的远，没必要用高性能总线。

[[p3_001.png]]

这张图为总线的层次结构，memory bus是最快的也是最近的，IO Bus比较远，也是最慢的，中间有用于显卡的PCI等总线。

#### 1.2 典型设备的组成部分

[[p3_002.png]]

一个典型的外围设备如图所示，包括两部分： **接口** 和 **内部结构** 。

**接口：** 类似软件接口的功能，硬件接口是留给OS和设备交互的。
**内部结构：** 比如㓟CPU、MEM等基本组件，还有称为固件(firmware)的软件来实现内部功能。

#### 1.3 PIO中的两种模式(Polling和Interrupt)

一种典型的协议是 **Polling** (轮询)，步骤有4: 

* 循环等待STATUS寄存器直到设备状态为不busy
* 写数据到DATA寄存器
* 写命令到COMMAND寄存器
* 循环等待STATUS直到设备为不busy

Polling显著的缺点就是太浪费CPU时间，这是因为IO相对于CPU是很慢的，大量的CPU时间被用在了等待上。

**Interrupt** (中断)方法可以解决这个问题，用Interrupt方法进行IO时，当设备完成操作时，会raise一个硬件interrupt。但是这样的话，如果设备很快(不如现在的NVMe SSD设备)，Interrupt由于需要进程上下文的切换、以及中断的控制等原因，会拖慢IO的速度。所以两种方法各有利弊：

|Polling | Interrupt |
|--------|--------|
| 浪费CPU时间 | 节省CPU时间 |
| 更小的I/O延迟 | 进程切换及中断处理导致高延迟 |

在IO请求压力时大时小不好确定的系统中，更好的方案可能是采用hybrid(混合)的 **两段协议** ，先poll一会儿，还没完成的话改用interrupt方式。还有一种方式是 **中断合并** ，当一个请求完成，等一等，说不定又有新的请求完成了，这样就见小了中断数，减小了中断带来的性能损失，但是这样做的缺点也是显而易见的--用延迟代价换来了高吞吐。

#### 1.4 设备交互：PIO和MMIO

以上的Interrupt和Polling都属于Programmed I/O(PIO)的方式，这种方式是CPU通过指令和设备进行的交互。

还有一种称为Memory-mapped I/O(MMIO)，这种方法中，设备寄存器被映射到内存地址空间，OS读写这个映射地址，硬件会自动将存取数据路由到设备而不是主存中。

#### 1.5 PIO中传输任务的卸载(Direct Memory Access, DMA)

若不使用DMA，虽然可以用中断来讲等待设备IO完成的时间用在其他进程上，但是IO请求中还包括CPU从内存到设备以字长为单位一点一点搬运数据（数据传输）的过程，如图：

[[p3_003.png]]

有了DMA这种专用设备帮CPU搬运，流水线就可以入下图一样：

[[p3_004.png]]

当DMA完成任务，DMA控制器会raise一个中断，这样OS就知道传输完成了。

#### 1。6 设备驱动和I/O栈

I/O栈各层的抽象(如块设备驱动、文件系统等)当然有好处，其把不同的设备封装成统一的结构，但也有坏处。

其实不是从上层应用到底层驱动会出现信息丢失的问题(我曾经调研过上层到下层会有语义鸿沟的问题)，底层的设备由于统一的抽象也会“丧失个性”，比如SCSI支持多种IO错误信息，但是ATA/IDE却不支持，因此Linux设计成上层文件系统只能接到更"EIO"错误(generic IO errer)。

驱动占Linux源码的70%，很多驱动都是“业余”开发的，因此很多系统崩溃也是由于驱动bug造成的。

## 第三节 RAID

书中有个对比表总结的不错：

[[p3_005.png]]]

## 第四节 文件和目录

文件(file)和目录(directory)是OS虚拟化中存储部分的两个重要的抽象概念。

本节主要解释一些基本的文件操作和对应的系统调用。比如：

| 常用操作 | 系统调用 |
|--------|--------|
|  cat命令   | open() / read() / write()  |
| 数据同步  |   fsync()     |
|   mv命令重命名   |   rename()     |
|  ls的-l参数、stat命令    |   stat() / fstat()      |
|    rm命令    |    unlink()    |
|     mkdir命令    |   mkdir()     |
|文件夹操作函数|opendir() / closedir() / readdir()|
|rmdir命令|rmdir()|

这节还讲了硬链接和软连接、创建和挂载文件系统的内容，略了。。


## 第五节 文件系统的实现

本节主要讲，要实现一个文件系统的基本功能上应该怎么实现。

#### 5.1 文件系统的根本

对于文件系统，我们头脑中应该有一种模型：文件系统(Filesystem, FS)由接入部分和基本数据结构部分组成。前者指的是read()、write()等这样的接口；后者关系到FS内部怎么组织存储用户数据和元数据。设计时，不同的文件系统一般都有相同的接口，不同FS的主要区别是内部的 **数据结构** 。

#### 5.2 整体结构

文件系统内的数据可以分为用户数据(data)和元数据(metadata)，元数据可以简单的理解为数据的数据。上节所讲的文件系统的两种重要抽象（文件和目录），都需要存储data和metadata。

**data：**
  * 文件的data自然是用户数据，我们不需要关注用户数据的具体内容；目录的data应该存储文件名和对应文件的metadata。

**metadata：**

  * **inode** 文件的metadata是inode(曾经是index node的缩写)或者类似inode但不叫inode的东西；目录的metadata也是inode。inode以某种结构存储有对应文件或目录的数据块地址。
  * **bitmap**(或free list) 是与整个文件系统空闲空间相关的metadata，FS需要分配新空间时，会从这里查询哪里有空闲位置。分为data的bitmap和inode的bitmap。这里的bitmap也可以换为使用free list其他的数据结构。可以说，bitmap是metadata(文件和目录的inode)的metadata和data(文件和目录的data)的metadata，不过也还是metadata。。。
  * **superblock** 记录有文件系统最大inode数、inode块和数据块从哪个地址开始等信息，是整个文件系统的metadata。

#### 5.3 Inode

**组成：** 每个inode都有一个inumber，由于inode是顺序排列的，给定inode table开始块的地址、inode的大小和inumber就可以知道这个inode在哪个块了。inode中包含的信息包括：type（一般文件还是目录）、size（文件大小）、各种时间信息、指向数据块的地址“指针”（索引）等。

**数据块地址索引：** 其中的地址“指针”可以分为两类，最简单的直接指向相关的data块，称为direct pointer；另一种更常应用的交indirect pointer。

为什么要用indirect呢？因为一个inode的空间是有限的，如果文件数据太大，inode中留给存储块地址的空间装不下。于是就有了间接的两层索引、三层索引这种结构。例如，三级索引中，总共inode有n个地址空间有a个直接索引，b个二级间接索引，c个三级间接索引，那么有`n=a+b+c`；如果设一个数据块可以存m个索引，块的大小为4KB，支持文件的最大大小为`4KB * (a + b * m + c * m * m)`。

显然，这个多级索引结构是个非平衡树，也是不对称的，看了让人挺难受（强迫症），为什么这样设计呢？这是出于多数文件都很小的事实。

**FAT的链式存储：** FAT等FS没有inode，而是只存储第一个数据块的地址（类似链表头），然后下一个块的地址可以去前一个块找。这只是道理上的，如果真的这么做，随机访问肯定超级慢，所以还内存中存在一种存有连接信息的表，（可以看成key-value形式，用块的地址作为key，用下一个块作为value），这样就可以在内存中完成“链表的遍历”，加速了这种思路。这种结构的缺陷之一是无法创建硬链接。

书的作者给出了几种事实对设计FS很有借鉴意义：

| 事实 | 数据 |
|--------|--------|
|  多数文件都很小 |  多数都在2KB左右      |
|   平均大小会大一些     |  200KB左右      |
|   大多数数据都在大文件中     | 少数的大文件占据了大部分的空间     |
|   文件系统有很多文件  |  平均接近100k个     |
|   文件系统一般都是没满的 |  即使磁盘空间在变大，还是有50%空间空闲      |
|  目录一般都很小      |   平均小于20个项     |

#### 5.4 目录的组织

在作者的例子中，目录和文件是类似的，都有inode，只不过目录的data中有文件名和文件inode地址的映射，这是一种类似线性链表的结构，所以目录如果深的话查找开销会比较大。

目录的组织是对数据结构的一种设计和选择，当然也可以有不同的选择，比如XFS就采用了B-tree作为目录的存储组织结构（这样在创建文件时也很容易确定是不是重名）。

#### 5.5 空闲空间的管理

和目录的组织一样，作者的例子用了bitmap，但还可以用free list链表形式或者B-tree(XFS)等很多形式进行管理，这将导致性能和空间的trade-off。

当使用空闲空间时，尽量将连续的空间分配给需要的文件，这样的启发式方法会增加文件读写的速度（请求次数更少、一次顺序读写更多）。

#### 5.6 read()和write()的过程

作者的例子中，一次读或写请求会导致多次IO。尤其对于写时不存在的文件进行creat操作时，需要更多的IO，因为要逐级更改上层目录data和inode等。读和创建文件的操作如下两图：

[[p3_006.png]]

[[p3_007.png]]

#### 5.7 缓存和缓冲区(caching and buffering)

现代系统一般将virtual memory pages和文件系统pages合并成统一的page cache(unified page cache)，这样内存可以被更灵活的在虚拟内存和文件系统间分配（？）。

write buffering是有好处的，等一等再往下存，可以batch一些请求或者减少请求（如创建后马上删除），现在的文件系统一般都会等5s或30s之类的。这样做是有trade-off的：增加了延迟，增加了系统crash时数据丢失的可能。DBMS等系统决不允许这样导致数据丢失，因此可以勤用fsync()同步、用direct I/O绕过缓存或用raw disk接口绕过文件系统。但是一般这种trade-off在作者看来是可以接受。


## 第六节 局部性和FFS(Fast File System)

本节主要讲了FFS，一种84年提出的Unix文件系统，ext2和ext3的前辈。

在FFS之前，磁盘的性能很差，主要是因为人们没有考虑底层磁盘的特性，把磁盘当成了一个随机存储设备。例如，相对更古老Unix FS中的碎片没有被适当的处理，越来越碎，性能越来越差；而且块太小只有一个扇区的大小，这会导致开销增大（传输一次的量太小了）。

#### 措施1：分组存储

将整个文件系统分成Cylinder Group，每个Group都类似一个文件系统，甚至有冗余的Superblock。ext2和ext3中把这种结构称为block group。

这样存储就可以实现一些策略，这些“启发式”的策略并不是通过详细的论证得到，都是基于经验的，也是很管用的：1）将相关的文件（如同一个文件夹中的文件）放到一个组中（空间局部性，虽然FFS考虑了空间局部性，但没有考虑时间局部性，比如编译文件夹和源码文件夹在相距很远的两个目录里，就可能导致反复的查询）；2）创建文件时平均让各个组的空余inode数平衡等。


#### 措施2：大文件的分组存储

大的文件如果大到占了一个组的大部分，就开始破坏组内的局部性了，因为很少有地方可以存相关的文件了。因此可以根据预先设定，一个组内一个文件最多存多少块，如果多于这个数，就把一个文件分在多个组中存。

这样固然会降低存储效率，但是降低的应该不多，因为即使分块了，大文件的每个块依然较大，一次还是可以传输较多的数据，这样，传输所占的时间还是远大于请求所占的时间。这也是可以用数学公式计算一下比例的（摊还分析），作者在书中进行了推导，要达到50%的带宽，一个块400K即可，要达到99%的带宽，一个块需要40MB。（当然这只是针对磁盘，现在的高性能设备就不一定了！）

作者还讨论了HDD中顺序请求也可能让磁头旋转可能过头的问题。解决方法如图，具体解释，略。。。

[[p3_008.png]]


## 第七节 FSCK和Journaling


#### 7.1 Crash Consistency

FS的数据结构和其他内存中的数据结构不同，必须持久化存储。但是由于一次写请求是必定引起多次的磁盘IO（比如，要更新一个文件，需要更新或添加数据块、更新inode信息、可能更新bitmap块等。），若在一次写请求的多次IO之间系统崩溃了（可能由于断电等原因），那么文件系统结构就可能出现不一致。作者将这个问题成为crash consistency问题，并假设一次写请求分解成了3次基本IO操作（更新数据块、更新inode块、更新bitmap块），总结了几种情况，总结如下表(F for finished, N for not finished)：

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

FSCK和Journaling是保证crash consistency的两种最基本、最广泛的方法。FSCK即File System ChKer, Journaling又可以叫logging，都是保证crash consistency的方法。这些保证只是说保证系统不发生错误，无法保证写请求的成功。（类似DBMS的事务，consistency就是一次事务要么完了，要么没发生过，不能发生一半）

#### 7.2 FSCK

思路很简单，在每次FS挂载时，进行FSCK检查，进行必要的修复。 **缺点是很慢，因为每次都要全局进行检查。** 检查方法如下：

**Superblock** 检查超级块有没有异常，如果有异常，会启用备用超级块。

**Bitmap** 逐一检查inode和indirect块，生成一个记录分配情况的新bitmap，这样就不会有数据块和inode块与bitmap记录的不一致的问题。

**Inode** 检查有没有异常，比如标志位是不是有效，检查Inode的link count是不是正确，如果inode没有被任何目录指向，会放到lost+found文件夹；如果指向的块没有在有效范围，可能inode会被清除以保证一致性。

**Data block** 如果两个inode指向同一个块，会复制一份让两个inode各自拥有一份数据块；directory数据块会检查前两个是不是.和..目录，并且要保证每个inode没有在同一个目录被link两次。

#### 7.3 Journaling

借鉴了DBMS的write-ahead logging的方法来改进FS的一致性，将恢复时间由O(size-of-disk-volumn)降低到O(size-of-the-log)，ext3、ext4、XFS、JFS、NTFS等FS都用了这种方法。

可以分为两种：metadata journaling和full mode journaling。后者在更新磁盘区域时，会提前将所有新数据写到journal区域；而前者在FS journal区域只存储inode、bitmap等metadata，不存user data，因为节省bandwidth，更为常用。

##### 7.3.1 full mode journaling 

**大概需要三步：**

1. Journal write: 在journal区域以一个TxB(Transaction Begin)标志开始讲需要journal的data、metadata写入。
2. Journal commit: 在日志写好后写一个TxE(Transaction End)标志表示日志写结束了。
3. Checkpoint: Checkpoint过程就是真正更新磁盘的过程。
4. Free: 过一段时间后，需要更新journal的superblock，mark这次事务为free

如下图：

[[p3_009.png]]

**两个问题：**

1. 其中为了将a)和b)两次IO合成一次减少性能开销，可以在TxB和TxE中都写一下日志的校验和(checksum)，这样恢复的时候就可以根据TxB的checksum和已经存储的检验日志的完整性了，这个方法是被作者的团队提出的，现在被用于 **ext4** 中。
2. journal的区域是一定的，不能无限增长，所以采用了类似环形链表的数据结构存储log，只需要存储开始块和结束块的指针就可以了。

##### 7.3.2. metadata journaling 


**User Data 和 Journal的提交顺序：**

metadata journaling中，根据user data写盘的顺序，又可以分为ordered journaling和non-ordered journaling，前者保证先写user data到磁盘，再写metadata到日志，最后写metadata到磁盘；后者的区别不保证user data和metadata的顺序性，实际这不会造成什么问题。所以NTFS、XFS等FS都采用了non-ordered metadata journaling的方式保证一致性。

**大概分为五步**

1. Data write
2. Journal metadata write
3. Journal commit
4. Checkpoint metadata
5. Free

这里，只是将journal的内容减少了user data。在ordered mode中，data要先写完再开始下一步；在non-ordered mode中，data write和其他步顺序无关，异步进行。如图，complete顺序和具体运行有关：

[[p3_010.png]]

#### 7.4 其他方法

除了1)fsck、2)journaling，还可以用其他的方法保证一致性。比如3)Soft Update[1][2]，4)copy-on-write(COW)被用于ZFS，5)backpointer-based consistency(BBC)，等等。

---

[1] M. Dong and H. Chen, “Soft Updates Made Simple and Fast on Non-volatile Memory,” Atc, 2017.

[2] M. McKusick and G. Ganger, “Soft updates: a technique for eliminating most synchronous writes in the fast filesystem,” ATEC ’99 Proc. Annu. Conf. USENIX Annu. Tech. Conf., 1999.


## 第八节 LFS(log-structured filesystem)

What does “level of indirection” mean in David Wheeler's aphorism?
, https://stackoverflow.com/questions/18003544/what-does-level-of-indirection-mean-in-david-wheelers-aphorism

## 第九节 数据完整性和数据保护

## 第十~十二节 分布式系统简介、NFS和AFS

介绍了分布式系统很复杂，系统各部分的错误是无法消除的，需要使用各种手段保证系统正常运行。

分布式系统的问题包括性能、安全、通信等问题，本节主要谈通信问题。首先，通信本身就是不可靠的，在网络传输中，丢包不可避免。TCP能保证传输可靠性，但性能牺牲太大，UDP只提供了简单的checksum机制，需要分布式系统自己保证传输的可靠。比如，作者较详细地介绍了RPC(详见原文)，其一般为了保证性能，用UDP而不用TCP。

作者在下两节分别介绍了NFS和AFS两种分布式文件系统。

#### 10.1 Sun's Network File System(NFS)协议

NFS由SUN公司开发，并没有被实现为一种特定的系统，而是指定了一种开方的协议（open protocol）。现在最新为v4版，作者重点介绍NFSv2。

首先，NFSv2被实现为一种无状态协议(stateless protocol)，即每个客户端的单个操作都包含着完成请求所需的所有信息。其次，它应该兼容POSIX，来方便用户和应用使用。

NFSv2的关键概念是 **file handle** 。它包括3部分：volume identifier、inode number和generation number。volume ID用于指定请求的是哪个server，inode number指明了是哪个文件，而generation number用于重复使用一个inode number使对请求进行区分。协议如图：

[[p3_011.png]]


#### 10.2 The Andrew File System(AFS)协议

AFS用的不多了，其特色思路已经被最新的NFSv4引入，人们大多用NFS和CIFS等代替它。作者重点是讲其思路。AFS最初由CMU开发，版本1(ITC)和版本2之间有较大变革。

与NFS不同，AFS是以文件为单位进行下载和更新的，而NFS是以块为单位的。

AFSv1的协议如下：


[[p3_012.png]]


#### 10.3 NFS和AFS

两者性能对比表如下：

[[p3_013.png]]