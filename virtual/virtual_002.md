# 怎样理解Qemu/KVM的存储栈


## 1. Qemu扮演的角色



[[virtual_002_p3.png|height = 512px]]

Guest上的用户应用和OS kernel像在物理机上一样运行着；而Guest看来的物理磁盘，其实只是Host上的一个(镜像)文件，所以Host的OS就像管理一个普通文件一样管理这个镜像文件。

怎么让Guest上的系统把一个文件看成一个物理磁盘呢？Qemu就起一个中间处理人的作用，不好听地说，他骗了Guest的系统，把Guest认为的磁盘级操作都揽过去，全部转成了Host的文件级操作。


## 2. 分层

```
                        +---------------+    e.g. virtio-blk / nvme / ide
Frontend Devices  +-->  | Guest Devices |
                        +-------+-------+    srcs in: QEMU_SRC/hw/block/*
                                |                     QEMU_SRC/hw/ide/*
                                |
                                |
                   +-   +-------+-------+    e.g. qcow2 / raw
                   |    | Format Driver |
                   |    +---------------+    srcs in: QEMU_SRC/block/*
                   |
Backend Drivers  +-+            |
                   |   +--------+--------+   e.g. file-posix / file-win32 / nbd
                   |   | Protocol Driver |
                   +-  +-----------------+   srcs in: QEMU_SRC/block/*

```
存储IO栈的层次本来就很多，QEMU这一层本来就是虚拟化中存储栈的一小层，但是光它自己最少又可以分成三层：我把它们称为设备模拟层(Guest device)、格式驱动层(Format driver)和协议驱动层(Protocol driver)。大概的层次关系见上图。通俗来讲：

1. 设备模拟层主要决定你的镜像文件在GuestOS看起来是什么设备，比如QEMU可以把这个文件模拟成一个IDE硬盘、一个virtio-blk设备或者一个NVMe设备等；

2. 格式驱动层对应了你的镜像文件格式，这个一般最开始就是由`qemu-img`工具创建好的，比如你用了qcow2格式或者raw格式等；

3. 协议驱动层就是对应你用了什么作为你的存储后端，一般都是用本地的一个文件，其实还可以是远程的块设备nbd等，当这里用文件作为存储后端时，由于要和Host的操作系统不同(Linux或者Win)，文件操作也是不同的，所以这也要分为两个协议驱动。




## 3. QEMU镜像文件的cache mode


[[virtual_002_p2.png|height=512px]]

### 3.1.Qemu-KVM的5种cachemode


* cache mode unspecified

>In qemu-kvm versions older than v1.2 (eg SLES11 SP2), not specifying a cache mode meant that writethrough would be used as the default. Since that version, the various qemu-kvm guest storage interfaces have been fixed to handle writeback or writethrough semantics more correctly, allowing for the default caching mode to be switched to writeback. The guest driver for each of ide, scsi, and virtio have within their power to disable the write back cache, causing the caching mode used to revert to writethrough. The typical guest's storage drivers will maintain the default caching mode as writeback, however.


* cache = writethrough

>This mode causes qemu-kvm to interact with the disk image file or block device with O_DSYNC semantics, where writes are reported as completed only when the data has been committed to the storage device. The host page cache is used in what can be termed a writethrough caching mode. The guest's virtual storage adapter is informed that there is no writeback cache, so the guest would not need to send down flush commands to manage data integrity. The storage behaves as if there is a writethrough cache.

该模式对应的标志位是O_DSYNC，仅当数据被提交到了存储设备里面的时候，写操作才会被完整的通告。此时host的页缓存可以被用在一种被称为writethrough缓存的模式。guest的虚拟存储设备被告知没有回写缓存(writeback cache)，因此guest不需要为了操纵整块数据而发送刷新缓存的指令了。此时的存储功能如同有一个直写缓存(writethrough cache)一样。


* cache = writeback

>This mode causes qemu-kvm to interact with the disk image file or block device with neither O_DSYNC nor O_DIRECT semantics, so the host page cache is used and writes are reported to the guest as completed when placed in the host page cache, and the normal page cache management will handle commitment to the storage device. Additionally, the guest's virtual storage adapter is informed of the writeback cache, so the guest would be expected to send down flush commands as needed to manage data integrity. Analogous to a raid controller with RAM cache.

对应的标志位既不是 O_DSYNC 也不是 O_DIRECT ,在writeback模式下，IO操作会经过host的页缓冲，存放在host页缓冲里的写操作会完整地通知给guest.除此之外,guest的虚拟存贮适配器会被告知有回写缓存(writeback cache),所以为了能够整体地管理数据，guest将会发送刷新缓存的指令.类似于带有RAM缓存的磁盘阵列(RAID)管理器。

