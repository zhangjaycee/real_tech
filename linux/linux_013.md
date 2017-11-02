# 扇区(磁盘块)大小、内核通用块层bio大小、文件系统块大小、VFS Page Cache页大小



## 磁盘块大小
一个物理磁盘一般一次最小的读写单元是512 Bytes(扇区)。这也是为什么`dd`命令默认ibs=512(最大的读入字节数)：
```
dd if=/dev/sda1 of=/dev/null count=1
记录了1+0 的读入
记录了1+0 的写出
512字节(512 B)已复制，0.000632521 秒，809 kB/秒
```

## 通用块层bio的大小


## 文件系统块大小

文件系统也有最小的读写单元，比如ext4默认为4kB，这个可以简单的测出来：
```
zjc@/SSD$ df .
文件系统           1K-块      已用    可用 已用% 挂载点
/dev/sdb1      206292968 188401120 7389704   97% /SSD
zjc@/SSD$ echo hello > hello
zjc@/SSD$ df .
文件系统           1K-块      已用    可用 已用% 挂载点
/dev/sdb1      206292968 188401124 7389700   97% /SSD
```
我只写了很少的内容(hello)到一个文件中，整个文件系统的可用空间便减少了4kB。

## 内存页

Linux Page Cache的页大小为4kB

## Linux一些IO的统计单位为1kB
> 
> ### Kernel block size
>Also the kernel has its own block size. This is relevant e.g. for vmstat. In the vmstat man page you find the statement
All linux blocks are currently 1024 bytes.
So, again another block size when you work with vmstat. This is the block size the Linux kernel uses internally for caching and buffering. It is the most prominent of all block sizes.



> http://wiki.linuxquestions.org/wiki/Block_devices_and_block_sizes
>
> http://sanwen.net/a/bsiyqqo.html
