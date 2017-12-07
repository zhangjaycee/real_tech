# 磁盘IO监控工具(blktrace(btrace) / iostat)
## blktrace
blktrace有内核支持。(`KERNEL_SRCS/kernel/trace/blktrace.c`)

blktrace使用的是ftrace的blk这个tracer[3] ？

统计各个逻辑CPU下某个盘和每个盘总共的I/O次数和时间。

开始追踪时，会在debugfs下创建逻辑cpu个数个文件，记录相关内容。


## btrace

Java有个测试工具叫btrace；用于追踪IO的工具blktrace有个简化版命令也是btrace，这两个不是一个东西。

由于blktrace产生的trace数据需要一个叫blkparse的工具进行格式化解析，不是很方便，btrace属于blktrace自带的一个简单的对自身封装，就是相当于一些blktrace和blkparse的常用组合。

以下摘自Man Page： 

* DESCRIPTION

The btrace script provides a quick and easy way to do live tracing of block devices. It calls blktrace on the specified devices and pipes the output through blkparse for formatting. See blktrace (8) for more in-depth information about how blktrace works.
* EXAMPLE

Simply running
```
btrace /dev/sda
```
 will show a trace of the device /dev/sda.

## iostat


`iostat -xt`也可以追踪很多io信息，但是blktrace / btrace可以给出一个设备每个CPU的请求情况，更详细。

centos下的安装：

```bash
yum -y install sysstat
```




## 参考

[1] Block I/O Layer Tracing: blktrace, https://www.mimuw.edu.pl/~lichota/09-10/Optymalizacja-open-source/Materialy/10%20-%20Dysk/gelato_ICE06apr_blktrace_brunelle_hp.pdf

[2] http://blog.csdn.net/hs794502825/article/details/8545133

[3] Kernel Tracing with Ftrace, https://blog.selectel.com/kernel-tracing-ftrace/