# SSD作HDD的缓存(Bcache / ZFS / Fusion-io ...)

## Bcache

在内核中。一种块层的缓存。比如可以用来将ssd作为hdd的缓存。

[1] Bcache, https://bcache.evilpiepirate.org/

[2] (在Centos7 上编译bcache), Bcache, CentOS 7.1 (w/kernel >= 3.10), http://10sa.com/sql_stories/?p=1052


## ZFS

ZFS的L2ARC机制可以利用不同硬件存储不同热度的数据，相当于用块设备给慢设备作缓存。