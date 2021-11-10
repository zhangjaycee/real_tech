# QEMU的存储栈


## 1. QEMU在虚拟化存储栈扮演的角色

对于基于全虚拟化的、以文件块存储设备，Guest OS的块设备驱动像在物理机上一样运行着；而Guest的物理块设备磁盘，很可能只是Host上的一个(镜像)文件，QEMU会“委托”Host OS的文件系统管理这个镜像文件。

怎么让Guest上的系统把一个文件看成一个物理磁盘呢？QEMU就起一个中间处理人的作用，对上层Guest模拟一个物理设备，将上层的请求转换为对下层Host文件系统的文件级操作。

## 2. 分层

存储IO栈的层次本来就很多，QEMU这一层本来就是虚拟化中存储栈的一小层，但是光它自己最少又可以分成三层：分别被称为设备模拟层(Device Emulation)、格式驱动层(Format Driver)和协议驱动层(Protocol Driver)。大概的层次关系见下图：

```
                      +------------------+    e.g. virtio-blk / nvme / ide
Frontend Devices +--> | Device Emulation |
                      +---------+--------+    srcs in: QEMU_SRC/hw/block/*
                                |                     QEMU_SRC/hw/ide/*
                                |
                                |
                   +-   +-------+-------+    e.g. qcow2 / raw
                   |    | Format Driver |
                   |    +-------+-------+    srcs in: QEMU_SRC/block/*                   
                   |            |
Backend Drivers  +-+            |
                   |   +--------+--------+   e.g. file-posix / file-win32 / nbd
                   |   | Protocol Driver |
                   +-  +-----------------+   srcs in: QEMU_SRC/block/*

```
通俗来讲：

1. **设备模拟层**主要决定你的镜像文件在GuestOS看起来是什么设备并决定对应的存储传输协议。比如QEMU可以把这个文件模拟成一个IDE硬盘、一个virtio-blk设备或者一个NVMe设备等，这也分别对应了IDE、virtio和NVMe的存储协议。

2. **格式驱动层**对应了你的镜像文件格式，这个一般最开始就是由`qemu-img`工具创建好的，比如你用了qcow2格式或者raw格式等。这些可以实现存储虚拟化的功能，比如raw格式是镜像文件和虚拟磁盘线性映射的关系，而qcow2可以维护自己的映射表在格式驱动层实现qemu的存储虚拟化特性(如快照、thin-provision、base image等)。

3. **协议驱动层**就是对应你用了什么作为你的存储后端，一般都是用本地的一个文件，其实还可以是远程的块设备nbd等，当这里用文件作为存储后端时，由于要和Host的操作系统不同(Linux或者Win)，文件操作也是不同的，所以这也要分为两个协议驱动。

举个例子，现在QEMU中，既有`hw/block/nvme.c`，又有`block/nvme.c`，根据上述规则，前者是模拟一个NVMe设备，是“设备模拟层”，这样虚拟机中就可以用原生NVMe驱动了；后者是一个VFIO实现的用户态NVMe驱动，用于驱动host的NVMe设备，和file-posix后端平级，是“协议驱动层”。


## 3. QEMU镜像文件的cache mode

[[virtual_002_p2.png|height=512px]]

### 3.1.QEMU的5种cache mode参数及实现方式
      
QEMU虚拟磁盘的的参数 "cache=XXX" 有5种，如下表，其实在实现时对应三个QEMU内部标志：

|| BDRV_REQ_FUA | BDRV_O_NOCACHE | BDRV_O_NO_FLUSH |
|--------|--------|--------|-------|
|writeback|❌|❌|❌|
|writethrough|❌|✅|❌|
|none|✅|❌|❌|
|directsync|✅|✅|❌|
|unsafe|❌|❌|✅|

**writethrough** 对应的`O_NOCACHE`的实现方式是在open()中加入`O_DIRECT`参数。

**none** 对应的`BDRV_REQ_FUA`会调用bdrv注册的`bdrv_co_flush`函数，进而调用bdrv注册的`bdrv_co_flush_to_os`(刷qemu自身的元数据cache，如qcow2 lookup table)和`bdrv_co_flush_to_disk`函数(把数据真正刷到磁盘，如file-posix的fsync或fdatasync)。

**writeback** 是则是利用了host page cache，并且不会在每次写操作后进行sync操作。

**directsync** 出现的原因是`O_DIRECT`并不能绝对保证数据从硬件设备里的buffer持久化到了硬件设备的存储介质上，而fsync通常可以通过相应的flush IO指令达到目的，所以结合writethrough和none模式有时是有必要的(比如guest从不会下发flush IO的指令)。

> Recall that the storage may itself store the data in a write-back cache, so fsync() is still required for files opened with O_DIRECT in order to save the data to stable storage. The O_DIRECT flag is only relevant for the system I/O API. [7]

**unsafe** 对应`BDRV_O_NO_FLUSH`标志，会忽略guest传下来的刷盘指令，所以是“不安全”的。

更多解释还可参考[2-4][6]。

### 3.2 (相关解释) read/write-through 和 read/write-back[5]

（CPU和块设备缓存思想是类似的）

> 所谓的read/write cache的hit/miss，指的是CPU要read/write某一位址的资料，若此时cache里的资料刚好是该位址的资料，则称为cache hit，若此时cache里的资料不是该位址的资料，则称为cache miss。

> 当cache hit时，若CPU要读取某一位址的资料时，会直接从cache中读取资料。

> 当cache miss时，若CPU要读取某一位址的资料时，又可分为二种方式：一种是read through，这种方式会直接将资料从主记忆体端读进CPU；另一种是no read through，这种方式会先将资料从主记忆体端读进cache，然后再从cache读进CPU。

> 当cache hit时，若CPU要写入资料到某一位址时，可分为二种方式：一种是write through，此种方式资料会立刻写到cache及主记忆体中；另一种是write back ，此种方式会先将资料写入cache中，然后再将同一位址的资料整批一起写入主记忆体中（非立即写入）。

> 当cache miss时，若CPU要写入资料到某一位址时，可分为二种方式：一种是no write allocate，此种方式会直接将资料写到主记忆体中，不会再从记忆体中载入到cache，另一种方式是write allocate，此种方式会先将资料从主记忆体中载入到cache，然后再依cache hit的规则，将资料写出。
---

### 参考：
[1] KVM性能测试报告, http://openskill.cn/article/88

[2] 理解 QEMU/KVM 和 Ceph（1）：QEMU-KVM 和 Ceph RBD 的 缓存机制总结, http://www.cnblogs.com/sammyliu/p/5066895.html

[3] SUSE Doc, Description of Cache Modes, https://www.suse.com/documentation/sles11/book_kvm/data/sect1_1_chapter_book_kvm.html

[4] qemu-kvm磁盘读写的缓冲(cache)的五种模式, http://www.cnblogs.com/jusonalien/p/4772618.html

[5] 有關Cache的read/write through/back/allocate的意義, http://dannynote.blogspot.com/2007/04/cachereadwrite-throughbackallocate.html

[6] Disk Cache Modes, https://doc.opensuse.org/documentation/leap/virtualization/html/book.virt/cha.cachemodes.html

[7] Ensuring data reaches disk, https://lwn.net/Articles/457667/

