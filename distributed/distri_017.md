# 文件系统中的原子性

## 文件的原子操作

#### 文件偏移的原子性 [1][3]

* `O_APPEND` 可以保证多个进程同时追加一个文件的原子性。

* `pread`和`pwrite`可以保证读写某个位置的两个步骤（偏移和读写）的原子性。

* `O_CREAT`和`O_EXCL`可以保证用`open`打开失败时创建文件时两个操作（尝试打开和创建文件）的原子性。


#### 多线程同时write会造成的文件乱掉吗[2]

---
[1] APUE P62

[2] http://www.man7.org/tlpi/errata/index.html

[3] Is lock-free logging safe? https://www.jstorimer.com/blogs/workingwithcode/7982047-is-lock-free-logging-safe

## 记录锁

---
[1] APUE p391
