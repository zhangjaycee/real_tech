# SR-IOV

* 一种全称为Single Root I/O virtualization的I/O虚拟化标准。

* 一种定义[2]
> SR-IOV 技术是一种基于硬件的虚拟化解决方案，可提高性能和可伸缩性。SR-IOV 标准允许在虚拟机之间高效共享 PCIe（Peripheral Component Interconnect Express，快速外设组件互连）设备，并且它是在硬件中实现的，可以获得能够与本机性能媲美的 I/O 性能。SR-IOV 规范定义了新的标准，根据该标准，创建的新设备可允许将虚拟机直接连接到 I/O 设备。
>
> SR-IOV 规范由 PCI-SIG 在 http://www.pcisig.com 上进行定义和维护。

* 可以看成是将物理设备直接分配给VM的一种方式，是一种不同于全虚拟化模拟I/O(如QEMU模拟ide设备)和半虚拟化I/O(如KVM/QEMU的virtio-blk设备)的第三种I/O虚拟化方式，并且不同于PCIe passthrough的方式(Intel CPU相应的技术称为VT-d)，这种标准允许一个设备直接分配给多个VM[3]。

* [1]中的论文中提到了一种利用这种标准

## 参考

[1] X. Song, J. Yang, and H. Chen, “Architecting Flash-based Solid-State Drive for High-performance I/O Virtualization,” IEEE Comput. Archit. Lett., vol. 13, no. 2, pp. 61–64, 2014.

[2] SR-IOV 简介, http://docs.oracle.com/cd/E38902_01/html/E38873/glbzi.html

[3] KVM 介绍（4）：I/O 设备直接分配和 SR-IOV [KVM PCI/PCIe Pass-Through SR-IOV], http://www.cnblogs.com/sammyliu/p/4548194.html