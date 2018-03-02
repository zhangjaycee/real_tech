# Persistent Memory

称为NVM容易有歧义，因为有人说NVM的时候可能指的是NVMe，有人指的是Persistent Memory。

在我理解PM应该除了掉电不丢数据，应该更接近DRAM而不是传统的块设备，即应该是DIMM接口，可字节寻址的。


### 一些资料

Persistent Memory Programming这个项目[1]，专注于PM编程，做了工具叫PMDK，专门用于PM编程。PMDK开发基于DAX[4][5]。


SNIA提出了NVM编程的标准(NVM Programming Model, NPM)[2]，在其开头，明确区分了"NVM-block"和PM的区别，并将模型分为四类，具体见原文。

[6]是威斯康星大学一个关于PM编程的一个讲座的ppt和相关的paper。


### 一个相关会议

Persistent Memory Summit。[3]

---

[1] Persistent Memory Programming, http://pmem.io/

[2] SNIA, NVM Programming Model, https://www.snia.org/sites/default/files/technical_work/final/NVMProgrammingModel_v1.2.pdf

[3] Persistent Memory Summit 2018, https://www.snia.org/pm-summit

[4] (Kernel Doc) DAX, https://www.kernel.org/doc/Documentation/filesystems/dax.txt

[5] DAX, mmap(), and a "go faster" flag, https://lwn.net/Articles/684828/

[6] Programming and Usage Models for Non-Volatile Memory, http://research.cs.wisc.edu/sonar/tutorial/