# 关于系统性能监控和测试的工具

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


## iometer


## iozone
> 参考：

> http://junlee.blog.51cto.com/228061/508940

## Phoronix Test Suite

## vmstat
> http://www.cnblogs.com/ggjucheng/archive/2012/01/05/2312625.html

---

### 参考：
[1] Stefan Hajnoczi, Common disk benchmarking mistakes, http://blog.vmsplice.net/2017/11/common-disk-benchmarking-mistakes.html