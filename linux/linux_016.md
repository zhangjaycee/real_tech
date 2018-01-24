# Stackable Block Layer

### 1. 定义

Linux的IO栈中有一块可选的部分，可以我称为Stackable Block Layer：

```bash
# Linux IO stack
Userspace >> VFS >> (Stackable Block Layer) >> Block Layer >> Block Drivers >> Storage Hardware
                                                    v
                                     (IO Scheduler / Block Multi-queue)
```

这部分包括 **MD(multiple device)** 、 **DM(device mapper)** 等。

LVM、Bcache、软RAID等都基于这层实现。其中LVM基于DM[1]。

---
[1] What is the difference between dm and md in Linux kernel?, https://stackoverflow.com/questions/23164384/what-is-the-difference-between-dm-and-md-in-linux-kernel

### 2. LVM

LVM是DM(device mapper)内核模块在用户空间的管理工具。这也体现了OS中策略(policy)和机制(mechanism)的分工。



### 3. Bcache

* 利用Bcache，可以将SSD作HDD的缓存

在内核中。一种块层的缓存。比如可以用来将ssd作为hdd的缓存。

* ZFS也可以有类似的功能

ZFS的L2ARC机制也可以利用不同硬件存储不同热度的数据，相当于用块设备给慢设备作缓存。

---
[1] https://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)

[2] Bcache, https://bcache.evilpiepirate.org/

[3] (在Centos7 上编译bcache), Bcache, CentOS 7.1 (w/kernel >= 3.10), http://10sa.com/sql_stories/?p=1052

[4] Add SSD as cache to ZFS on Linux, http://serverascode.com/2014/07/03/add-ssd-cache-zfs.html