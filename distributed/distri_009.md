# raw flash 和 Open-channel SSD 

## 1. 硬件层

### 1.1 raw flash

raw flash所有的管理由host进行，通过mtd, ubi等抽象层进行操作或管理。[1]中写了raw flash和FTL-based devices(SSD)的区别，SSD在设备的控制器中实现了这些抽象，将设备内的flash memory抽象成对于上层的block device。

### 1.2. Open-channel SSD

Open-channel的概念最初由百度的SDF(software-defined flash)提出[2]，用FPGA作为控制器，这样上层app可以分开控制各个flash unit (LUN)。

M. Bjørling推广了这个概念[3]，不像百度一样由应用负责部分flash的管理，而是对linux系统的存储栈进行扩展，并同硬件厂商推动相关标准的制定。

Fast 17 中专门有一个分区(包括3篇paper)讲了相关的研究:
```
LightNVM: The Linux Open-Channel SSD Subsystem
FlashBlox: Achieving Both Performance Isolation and Uniform Lifetime for Virtualized SSDs
DIDACache: A Deep Integration of Device and Application for Flash based Key-value Caching
```
其中写LightNVM的作者正是Bjørling（他13年的SYSTOR还写了blk-mq linux块层multi-queue调度器(Linux Block IO: Introducing Multi-queue SSD Access on Multi-core Systems)更多关于blk-mq在本wiki中也有写到：[[blk-mq 相关|linux_015]]。

### 1.3. raw flash 和 open-channel SSD区别?

MTD用来解决raw flash的驱动问题，而open-channel SSD硬件内部有控制器，不需要MTD。使用open-channel SSD时，host主要通过lightNVM等[4]来管理数据放置位置、IO调度策略和垃圾回收GC，而其他的任务，如管理上百个flash芯片、提供电源管理等交给硬件控制器管理。正如Bjørling在[5]中的回复所说：

> MTD solves the problem of directly driving raw flash. Whereas Open-Channel SSDs have flash controllers embedded in hardware, that takes care of scheduling, driving hundred of flash chips, and provide power capacitors for durability. The host primarily handles data placement, I/O scheduling, and garbage collection and leaves everything else to the SSD controller. Making it more efficient for >1M IOPS devices.

---
[1] Raw flash vs. FTL devices http://www.linux-mtd.infradead.org/doc/ubifs.html#L_raw_vs_ftl

[2] Jian Ouyang, Shiding Lin, S Jiang, and Z Hou. SDF: Software-defined flash for web-scale internet storage systems. In Proceedings of the 19th international conference on Architectural support for programming languages and operating systems, 2014.

[3] M. Bjørling, “Operating System Support for High-Performance Solid State Drives.”

[4] Support for Open-Channel SSDs (was dm-lightnvm), https://lwn.net/Articles/615341/

[5] Taking control of SSDs with LightNVM, https://lwn.net/Articles/641247/
  
## 2. 软件管理层

## 2.1 MTD/UBI

 MTD(memory technology devices)和UBI(unsorted block images)这两个抽象层是用于管理raw flash的subsystem。比如，有两个文件系统分别建立在这两个抽象层之上，JFFS2是基于MTD的FS，UBIFS是基于UBI的FS。UBI建立在MTD之上，MTD建立在raw flash之上。[1]

其中，MTD提供了访问raw flash的统一接口(系统中为/dev/mtdX)，UBI是对flash device的磨损平衡管理和镜像管理，UBI在MTD之上，UBI卷(UBI volumes)比MTD devices层次更高，负责解决MTD devices存在的磨损均衡、坏块等问题。

## 2.2 lightNVM

lightNVM是用于管理open-channel SSD的子系统[2][3]。To be continue...

---

[1] http://www.linux-mtd.infradead.org/doc/ubifs.html

[2] M. Bjørling, C. Labs, J. Gonzalez, F. March, and S. Clara, “LightNVM: The Linux Open-Channel SSD Subsystem,” 15th USENIX Conf. File Storage Technol. (FAST 17), 2017.

[3] Support for Open-Channel SSDs (was dm-lightnvm), https://lwn.net/Articles/615341/
