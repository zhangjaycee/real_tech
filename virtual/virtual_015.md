# KVM内存虚拟化

涉及到mmu的虚拟化，也就是虚拟内存地址和物理内存地址的转换。

mmu虚拟化分为软件虚拟化和硬件虚拟化。软件对应影子页表；硬件对应Intel的EPT(Extent Page Table)技术和AMD的NPT(Nest Page Table)技术。

### 参考：

https://www.ibm.com/developerworks/cn/linux/l-cn-kvm-mem/
https://events.linuxfoundation.org/slides/2011/linuxcon-japan/lcj2011_guangrong.pdf