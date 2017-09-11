# SR-IOV


## 定义[1][2]

* 一种全称为Single Root I/O virtualization的I/O虚拟化标准。在硬件中实现

* SR-IOV 规范由 PCI-SIG 在 http://www.pcisig.com 上进行定义和维护[2]。


## 分析

* 可以看成是将物理设备直接分配给VM的一种方式，是一种不同于全虚拟化模拟I/O(如QEMU模拟ide设备)和半虚拟化I/O(如KVM/QEMU的virtio-blk设备)的第三种I/O虚拟化方式，并且不同于PCIe passthrough的方式(Intel CPU相应的技术称为VT-d)，这种标准允许一个设备直接分配给多个VM[3]。

* 论文[1]中提到了一种利用这种标准来优化虚拟机SSD设备性能的方法。

## 优缺点(摘自[3])

|优势	|不足    |
|-------|-------|
|真正实现设备共享(多个客户机共享一个 SR-IOV 设备的物理端口)|对设备有依赖，目前只有部分设备支持 SR-IOV。RedHat Linux 只是测试了 Intel 的几款高端网卡。|
|接近原生性能|使用 SR-IOV 时不方便动态迁移客户机。 这是因为这时候虚机直接使用主机上的物理设备，因此虚机的迁移（migiration）和保存（save）目前都不支持。这个在将来有可能被改变。|
|相比 VT-d， SR-IOV 可以使用更少的设备来支持更多的客户机，可以提高数据中心的空间利用率。||


## 参考

[1] X. Song, J. Yang, and H. Chen, “Architecting Flash-based Solid-State Drive for High-performance I/O Virtualization,” IEEE Comput. Archit. Lett., vol. 13, no. 2, pp. 61–64, 2014.

[2] SR-IOV 简介, http://docs.oracle.com/cd/E38902_01/html/E38873/glbzi.html

[3] KVM 介绍（4）：I/O 设备直接分配和 SR-IOV [KVM PCI/PCIe Pass-Through SR-IOV], http://www.cnblogs.com/sammyliu/p/4548194.html