# 关于系统IO测量的工具

## sysbench

> [github源码]https://github.com/akopytov/sysbench

> https://www.percona.com/docs/wiki/benchmark_sysbench_oltp.html

*

sysbench 分为三个阶段 prepare run cleanup，在run之后会打印出测试结果。Ubuntu 16.04下，apt会安装0.4版本的sysbench，其他版本需要手动编译。

* 测试OLTP需要注意：

1. 对于默认情况下安装的mysql，如果需要用sysbench测得oltp数据，需要指明用户名、密码（否则无法登陆）和用于测试的数据库（sysbench默认的sbtest数据库在mysql并未默认创建）。

2. prepare时`sysbench --max-requests=2000 --test=oltp --mysql-user=root --mysql-password=1234 --oltp-table-size=10000000 prepare`就可以成功创建10000000个records，但是`sysbench --max-requests=2000 --test=oltp --mysql-user=root --oltp-table-size=10000000 --mysql-password=1234  prepare`一个record也不会创建，只是创建了table，可能是因为--oltp-table-size选项不可以夹在mysql账号和密码之间。。。

3. 0.4版本是ubuntu apt会安装的版本，但是从0.5开始，sysbench才支持多表测试，需要从github下载源码编译安装。


如果用默认的sbtest作为测试数据库，应该写：
```bash
mysql -u root -p
(mysql) create database sbtest;
```


## iometer


## iozone
> 参考：

> http://junlee.blog.51cto.com/228061/508940

## Phoronix Test Suite