# 内存虚拟化

### 操作系统的内存虚拟化

首先，操作系统负责将有限的内存资源动态地分配给多个进程，这种概念可以称得上一种虚拟化。

这种内存虚拟化实现的核心在于不同的进程有各自的虚拟地址空间(address space)，地址空间里的地址称为虚拟地址VA，并由操作系统和硬件将其转化为物理地址PA。

[1][2]中讲的比较好。

(待续。。。)

---
[1] https://blog.csdn.net/ipmux/article/details/19167605

[2] https://www.mnstory.net/2016/06/30/qemu-hugepages/

### 虚拟机的内存虚拟化

涉及到mmu的虚拟化，也就是虚拟内存地址和物理内存地址的转换。

mmu虚拟化分为软件虚拟化和硬件虚拟化。软件对应影子页表；硬件对应Intel的EPT(Extent Page Table)技术和AMD的NPT(Nest Page Table)技术。

### 参考：

https://www.ibm.com/developerworks/cn/linux/l-cn-kvm-mem/
https://events.linuxfoundation.org/slides/2011/linuxcon-japan/lcj2011_guangrong.pdf

https://blog.csdn.net/xelatex_kvm/article/details/17679529
http://blog.vmsplice.net/2016/01/qemu-internals-how-guest-physical-ram.html