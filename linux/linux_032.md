# 共享内存(shm...)进行进程间通信(IPC)


System V shared memory (shmget / shmat / shmdt) 和 POSIX shared memory (shm_open / shm_unlink)是Linux支持的两套共享内存IPC的接口。

这两套接口内核底层都是用tmpfs实现的，与tmpfs有关的内核选项`CONFIG_TMPFS`开启与否只影响用户空间部分的tmpfs特性，并不会改变两套共享内存IPC的内核实现。


* 关于tmpfs在两套实现中的用途: 

> [1]
>(1) 用于SYSV共享内存，还有匿名内存映射；这部分由内核管理，用户不可见；
>
>(2) 用于POSIX共享内存，由用户负责mount，而且一般mount到/dev/shm；依赖于CONFIG_TMPFS;

这在两套接口也可看出，
```cpp
int shm_open(const char *name, int oflag, mode_t mode);
int shmget(key_t key, size_t size, int shmflg);
```
`shm_open`要求用户指定一个以"/"开头的name，并且name尽量不要再有"/"，所创建的共享内存文件在 `/dev/shm` 目录下保存。而shmget的空间用户是不可见的。

POSIX和Sys V两套接口最大限制分别由`/dev/shm` mount时的限定大小和`/proc/sys/kernel/shmmax`参数分别决定，两者互不影响。例[1]：
```bash
# 调整Sys V接口共享内存的大小限制到65 MB：
echo 68157440 > /proc/sys/kernel/shmmax
# 调整POSIX接口共享内存tmpfs到64 MB:
mount -size=64M -o remount /dev/shm
```

从[1]的实验，还可以发现POSIX接口的tmpfs /dev/shm 目录中，可以创建大于文件系统size的文件，但是写超过size的文件区间时会发生SIGBUS，感觉类似mmap的范围大于file size时会发生的一样。[2]

---
[1] 浅析Linux的共享内存与tmpfs文件系统， http://blog.chinaunix.net/uid-28541347-id-5763124.html

[2] 用mmap接口访问文件时边界问题会导致的两个错误, http://blog.jcix.top/2018-10-26/mmap_tests/