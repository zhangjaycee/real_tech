# Page fault

## 1. Linux的缺页

page fault:

内存page有三种状态：[1]
```
(1) unmapped: if the program has not written to the memory region since requesting its allocation, then it is by definition filled with all-zeroes. The Operating System does not have to store it at all, since it knows it’s just filled with zero bytes. Thus the OS will just mark the page as ‘unmapped’ until the program actually writes to it. Thus, on most Operating Systems, when you allocate “memory”, the OS will give you an address range but won’t actually map it to physical storage (yet).

(2) resident: the page corresponds to a page in RAM.

(3) swapped: the page corresponds to a page that has been swapped to disk.
```
访问一个页时，应在状态(2)。

状态(1)会引起minor page fault，这时虽然被分配了，但是进程还没有读写过对应的线性区(memory region)，所以读写时会产生一次minor page fault。

状态(3)会引起major page fault，需要磁盘IO来恢复页。

---
[1] https://frogatto.com/2009/10/30/what-every-programmer-should-know-about-memory-management/

## 2. KVM(EPT)的缺页


## 3. userfaultfd

即用户空间的page fault handler。

要使用此功能，首先应该用userfaultfd调用来创建一个fd，然后用ioctl来配置这个fd，比如可能需要用ioctl-userfaultfd支持的UFFDIO_API、UFFDIO_REGISTER等进行设置。

* 文档

关于userfaultfd系统调用及例子见[1]，关于ioctl设置选项ioctl_userfaultfd见[2]。

---
[1] http://man7.org/linux/man-pages/man2/userfaultfd.2.html

[2] http://man7.org/linux/man-pages/man2/ioctl_userfaultfd.2.html

[3] Caldwell, Blake, et al. "FluidMem: Memory as a Service for the Datacenter." arXiv preprint arXiv:1707.07780 (2017). (https://arxiv.org/pdf/1707.07780.pdf)

[4] The next steps for userfaultfd(), https://lwn.net/Articles/718198/
