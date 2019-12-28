# IOMMU / vIOMMU / VT-d


## 什么是IOMMU

IOMMU同MMU一样用作地址转换，区别是MMU负责进程(CPU)虚拟地址(VA)和物理地址(PA)的转换，而IOMMU负责设备(IO devices)虚拟地址(IOVA)和物理地址之间的转换。Intel的IOMMU技术也称作VT-d。


## VFIO和IOMMU什么关系

VFIO这个词经常和IOMMU出现在一起是因为VFIO这个框架支持IOMMU，而它的前辈UIO框架不支持IOMMU。UIO和VFIO都是支持将设备暴露给userspace的，有了这种技术，我们就可以实现用户态的驱动，或者也可以用运行于用户态的qemu将一个IO设备assign到一个VM。VFIO通过支持IOMMU，让这种到userspace的设备暴露更安全了。

## 什么是vIOMMU

虽然利用VFIO，QEMU支持将设备绑定到一个VM。但是这还是不够安全，于是有了vIOMMU[2][3]和硬件加速的二级VT-d Scalable IO virtualization(类似于EPT之于普通页表)[4][5]。

to be continued ...


---
[1] https://lwn.net/Articles/805870/

[2] https://wiki.qemu.org/Features/VT-d

[3] Amit, Nadav, Muli Ben-Yehuda, and Ben-Ami Yassour. "IOMMU: Strategies for mitigating the IOTLB bottleneck." In International Symposium on Computer Architecture, pp. 256-274. Springer, Berlin, Heidelberg, 2010.

[4] https://lkml.org/lkml/2019/9/23/297

[5] https://phoronix.com/scan.php?page=news_item&px=Intel-VT-d-Scalable-Mode