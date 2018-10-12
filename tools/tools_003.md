
# A. 性能测试工具

## 1. 测文件/磁盘IO

IO测试中需要注意的问题可以参考[4]。

### 1.1. iometer

### 1.2. iozone [1]

### 1.3. fio [2]

* Centos 安装：

源码编译或者用包管理器安装(CentOS 为例)：
```
yum install epel-release
yum install fio
```
* ioengine:

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
* 结果中的clat, slat, lat指什么？[3]

> The first latency metric is submission latency (slat), “how long did it take to submit this IO to the kernel for processing?”.
>
> Next is completion latency (clat), “the time that passes between submission to the kernel and when the IO is complete, not including submission latency”.

---
[1] http://junlee.blog.51cto.com/228061/508940

[2] 使用fio进行I/O性能测试, http://debugo.com/fio-test/

[3] http://tate.cx/using-fio-to-measure-io-performance/

[4] Stefan Hajnoczi, Common disk benchmarking mistakes, http://blog.vmsplice.net/2017/11/common-disk-benchmarking-mistakes.html

## 2. 数据库测试

### 2.1. sysbench OLTP测试

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

### 2.2. TPC-C测试

---

[1] https://github.com/akopytov/sysbench

[2] https://www.percona.com/docs/wiki/benchmark_sysbench_oltp.html

[3] http://blog.csdn.net/zqtsx/article/details/42775393


## 3. 其他工具

### 3.1. Phoronix Test Suite

全面的系统性能benchmark。

### 3.2. lmbench
可以测试上下文切换的时间。

### 3.3. stress

这个是产生压力的，不是测试的。stress-ng这个工具是stress的升级版，可以指定CPU负载的百分比。安装方法：

ubuntu:
```
apt install stress
apt install stress-ng

```
centos:
```
yum install epel-release
yum install stress
yum install stress-ng
```

具体可以看man手册，可以产生多种进程数，指定每个进程malloc的内存等。--vm-keep N 还可以保证malloc的内存保持多少时间再free，N为0时为一直不free。

一个用stress-ng在第一个核产生90%负载的例子：
~~~shell
taskset 0x0001 stress-ng --cpu 1 --cpu-load 90 --cpu-load-slice 10
~~~



# B. 性能分析工具

## 1. 状态监测

### 1.1. 系统状态监视 (top / htop / iotop)

### 1.2. 系统状态检查 (iostat / vmstat)

### 1.3. 应用运行状态 (pstack / gdb)

## 2. 追踪测量

### 2.1. 内核级 ftrace

### 2.2. 系统调用级 strace

### 2.2. 应用级 perf

