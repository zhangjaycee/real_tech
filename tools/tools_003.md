# 系统测试工具

## lmbench
可以测试上下文切换的时间。

## sysbench

> [github源码]https://github.com/akopytov/sysbench

> https://www.percona.com/docs/wiki/benchmark_sysbench_oltp.html

> http://blog.csdn.net/zqtsx/article/details/42775393

* sysbench 分为三个阶段 prepare run cleanup，在run之后会打印出测试结果。Ubuntu 16.04下，apt会安装0.4版本的sysbench，其他版本需要手动编译。

#### 编译方法：
```
#sysbench-0.5为例
unzip sysbench-0.5.zip
./autogen.sh
./configure --prefix=/PATH/TO/INSTALL --with-mysql-includes=/PATH/TO/MYSQL/include --with-mysql-libs=/PATH/TO/MYSQL/lib
make 
make install
```


## fio
* Centos 安装：

源码编译或者：
```
yum install epel-release
yum install fio
```
* ioengin:

```
sync：Basic read(2) or write(2) I/O. fseek(2) is used to position the I/O location.
psync：Basic pread(2) or pwrite(2) I/O.
vsync: Basic readv(2) or writev(2) I/O. Will emulate queuing by coalescing adjacents IOs into a single submission.
libaio: Linux native asynchronous I/O.
posixaio: glibc POSIX asynchronous I/O using aio_read(3) and aio_write(3).
mmap: File is memory mapped with mmap(2) and data copied using memcpy(3).
splice： splice(2) is used to transfer the data and vmsplice(2) to transfer data from user-space to the kernel.
syslet-rw： Use the syslet system calls to make regular read/write asynchronous.
sg：SCSI generic sg v3 I/O.
net ： Transfer over the network. filename must be set appropriately to `host/port’ regardless of data direction. If receiving,
only the port argument is used.
netsplice： Like net, but uses splice(2) and vmsplice(2) to map data and send/receive.
guasi The GUASI I/O engine is the Generic Userspace Asynchronous Syscall Interface approach to asycnronous I/O.
```
* clat & slat:

> copy from: http://tate.cx/using-fio-to-measure-io-performance/
>
>The first latency metric is submission latency (slat), “how long did it take to submit this IO to the kernel for processing?”.
>
>Next is completion latency (clat), “the time that passes between submission to the kernel and when the IO is complete, not including submission latency”.


---

[1] 使用fio进行I/O性能测试, http://debugo.com/fio-test/

## stress

这个是产生压力的，不是测试的。安装方法：

ubuntu:
```
apt install stree
```
centos:
```
yum install epel-release
yum install stress
```

具体可以看man手册，可以产生多种进程数，指定每个进程malloc的内存等。--vm-keep N 还可以保证malloc的内存保持多少时间再free，N为0时为一直不free。

## iometer


## iozone
> 参考：

> http://junlee.blog.51cto.com/228061/508940

## Phoronix Test Suite

## vmstat
> http://www.cnblogs.com/ggjucheng/archive/2012/01/05/2312625.html

---

## IO测试中需要注意的问题


### 参考：
[1] Stefan Hajnoczi, Common disk benchmarking mistakes, http://blog.vmsplice.net/2017/11/common-disk-benchmarking-mistakes.html