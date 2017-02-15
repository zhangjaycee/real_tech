# 关于virtio

> https://wiki.archlinux.org/index.php/QEMU#Installing_virtio_drivers

> [paper] [virtio: Towards a De-Facto Standard For Virtual I/O Devices](http://www.ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)

> [Virtio基本原理(KVM半虚拟化驱动)](https://my.oschina.net/davehe/blog/130124)

> [(KVM连载)5.1.1 VIRTIO概述和基本原理（KVM半虚拟化驱动）](http://smilejay.com/2012/11/virtio-overview/)

> [Virtio 基本概念和设备操作](http://www.ibm.com/developerworks/cn/linux/1402_caobb_virtio/)

> [Virtio：针对 Linux 的 I/O 虚拟化框架](https://www.ibm.com/developerworks/cn/linux/l-virtio/)

> [[Linux KVM]半虚拟化驱动（Paravirtualization Driver）](https://godleon.github.io/blog/2016/08/20/KVM-Paravirtualization-Drivers)

对于qemu/kvm虚拟机来说，用不用virtio，决定了我们的虚拟化是半虚拟化还是全虚拟化。

决定虚拟机是半虚拟还是全虚拟的性质转变的标准只有一个：Guest机知不知道自己是一个虚拟机。具体来说，不使用virtio，虚拟机会像在真实物理环境下运行一样地运行————它不认为它是虚拟机；而使用virtio，就是让两部分virtio程序的互相通信，这两部分程序分别是前端驱动(frontend, Guest中)和后端设备(backend, Host中)，这样因为Guest中有了virtio的frontend部分，所以它的运行和物理机环境下有了区别，Guest按照一个使用virtio的虚拟机的方式运行————它知道了它是一个虚拟机。

virtio提高了io效率，（？也为host和guest间更复杂的合作机制实现提供了便利）