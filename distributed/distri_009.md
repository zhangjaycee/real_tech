# raw flash, FTL device (SSD) and Open-channel SSD 

## 1. raw flash

raw flash所有的管理由host进行，通过mtd, ubi等抽象层进行操作或管理。[1]中写了raw flash和FTL-based devices(SSD)的区别，SSD在设备的控制器中实现了这些抽象，将设备内的flash memory抽象成对于上层的block device。

### 1.1 MTD 和 UBI

JFFS2是基于MTD的FS，UBIFS是基于UBI的FS。

UBI建立在MTD之上，MTD建立在raw flash之上。

```
[2]UBIFS is a new flash file system developed by Nokia engineers with help of the University of Szeged. In a way, UBIFS may be considered as the next generation of the JFFS2 file-system.

JFFS2 file system works on top of MTD devices, but UBIFS works on top of UBI volumes and cannot operate on top of MTD devices. In other words, there are 3 subsystems involved:

MTD subsystem, which provides uniform interface to access flash chips. MTD provides an notion of MTD devices (e.g., /dev/mtd0) which basically represents raw flash;
UBI subsystem, which is a wear-leveling and volume management system for flash devices; UBI works on top of MTD devices and provides a notion of UBI volumes; UBI volumes are higher level entities than MTD devices and they are devoid of many unpleasant issues MTD devices have (e.g., wearing and bad blocks); see here for more information;
UBIFS file system, which works on top of UBI volumes.
```

---

[1] Raw flash vs. FTL devices http://www.linux-mtd.infradead.org/doc/ubifs.html#L_raw_vs_ftl

[2] http://www.linux-mtd.infradead.org/doc/ubifs.html

## 2. Open-channel SSD

Fast 17 中专门有一个分区(包括3篇paper)讲了相关的研究:

- LightNVM: The Linux Open-Channel SSD Subsystem

- FlashBlox: Achieving Both Performance Isolation and Uniform Lifetime for Virtualized SSDs

- DIDACache: A Deep Integration of Device and Application for Flash based Key-value Caching

[其中写LightNVM的作者Bjørling正是13年SYSTOR写了blk-mq linux块层multi-queue调度器的人，(Linux Block IO: Introducing Multi-queue SSD Access on Multi-core Systems)更多关于blk-mq在本wiki中也有写到：[[blk-mq 相关|linux_015]]]

**TO UPDATE:**

what is the difference between raw flash and open-channel SSD?

## 更多相关网页：

The multiqueue block layer, https://lwn.net/Articles/552904/

Support for Open-Channel SSDs (was dm-lightnvm), https://lwn.net/Articles/615341/

Taking control of SSDs with LightNVM, https://lwn.net/Articles/641247/
  