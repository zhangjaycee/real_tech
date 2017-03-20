# 关于virtio

> 
1. [概述](#概述)
2. [前端驱动分析](#前端驱动分析)
3. [后端设备分析](#后端设备分析)
4. [相关资料](#相关资料)


### 概述

对于qemu/kvm虚拟机来说，用不用virtio，决定了我们的虚拟化是半虚拟化还是全虚拟化。

决定虚拟机是半虚拟还是全虚拟的性质转变的标准只有一个：Guest机知不知道自己是一个虚拟机。具体来说，不使用virtio，虚拟机会像在真实物理环境下运行一样地运行——它不认为它是虚拟机；而使用virtio，就是让两部分virtio程序的互相通信，这两部分程序分别是前端驱动(frontend, Guest中)和后端设备(backend, Host中)，这样因为Guest中有了virtio的frontend部分，所以它的运行和物理机环境下有了区别，Guest按照一个使用virtio的虚拟机的方式运行——它知道了它是一个虚拟机。

virtio提高了io效率，（？也为host和guest间更复杂的合作机制实现提供了便利）



### 前端驱动分析（Linux Kernel）

> [virtio-blk浅析](http://www.2cto.com/os/201408/329744.html)

> [Virtio：针对 Linux 的 I/O 虚拟化框架](https://www.ibm.com/developerworks/cn/linux/l-virtio/)

> [Virtio 原理与Guest OS driver](http://blog.csdn.net/wanthelping/article/details/47069429)

> [virtio-blk请求发起](http://blog.csdn.net/LPSTC123/article/details/44983707)

> [The multiqueue block layer](https://lwn.net/Articles/552904/)

> [Linux Multi-Queue Block IO Queueing Mechanism (blk-mq)](https://www.thomas-krenn.com/en/wiki/Linux_Multi-Queue_Block_IO_Queueing_Mechanism_(blk-mq))

> [ KVM+QEMU世界中的pci总线与virtio总线 ](http://blog.chinaunix.net/uid-23769728-id-4467752.html)

前端驱动已经并到Linux内核主线了，所以要去内核找相关代码分析。

* linux 内核与virtio、virtio-blk相关的文件与目录结构：

```

include/uapi/linux
	├── virtio_blk.h
	└── virtio_ring.h

include/linux
	├── virtio.h
	├── virtio_byteorder.h
	├── virtio_caif.h
	├── virtio_config.h
	├── virtio_console.h
	├── virtio_mmio.h
	└── virtio_ring.h

drivers/block/virtio_blk.c

drivers/virtio/
	├── Kconfig
	├── Makefile
	├── config.c
	├── virtio.c
	├── virtio_balloon.c
	├── virtio_input.c
	├── virtio_mmio.c
	├── virtio_pci_common.c
	├── virtio_pci_common.h
	├── virtio_pci_legacy.c
	├── virtio_pci_modern.c
	└── virtio_ring.c

drivers/vhost/
	├── Kconfig
	├── Makefile
	├── net.c
	├── scsi.c
	├── test.c
	├── test.h
	├── vhost.c
	├── vhost.h
	└── vringh.c

```

### 后端设备分析（QEMU）


> [virtio-blk后端处理-请求接收、解析、提交
](http://blog.csdn.net/LPSTC123/article/details/45171515)

> [Qemu-kvm的ioeventfd创建与触发的大致流程](http://blog.csdn.net/LPSTC123/article/details/45111949)

后端设备已经在QEMU实现，所以要分析的代码在QEMU中。

* qemu中与virtio、virtio-blk相关的文件与目录结构：

```
hw/block/dataplane/virtio-blk.c
hw/block/dataplane/virtio-blk.h
hw/block/virtio-blk.c
hw/virtio/virtio.c
include/hw/virtio
include/hw/virtio/virtio-blk.h
include/hw/virtio/virtio.h
include/standard-headers/linux/virtio_blk.h
include/standard-headers/linux/virtio_ring.h
```


### 相关资料

> [paper] [virtio: Towards a De-Facto Standard For Virtual I/O Devices](http://www.ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)

> [(KVM连载)5.1.1 VIRTIO概述和基本原理（KVM半虚拟化驱动）](http://smilejay.com/2012/11/virtio-overview/)

> [Virtio 基本概念和设备操作] (http://www.ibm.com/developerworks/cn/linux/1402_caobb_virtio/)

> [Virtio：针对 Linux 的 I/O 虚拟化框架](https://www.ibm.com/developerworks/cn/linux/l-virtio/)

> [[Linux KVM]半虚拟化驱动（Paravirtualization Driver）](https://godleon.github.io/blog/2016/08/20/KVM-Paravirtualization-Drivers)

> [Virtio-Blk性能加速方案](http://royluo.org/2014/08/31/virtio-blk-improvement/)

> [Centos6下Virtio-SCSI(multi-queues)/Virtio-SCSI/Virtio-blk性能对比](http://blog.csdn.net/bobpen/article/details/41515119)

> [QEMU-KVM I/O性能优化之Virtio-blk-data-plane](http://blog.sina.com.cn/s/blog_9c835df30102vpgd.html)

> [read 系统调用剖析](https://www.ibm.com/developerworks/cn/linux/l-cn-read/)
