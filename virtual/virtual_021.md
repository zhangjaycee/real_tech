# 硬件辅助的虚拟化

# Intel VT(Virtualization Technology)

### CPU虚拟化VT-x 

VT-x 即 Virtualization Technology for x86



---

[1] QEMU KVM VCPU internal, http://blog.allenx.org/2015/03/19/qemu-kvm-vcpu-internal

### 内存虚拟化EPT

EPT 即Extended Page Table.

内存虚拟化的任务是地址空间的转换。在虚拟机的虚拟化中，需要两次地址转换：

```
Guest Virtual Address(GVA) 
    --> Guest Physical Address(GPA) 
        --> Host Physical Address(HPA)
```
原本的硬件只支持一次转换，所以为了将`GVA->GPA->HPA`压缩成一次`GVA->HPA`，需要软件实现的 **“影子页表”（shadow page table）** ，但是这种方式开发维护和调试都很复杂。EPT同样也存在对应的TLB，EPT一种支持两次地址转换的硬件技术。为了提高TLB效率，VT-x还引入了Virtual Processor ID(VPID)，减少不必要的TLB擦除的同时区分不同的进程，来增加内存虚拟化的性能。


### IO虚拟化VT-d

VT-d 即Virtualization Technology for Direct I/O)

VT-d的核心是DMA remap技术，可以将设备对主机内存的访问限制在一定的内存区域（如guest分配的内存）。

* VT-d和SR-IOV的关系？

* VT-d和virtio的关系？



----------

##### 参考： 《系统虚拟化：原理与实现》