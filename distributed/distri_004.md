# SSD的结构和特性

## 读写原理

一块SSD中可以包含多个NAND Flash chips(packages)，一个SSD中的多个chip(package)可以组成多组channel，这些channel并联接入controller。

每个chip中可能有多个die，一个die一个时间只能执行一个command，是执行command的最小单位。一个die还可以有多个由多个block组成的plane，一个die中的多个plane在可以并行处理相似的指令。

每个die分为多个block，每个block又分为多个page。读时，可以读任意的page；写时，如果对应的page已经被写过，需要对page所在的整个block进行擦除，然后再写。（**导致写入放大**）这样还会导致块内不需要修改的page需要被迁移，因此如果写操作导致了block的重新擦除，会增加额外的读、写和擦除时间。

## 为什么SSD快

每个SSD内都有多个Flash芯片，单独一个Flash芯片并没有那么快的吞吐量，但是如果它们间是存在并行读写，那就快了。这个感觉类似RAID磁盘阵列的思路，只不过这里可以想象成flash chips组成的阵列。

而且，在SSD的发展趋势来看，NAND-flash的特征尺寸是减小的，一个package中的dies是增加的


## 擦写导致的寿命(lifetime)问题

典型的页读、 写和擦除的延时约为25微秒、200微秒和1500微秒。典型的擦除次数限于10K到100K之间。

比较便宜的MLC/TLC甚至只有低至几百次的擦除寿命。

## 地址翻译(FTL)

FTL是flash translation layer的缩写，即闪存翻译层。

FTL主要负责将暴露给上层的逻辑块地址，翻译为实际的物理块地址。这样做的一个主要原因就是FTL中的平均磨损逻辑(wear leveling)试图将擦除操作平均分配给所有块，来尽可能长的延长SSD使用寿命。

## Read Disturb

对于一个page读的次数多了，可能对同一个block的其他page造成影响，使其数据0/1发生变化，所以应该记录读的次数，对读的次数多的block进行擦除和重新写入操作。[2]

## GC、TRIM、Discard

GC是垃圾回收的意思。TRIM是一个SSD指令，需要软件（文件系统、RAID）等配合支持TRIM指令的SSD进行。TRIM在一些文件系统配置时的参数叫做DISCARD。

> [6]
> (Filesystem Recommendations)
>
> IMPORTANT: Do not discard blocks in filesystem usage.
>
> Be sure to turn off the discard option when making your Linux filesystem. You want to allow the SSD manage blocks and its activity between the NVM (non-volatile memory) and host with more advanced and consistent approaches in the SSD Controller.
>
> Core Filesystems:
>
> • ext4 – the default extended option is not to discard blocks at filesystem make time, retain this, and do not
add the “discard” extended option as some information will tell you to do.
>
> • xfs – with mkfs.xfs, add the –K option so that you do not discard blocks.
>
> If you are going to use a software RAID, it is recommended to use a chunk size of 128k as starting point, depending
on the workload you are going to run. You must always test your workload.

意思是使用NVMe SSD和NVMe驱动时不要开启文件系统的discard。因为SSD控制器会有更好的方法做这些工作。

> [7] 而如果在这之前，SSD执行了GC操作，那么GC会把这些实际上已经删除了的数据还当作是有效数据进行迁移写入到其他的block中，这是没有必要的。TRIM和DISCARD的支持，不仅仅要SSD实现这个功能，而是整个数据链路中涉及到的文件系统、RAID控制卡以及SSD都需要实现。要使用这个功能必须要在mount文件系统时，加上discard选项。如果想要确认SSD是否支持，可以通过hdparm -I命令检查。

原文说，如果在Discard/TRIM之前，SSD进行了GC操作，无用数据就被进行了毫无必要的迁移，所以TRIM的软硬件支持能提高性能。

> [8] So, SSDs are fast at writing, but only when their free space is neatly trimmed. The only component in your software stack that knows which parts of your SSD should be trimmed, is your file system. That is why there is a file system option in ext4 (my current file system of choice), called “discard”. When this option is active, space that is freed up in the file system is reported to the SSD immediately, and then the SSD does the trimming right away. This will make the next write to that part of the SSD as fast as expected.

这里说，文件系统(如ext4)删除文件时，会通知SSD进行TRIM的，这样就会保持SSD的空闲空间是trimmed的，这样可以保持SSD较快的写入速度。

## 参考
[1] Understanding Flash: Blocks, Pages and Program / Erases, https://flashdba.com/2014/06/20/understanding-flash-blocks-pages-and-program-erases/

[2] SSD 101, https://www.cactus-tech.com/landing/ssd-101-ebook

[3] NAND Flash存储器与SSD简介, http://blog.sina.com.cn/s/blog_679f935601011nt1.html

[4] Log-structured file systems: There's one in every SSD, https://lwn.net/Articles/353411/

[5] CSAPP

[6] Intel Linux NVMe Driver, https://www.intel.com/content/dam/support/us/en/documents/ssdc/data-center-ssds/Intel_Linux_NVMe_Guide_330602-002.pdf

[7] SSD的工作原理、GC和TRIM、写入放大以及性能评测, http://blog.csdn.net/scaleqiao/article/details/50511279

[8] https://patrick-nagel.net/blog/archives/337