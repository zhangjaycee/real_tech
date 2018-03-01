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

### IO虚拟化VT-d

VT-d 即Virtualization Technology for Direct I/O)