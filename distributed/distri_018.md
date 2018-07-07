# 设备I/O模型 (驱动层(polling/interrupt-based IO, DMA, MMIO, PMIO ...)、块层和应用层)

### 1. 驱动层的IO通信

IO设备的驱动程序为上层屏蔽了以下这些实际的IO指令和数据传输细节，所以以下分类时比较偏底层驱动的IO模式。

#### 基于polling/interrupt的IO和DMA

根据memory和device之间数据传输的模式，IO可以分为3种：**programmed IO (PIO)**、**interrupt-handling IO**和**direct memory access(DMA)**：

1. 前两种在数据传输时，都需要进行device<->CPU register<->memory的操作，区别在于等待设备就绪状态的方法：基于①**polling**的方法占用CPU不断检查设备是否准备好，准备好后马上开始传输；而基于②**interrupt**的方法在CPU向设备发送IO指令之后，处理器切换到其他任务，当设备准备好要传输的数据时，由设备发出中断信号，然后CPU和device才开始传输数据。

2. 第三种③**DMA**则不同，只需要CPU往设备发送IO指令和相关的信息，就可以去做别的了数据的传输方式是device<->DMA<->memory，这里DMA卸载了CPU的任务，减少了CPU占用。DMA模块可以是系统总线中一个独立模块，也可以并入到IO模块中。


#### PMIO和MMIO

根据CPU和device通信的模式，IO(一说是programmed IO)可以分为**port-mapped IO(PMIO)** 和 **memory-mapped IO(MMIO)** 两类，他们的区别主要是CPU把设备看成内存还是IO外设，或者说CPU是否认为内存和IO是统一的地址空间：
1. **memory-mapped IO**则指的是将设备的某些空间映射到系统的内存地址空间，这样CPU可以像访问内存一样用LOAD/STORE等形式与设备通信；
2. **port-mapped IO**指的是外部IO设备的地址空间和内存地址空间相互独立，CPU通过某些IO口用IN/OUT等指令和设备通信。

---

[1] 浅谈内存映射I/O(MMIO)与端口映射I/O(PMIO)的区别, https://www.cnblogs.com/idorax/p/7691334.html

[2] wikipedia- Memory-mapped I/O, https://en.wikipedia.org/wiki/Memory-mapped_I/O

[3] OSTEP, http://pages.cs.wisc.edu/~remzi/OSTEP/


### 2. 块层和应用层中polling和interrupt IO的思想

#### Userspace polling:

poll / epoll / select are all userspace polling. Originally, they are usually referred in context of network programming.

but now, **epoll can be used with libaio.** [5]

#### Kernel polling of blk-mq for file I/O:

In kernel, polling is only supported in NVMe driver or block layer's blk-mq. And the corresponding user space system call are preadv2 / pwritev2 with a flag RWF_HIPRI.[1][2]

Facebook uses polling and NVMe SSDs to optimize their MyRocks database [3].

FIO also support polling IO engine. (pvsync2) [4]

---
[1] The return of preadv2()/pwritev2(), https://lwn.net/Articles/670231/

[2] Block-layer I/O polling, https://lwn.net/Articles/663879/

[3] A. Eisenman et al., “[DRAM+Optane]Reducing DRAM Footprint with NVM in Facebook,” EuroSys ’18, 2018. 

[4] https://fio.readthedocs.io/en/latest/fio_doc.html

[5] https://github.com/littledan/linux-aio#use-with-epoll