* cache = none

>This mode causes qemu-kvm to interact with the disk image file or block device with O_DIRECT semantics, so the host page cache is bypassed and I/O happens directly between the qemu-kvm userspace buffers and the storage device. Because the actual storage device may report a write as completed when placed in its write queue only, the guest's virtual storage adapter is informed that there is a writeback cache, so the guest would be expected to send down flush commands as needed to manage data integrity. Equivalent to direct access to your hosts' disk, performance wise.

所对应的标志位是O_DIRECT,在 none 模式下，VM的IO操作直接在qemu-kvm的userspace缓冲和存储设备之间进行，绕开了host的页缓冲。这个过程就相当于让vm直接访问了你的host的磁盘，从而性能得到了提升。

* cache = unsafe

>This mode is similar to the cache=writeback mode discussed above. The key aspect of this unsafe mode, is that all flush commands from the guests are ignored. Using this mode implies that the user has accepted the trade-off of performance over risk of data loss in the event of a host failure. Useful, for example, during guest install, but not for production workloads.

该模式与writeback差不多，不过从guest发出的刷新缓存指令将会被忽视掉，这意味着使用者将会以牺牲数据的完整性来换取性能的提升。

*cache=directsync

>This mode causes qemu-kvm to interact with the disk image file or block device with both O_DSYNC and O_DIRECT semantics, where writes are reported as completed only when the data has been committed to the storage device, and when it is also desirable to bypass the host page cache. Like cache=writethrough, it is helpful to guests that do not send flushes when needed. It was the last cache mode added, completing the possible combinations of caching and direct access semantics.

该模式所对应的标志位是O_DSYNC和O_DIRECT,仅当数据被提交到了存储设备的时候，写操作才会被完整地通告,并且可以放心地绕过host的页缓存。就像writethrough模式,有时候不发送刷新缓存的指令时很有用的.该模式是最新添加的一种cache模式，使得缓存与直接访问的结合成为了可能。

### 3.2.有关Cache

（CPU和块设备缓存思想是类似的）

> 所谓的read/write cache的hit/miss，指的是CPU要read/write某一位址的资料，若此时cache里的资料刚好是该位址的资料，则称为cache hit，若此时cache里的资料不是该位址的资料，则称为cache miss。

> 当cache hit时，若CPU要读取某一位址的资料时，会直接从cache中读取资料。

> 当cache miss时，若CPU要读取某一位址的资料时，又可分为二种方式：一种是read through，这种方式会直接将资料从主记忆体端读进CPU；另一种是no read through，这种方式会先将资料从主记忆体端读进cache，然后再从cache读进CPU。

> 当cache hit时，若CPU要写入资料到某一位址时，可分为二种方式：一种是write through，此种方式资料会立刻写到cache及主记忆体中；另一种是write back ，此种方式会先将资料写入cache中，然后再将同一位址的资料整批一起写入主记忆体中（非立即写入）。

> 当cache miss时，若CPU要写入资料到某一位址时，可分为二种方式：一种是no write allocate，此种方式会直接将资料写到主记忆体中，不会再从记忆体中载入到cache，另一种方式是write allocate，此种方式会先将资料从主记忆体中载入到cache，然后再依cache hit的规则，将资料写出。

### 3.3. Qemu中cache mode的实现方式

实际上，是在Qemu打开镜像文件的时候，改变open()的参数改变的。详见代码或者参考[1]。以下是三种常见cache mode的标志位。

| CacheMode | Open()Flag |特点|
|--------|--------|--------|
|Write through|O_DSYNC|QEMU默认/ 安全/ 但是IO性能差|
|Write back||用了两层Cache/ 不安全/ IO性能最好|
|None|O_DIRECT|绕过Host Cache层/ 安全/ 性能较好|

---

### 参考：
[1] KVM性能测试报告, http://openskill.cn/article/88

[2] 理解 QEMU/KVM 和 Ceph（1）：QEMU-KVM 和 Ceph RBD 的 缓存机制总结, http://www.cnblogs.com/sammyliu/p/5066895.html

[3] SUSE Doc, Description of Cache Modes, https://www.suse.com/documentation/sles11/book_kvm/data/sect1_1_chapter_book_kvm.html

[4] qemu-kvm磁盘读写的缓冲(cache)的五种模式, http://www.cnblogs.com/jusonalien/p/4772618.html

[5] 有關Cache的read/write through/back/allocate的意義, http://dannynote.blogspot.com/2007/04/cachereadwrite-throughbackallocate.html

