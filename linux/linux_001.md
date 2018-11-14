# Linux进程管理

## 查看进程状态：
```bash
cat /proc/[PID]/status
```
其中`VmPTE`可以看页表大小[1]。

---
[1] https://ewx.livejournal.com/579283.html

## 前台/后台执行进程

> 参考

> http://www.cnblogs.com/kaituorensheng/p/3980334.html

* &

在命令后加`&`可以实现后台执行，但是退出执行终端会终止进程。

* nohup

在命令前写`nohup`可以使程序脱离终端中断信号而在后台执行，这时关闭终端不会终止程序。

* fg

`fg %`后接进程的作业编号，或者`fg`后接pid可以把后台程序调到前台，编号可以通过`jobs`命令查询。

* bg

`bg %`后接进程的作业编号，或者`bg`后接pid可以使暂停在后台的进程继续执行，任务编号和任务状态可以用`jobs`命令查询。


## Linux下如何杀掉一个进程

参考[1], 常用的两种：

```bash
# 方法1
killall -9 [prog_name]
# 方法2
ps -ef|grep [prog_name] ;
kill -9 [pid]
```

---

[1] 《linux下杀死进程的10种方法》, http://mrcelite.blog.51cto.com/2977858/1350392