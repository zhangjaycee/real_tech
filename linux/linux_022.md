# DRAM内存作存储(ramdisk/ramfs/tmpfs/memcached/radis)

首先，ramdisk / ramfs / tmpfs / memcached /radis 这几种内存作为存储（缓存）的方法，数据都是掉电就丢的，这也是由DRAM的特性决定的。

其次，我们可以把ramdisk / ramfs / tmpfs 看做一类，它们是本地的方案；可以吧memcached /radis 看做一类，它们是分布式的多机缓存方案。

在本地的方案中，可以把ramdisk看做一类，它是对块设备的模拟，要使用的话也需要像块设备一样在上边建文件系统。可以把ramfs / tmpfs看做一类，它们在文件系统层实现，像page cache一样工作，区别是tmpfs可以限制大小，可以用df、du查看使用情况，可以使用swap区；而ramfs只能用free来估算，且可能因过量使用导致内存占满影响系统稳定性。

### tmpfs



### ramdisk





---
### 参考：
[1] centos7下做内存盘的方法, http://www.zphj1987.com/2016/01/14/centos7下做内存盘的方法/