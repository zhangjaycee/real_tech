# Persistent Memory

称为NVM容易有歧义，因为有人说NVM的时候可能指的是NVMe，有人指的是Persistent Memory。

在我理解PM应该除了掉电不丢数据，应该更接近DRAM而不是传统的块设备，即应该是DIMM接口，可字节寻址的。


### 1. DAX


#### 1.1 device-dax和filesytem-dax

通过ndctl工具(可以通过yum或编译安装)可以在device-dax(/dev/daxX)和filesystem-dax(/dev/pmemX)模式之间转换。两者的区别在于是否抽象成块设备+文件系统，device-dax可能带来更大自由度、更高性能和更低使用便捷性[1]。[7]中分析了ext4的fsync函数，其中涉及一些ext4的dax实现，写的很详细。

> [6]As an interim solution, Linux
provides Device-DAX [1], which allows an application to open a
persistent memory device (without a file system), memory map
it, and utilize userspace flushes to make stores persistent

另外，device DAX 不仅支持4 K的页大小，还支持 2 M的hugepage大小，可以减小TLB占用[8]。qemu 2.12也为其以file为backend的NVDIMM模拟硬件加入了`align`选项，方便将`/dev/daxX.X`设备的对齐设为2 M：

> [9] The align option specifies the base address alignment when QEMU mmap(2) mem-path, and accepts common suffixes, eg 2M. Some backend store specified by mem-path requires an alignment different than the default one used by QEMU, eg the device DAX /dev/dax0.0 requires 2M alignment rather than 4K. In such cases, users can specify the required alignment via this option.




#### 1.2 consistency

首先文件系统间的DAX是不一致的，ext4只能整个文件系统DAX或者不DAX，而XFS是基于inode的DAX，粒度更细。 [3]

ext4-dax和xfs-dax目前还只支持metadata-consistency,data-consistency不支持。[4]

有一个叫BTT的东西试图把64 B粒度转为512 B。[5]

[1] "Device DAX" for persistent memory, https://lwn.net/Articles/687489/, https://lists.gt.net/linux/kernel/2434768

[2] http://linux.hpe.com/nvdimm/LinuxSDKReadme.htm

[3] The future of DAX, https://lwn.net/Articles/717953/

[4] https://www.snia.org/sites/default/files/PM-Summit/2017/presentations/Swanson_steven_NOVA_Fastest_File_system_for_NVDIMMsv2.pdf

[5] https://lwn.net/Articles/686150/

[6] Persistent Memory Programming, https://www.usenix.org/system/files/login/articles/login_summer17_07_rudoff.pdf

[7] Linux fsync和fdatasync系统调用实现分析（Ext4文件系统）, https://blog.csdn.net/luckyapple1028/article/details/61413724

[8] https://nvdimm.wiki.kernel.org/2mib_fs_dax

[9] https://qemu.weilnetz.de/doc/qemu-doc.html

### 2. PMDK

#### 2.1 PMDK同时支持device-dax和filesytem-dax

以安装使用pmemkv为例[1]，两种模式都可以传递给pmemkv使用，性能可能不同（还没测试）。

#### 2.2 pmemkv 

基于PMDK的libpmemobj抽象实现，并提供了接入KV的接口，现支持b-tree和blackhole(接口例子，哑接口)。


#### 2.3 PMDK的consistency

> [2]Data allocated with PMDK is put to the virtual memory address space, and concrete ranges are relying on result of mmap(2) operation performed on the user defined files. Such files can exist on any storage media, however data consistency assurance embedded within PMDK requires frequent synchronisation of data that is being modified. Depending on platform capabilities, and underlying device where the files are, a different set of commands is used to facilitate synchronisation. It might be msync(2) for the regular hard drives, or combination of cache flushing instructions followed by memory fence instruction for the real persistent memory.

----

[1] Installing pmemkv, https://github.com/pmem/pmemkv/blob/master/INSTALLING.md#fedora_latest_pmdk

[2] https://pmem.io/2016/02/22/pm-emulation.html

### 3. BTT - Block Translation Table

可以看做是一层间接(a level of indirection)，将PM的IO粒度由cache line(64 Bytes)转换为扇区(512 Bytes)。

https://www.kernel.org/doc/Documentation/nvdimm/btt.txt

### A. 其他资料

Persistent Memory Programming这个项目[1]，专注于PM编程，做了工具叫PMDK，专门用于PM编程。PMDK开发基于DAX[4][5]。


SNIA提出了NVM编程的标准(NVM Programming Model, NPM)[2]，在其开头，明确区分了"NVM-block"和PM的区别，并将模型分为四类，具体见原文。

[6]是威斯康星大学一个关于PM编程的一个讲座的ppt和相关的paper。

[7]舒继武教授的一个演讲的ppt中涉及不少的讨论和paper。

* 一个相关会议： 

Persistent Memory Summit。[3]

* Intel：

Intel基于3D XPOINT技术，推出了NVMe接口的Optane SSD，还将推出DIMM接口的NVRAM(NVDIMM, NVM)。Intel的编程模型遵循SNIA的标准[2][9]。一些英特尔的视频、文档。[10]

---

[1] Persistent Memory Programming, http://pmem.io/

[2] SNIA, NVM Programming Model, https://www.snia.org/sites/default/files/technical_work/final/NVMProgrammingModel_v1.2.pdf

[3] Persistent Memory Summit 2018, https://www.snia.org/pm-summit

[4] (Kernel Doc) DAX, https://www.kernel.org/doc/Documentation/filesystems/dax.txt

[5] DAX, mmap(), and a "go faster" flag, https://lwn.net/Articles/684828/

[6] Programming and Usage Models for Non-Volatile Memory, http://research.cs.wisc.edu/sonar/tutorial/

[7] 舒继武 大数据时代的存储系统若干变化的思考, part1: http://myslide.cn/slides/6485   part2: http://myslide.cn/slides/6491

[8] 如何在英特尔® 架构服务器上仿真持久性内存, https://software.intel.com/zh-cn/articles/how-to-emulate-persistent-memory-on-an-intel-architecture-server

[9] https://software.intel.com/en-us/persistent-memory

[10] https://software.intel.com/en-us/persistent-memory/documentation