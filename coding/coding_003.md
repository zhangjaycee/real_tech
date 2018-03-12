# 在存储系统中应用数据压缩技术

## Intel SSD硬件层

---
[1] Differences Between Intel® SSD Controllers—Data Compression, https://www.intel.com/content/www/us/en/support/articles/000006433/memory-and-storage.html

## 块层



## 文件系统层

ZFS、NTFS、BtrFS、[e2compr](http://e2compr.sourceforge.net/)、[FuseCompress](https://code.google.com/archive/p/fusecompress/)等

其中fusecompress是对整个文件进行的压缩/解压缩，所以只对归档存储比较适合，对于数据库等频繁读写大文件的场合显然不适用。

* 一些参考

> [在启用压缩的 ZFS 上运行 PostgreSQL]https://www.oschina.net/translate/running-postgresql-on-compression-enabled-zfs

## 应用层

* 数据库应用

  - MySQL的Table Compression Format 和 Transparent Page Compression