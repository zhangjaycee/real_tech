# Persistent Memory

称为NVM容易有歧义，因为有人说NVM的时候可能指的是NVMe，有人指的是Persistent Memory。

在我理解PM应该除了掉电不丢数据，应该更接近DRAM而不是传统的块设备，即应该是DIMM接口，可字节寻址的。




### 1. PMDK

#### 1.1 device-dax和filesytem-dax

通过ndctl工具(可以通过yum或编译安装)可以在device-dax(/dev/daxX)和filesystem-dax(/dev/pmemX)模式之间转换。两者的区别在于是否抽象成块设备+文件系统，device-dax可能带来更大自由度、更高性能和更低使用便捷性[1]。

以安装使用pmemkv为例[2]，两种模式都可以传递给pmemkv使用，性能可能不同（还没测试）。

#### 1.2 pmemkv 

基于PMDK的libpmemobj抽象实现，并提供了接入KV的接口，现支持b-tree和blackhole(接口例子，哑接口)。

----
[1] "Device DAX" for persistent memory, https://lwn.net/Articles/687489/

[2] Installing pmemkv, https://github.com/pmem/pmemkv/blob/master/INSTALLING.md#fedora_latest_pmdk

### 2. 其他资料

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