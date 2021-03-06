# 内核态和用户态

## 1. 用户态及内核态的关系

### 1.1 内核（驱动）模块

内核驱动模块运行在内核态，它在被装载时进行会运行init函数进行初始化和一些调用注册，然后类似事件驱动程序一样，被用户程序调用对应的一些“方法”，被卸载时，会运行对应的exit函数。

一般的驱动中的函数分两类任务，一些函数用于作为系统调用的一部分，当用户系统调用调用时，用户进程从用户态切换到内核态，并在内核态中最终调用到驱动的这些函数；另一些函数则负责中断处理。


### 1.2 内核线程kthreads

内核同样有线程的概念，称为kernel thread (kthread) 它们只在内核态运行，并且最开始都由kthreadd这个进程fork而来。

---

[1] LDD 第二章

[2] What is a Kernel thread? https://stackoverflow.com/questions/9481055/what-is-a-kernel-thread

## 2. 用户态及内核态的同步机制

和用户程序一样，内核编程时同样需要注意并发的同步问题。这正是因为可能有多个在多处理器运行的用户进程同时访问一个内核数据结构造成的。所以内核并发编程同样特别重要。下面是一些用户态与内核态进行同步（锁）的方法对比：

### 2.1 用户态：

1 **互斥量**

2 **读写锁**

3 **条件变量**

4 **自旋锁** 在用户空间并不常用，因为并不能保证用了pthread自旋锁不会休眠，当进程时间片到了，就可能会被OS休眠。其实互斥量mutex在userspace更常用，它通常会先自旋一小段时间再休眠，这样其实也是很高效的。 

5 **屏障**

### 2.2 内核态

1. **原子操作**

2A **自旋锁**
优点在于进程阻塞时没有休眠，虽然浪费CPU，但没有进程切换的开销，适合预期阻塞时间短的情况。通常用于底层来实现其他种类的锁。（如RCU）

2B **读写自旋锁**：首先它是自旋锁。读读不锁，读写和写写之间互斥。

3A **信号量**
信号量不同于自旋锁的地方在于，信号量允许进程休眠，而自旋锁不允许。

3B **读写信号量**：首先它是信号量。读读不锁，读写和写写之间互斥。内核中的相关函数是down_read / up_read / down_write / up_write。

4. **互斥量 Mutex**
5. **RCU(read-copy-update)**
读写和读读不锁，写写之间互斥。

7. 完成变量
8. 大内核锁
9. 顺序锁
10. 禁止抢占
11. 顺序和屏障


* 内核的自旋锁还是信号量如何选择？[3]
```
Spin locks VS. semaphores
(recommended)

• low overhead locking       ---> spinlock
• short lock hold time       ---> spinlock
• long lock hold time        ---> semaphore
• for interrupt context use  ---> spin lock
• sleep while holding lock   ---> semaphore
```

* 检测内核死锁的工具： lockdep

---

[1] APUE

[2] 《Linux内核设计与实现》读书笔记（十）- 内核同步方法, http://www.cnblogs.com/wang_yb/archive/2013/05/01/3052865.html

[3] http://staff.ustc.edu.cn/~james/em2005/5.pdf