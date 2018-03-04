# DRAM内存作存储(ramdisk/ramfs/tmpfs)

首先，ramdisk / ramfs / tmpfs / memcached /radis 这几种内存作为存储（缓存）的方法，数据都是掉电就丢的，这也是由DRAM的特性决定的。

其次，我们可以把ramdisk / ramfs / tmpfs 看做一类，它们是本地的方案；可以吧memcached /radis 看做一类，它们是分布式的多机缓存方案。

在本地的方案中，可以把ramdisk看做一类，它是对块设备的模拟，要使用的话也需要像块设备一样在上边建文件系统。可以把ramfs / tmpfs看做一类，它们在文件系统层实现，像page cache一样工作，区别是tmpfs可以限制大小，可以用df、du查看使用情况，可以使用swap区；而ramfs只能用free来估算，且可能因过量使用导致内存占满影响系统稳定性。

### tmpfs

以一个2GB的tmpfs为例

```
mount -t tmpfs -o size=2G tmpfs /TMPFS
```

### ramdisk

#### 在centos上使用一个ram disk

Step 1. 加载内核模块`brd`来创建一个ramdisk
```
# 创建连1个2GB的内存盘，最大分区数为4。
modprobe brd rd_nr=1 rd_size=2048000 max_part=4
```
Step 2. 用fdisk进行分区（可选），然后在相应分区上格式化新的文件系统，并挂载
```
# 分区，在fdisk中按提示操作即可
fdisk /dev/ram0
# 格式化文件系统，以ext4为例
mkfs.ext4 /dev/ram0p1
# mkdir /RAMDISK
mount /dev/ram0p1 /RAMDISK
```
Step 3. 然后就可以正常用了。。。
Step 4. 销毁ramdisk
```
# 接触挂载
umount /dev/ram0p1
# 卸载内核模块
modprobe -r brd
```

---
### 参考：
[1] The Difference Between a tmpfs and ramfs RAM Disk, https://www.jamescoyle.net/knowledge/951-the-difference-between-a-tmpfs-and-ramfs-ram-disk

[2] Create a RAM disk in Linux, https://www.jamescoyle.net/how-to/943-create-a-ram-disk-in-linux

[3] centos7下做内存盘的方法, http://www.zphj1987.com/2016/01/14/centos7下做内存盘的方法/