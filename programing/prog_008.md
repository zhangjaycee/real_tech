# what is coroutine?

> [Coroutine及其实现] http://www.cnblogs.com/foxmailed/p/3509359.html

> [怎么理解coroutine ？] https://www.zhihu.com/question/21483863

> [coroutines in qemu] http://blog.vmsplice.net/2014/01/coroutines-in-qemu-basics.html

> [Qemu中的协程] http://royluo.org/2016/06/24/qemu-coroutine/

> [Coroutine(协程) 介绍] http://mathslinux.org/?p=234


## 综述

Coroutine(协程)可以理解为用户态实现的线程，线程比进程轻量化，所以协程的特点也是轻量化、并且协程间的切换是由用户态程序操控的，不用内核参与调度。

Python中yield产生的迭代器和协程的切换cpu控制权和重新进入函数的机制很类似。

Qemu中的广泛应用了coroutine机制。


## 协程、线程、进程的区别
进程是资源分配的最小单元（地址空间等），线程是cpu调度的最小单元，而协程是用户态程序实现的任务切换机制，具体表现为可重入。


