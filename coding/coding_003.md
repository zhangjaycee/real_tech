# 在存储系统中应用数据压缩技术


## 块层

## 文件系统层

ZFS、NTFS、Btrfs、[e2compr](http://e2compr.sourceforge.net/)、[fusecompress](https://code.google.com/archive/p/fusecompress/)等

其中fusecompress是对整个文件进行的压缩/解压缩，所以只对归档存储比较适合，对于数据库等频繁读写大文件的场合显然不适用。

## 应用层

* 数据库应用

  - MySQL的Table Compression Format 和 Transparent Page Compression