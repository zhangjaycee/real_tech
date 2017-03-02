# 关于系统IO测量的工具

## sysbench

> [github源码]https://github.com/akopytov/sysbench

*

sysbench 分为三个阶段 prepare run cleanup，在run之后会打印出测试结果。Ubuntu 16.04下，apt会安装0.4版本的sysbench，其他版本需要手动编译。

* 测试OLTP需要注意：

对于默认情况下安装的mysql，如果需要用sysbench测得oltp数据，需要指明用户名、密码（否则无法登陆）和用于测试的数据库（sysbench默认的sbtest数据库在mysql并未默认创建）。

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