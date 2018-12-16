# DMA 和 RDMA

## 1. DMA[1]

首先DMA是一种概念而非一种标准，没有一种标准规定DMA传输如何工作。

### 1.1 历史

随着发展，DMA从独立转为每个设备有自身的DMA engine，但是driver的职责不变，它们都要负责DMA传送的初始化。

* 第三方DMA

DMA 开始被发明时是一种独立于CPU与IO设备的DMA控制器，比如Intel 8237，它是1981年发明的，这种DMA被称为"第三方DMA"。这种第三方DMA在外围扩展IO设备和内存、CPU公用一条总线的时代，和Industrial Standard Architecture (ISA) Bus以ISA bridge与CPU bus分离的时代都存在。

* 第一方DMA

后来1992年开始的PCI Bus支持bus mastering，某个时刻只有成为bus master的外设可以与内存通信。与之前不同，没有一个专门的DMA控制器了，支持DMA的设备要有自己的DMA engine。

2004年PCIe接口出现，同时支持多个设备全双工DMA。

### 1.2 DMA流程

1. 确定src和dst内存地址。
2. driver编程硬件，让硬件开始进行DMA传输。PCI/PCIe设备的初始化各不相同，因为每个DMA engine都是设备自己的。而传统的DMA控制器则是相同的流程。：
    1. 首先，DMA engine被用src和dst地址编程；
    2. 设备被发出信号开始DMA传输；
    3. 通常设备会对CPU发interrupt说明已经传输完成。
    4. driver 中的interrupt handler会处理中断。

中断有开销，因此interrupt coalescing可以在一定程度上减少开销。interrupt coalescing时，多个中断被积攒到device中，只要一定的时间后才一起发到CPU。

---

[1] https://geidav.wordpress.com/2014/04/27/an-overview-of-direct-memory-access/

## 2. RDMA

RDMA 即 remote direct memory access。
