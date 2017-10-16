# SSD的结构

## 读写原理

一块SSD中可以包含多个NAND Flash chips(packages)，一个SSD中的多个chip(package)可以组成多组channel，这些channel并联接入controller。

每个chip中可能有多个die，一个die一个时间只能执行一个command，是执行command的最小单位。一个die还可以有多个由多个block组成的plane，一个die中的多个plane在可以并行处理相似的指令。

每个die分为多个block，每个block又分为多个page。读时，可以读任意的page；写时，如果对应的page已经被写过，需要对page所在的整个block进行擦除，然后再写。这样还会导致块内不需要修改的page需要被迁移，因此如果写操作导致了block的重新擦除，会增加额外的读、写和擦除时间。

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

## 参考
[1] Understanding Flash: Blocks, Pages and Program / Erases, https://flashdba.com/2014/06/20/understanding-flash-blocks-pages-and-program-erases/

[2] CSAPP

[3] NAND Flash存储器与SSD简介, http://blog.sina.com.cn/s/blog_679f935601011nt1.html

[4] Log-structured file systems: There's one in every SSD, https://lwn.net/Articles/353411/

