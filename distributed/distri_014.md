# 存储系统中的各种“写放大”(Write Amplification)

“写放大”(Write Amplification)在存储系统中是很常见的。但是，即使都是在存储系统中，“写放大”也有很多种，各种的写放大原理并不是很一样。下边根据自己的理解，进行了下总结，如有问题，恳请指正。

### 1. 读写单元较大导致的写放大

在文件系统中，读写单元固定，比如都是4K，这样，如果write函数写的数据小于4K，则要先把整块读入，再修改，再把新的4K整体写入（O_DIRECT情况除外）。这个过程可以称为 **RMW** (Read-Modify-Write)，这就是File System的写放大问题。[1][2][5] （注意：Read-Modify-Write被更广泛地用在[[原子指令|prog_018]][3]和RAID[4]中。）

再如，在DBMS等应用层存储系统中，同样存在自己管理的读写单元，如MySQL的默认读写单元称为页，默认是16KB，所以一次读写只能以页的单位进行，这时，小于页的数据读写同样会带来整页的读写，进而造成了“写放大”，道理和文件系统是一样的。

### 2. RAID中的Read-Modify-Write造成的写放大

如前段所述，RAID中更新一个块，需要额外读原始块、校验块，额外写校验块，所以多了两个读，一个写，也称为Read-Modify-Write[4]。 这是由于校验块必须更新，且根据与运算的可逆性，新校验块=新数据块^旧校验块^旧数据块。

### 3. SSD中闪存特性造成的写放大

在SSD中，一个block可以分为多个page，在读的时候，可以以page为单位，但是写的时候，只能以block为单位。因此写的单元比较大。在上层（比如文件系统）读写单元相同的情况下，同样是读写1个page的大小，读的话直接读就行，写的话却需要先把与要写page同一个block的数据全复制一遍，加上修改的page后，再一起写入block。写入的数据量远比实际的大，这就是SSD的写放大问题。

### 4. 存储系统一致性机制造成的同步写放大

在存储系统的很多层次中，都有保证系统crash consistency（一致性）的设计。因此，不管是应用层的存储系统（如DBMS、KV-store）、虚拟化层中的镜像管理、系统层的文件系统，甚至是硬件层的SSD FTL[7]，都要通过强制同步各种元数据的写入顺序，或者利用redo log的思想，用journaling、log-structured或copy-on-write等策略保证元数据写入目的位置生效前先完整地生成日志，来保证系统崩溃或断电时，元数据之间是一致。但是，如果多层存储系统重叠，由于一致性机制导致同步次数增加就会层层放大。

比如，运行在x86虚拟机中的levelDB，其一次更新操作就会（1）最终导致levelDB写log文件和写数据两次同步写，这两次写就又会（2）导致2次的Guest文件系统log写和2次Guest文件系统数据写，一共4次同步写，这4次写又会导致（3）虚拟化镜像管理层的4 x N次写（N取决于镜像为保证元数据crash consistency的同步次数，若是qcow2格式，N可能有5次之多[6]），最后导致（4）Host文件系统的4 x N x 2 = 8 x N次同步写。当然这是一种比较极端的情况，但实际应用中也应该存在。

### 5. 基于LSM树的KV系统的Merge操作造成的写放大

levelDB等KV存储广泛采用了LSM树等结构进行存储组织，其特点就是靠上的level的数据会最终被merge sort到下层，由于多数level在磁盘文件中，这也就导致了同一KV数据的总写放大，放大的倍数就是大约是level的数目。和前边4中写放大不同的是，这种写放大并非写操作时马上就会发生写放大，而是写操作发生时会潜在的导致“未来会发生”写放大，所以这种写放大只会导致整体写代价提升，不会影响实时的延迟性能，只可能会影响磁盘带宽或者在SSD做存储设备时影响闪存耐久。FAST 16上有篇论文也专门分析了这种写放大。[9]

---

[1] Why buffered writes are sometimes stalled, http://yoshinorimatsunobu.blogspot.com/2014/03/why-buffered-writes-are-sometimes.html

[2] Block size and read-modify-write, https://www.spinics.net/lists/linux-xfs/msg14456.html

[3] https://en.wikipedia.org/wiki/Read-modify-write

[4] http://www.ecs.umass.edu/ece/koren/architecture/Raid/basicRAID.html

[5] https://utcc.utoronto.ca/~cks/space/blog/tech/AdvancedFormatDrives

[6] Q. Chen, L. Liang, Y. Xia, and H. Chen, “Mitigating Sync Amplification for Copy-on-write Virtual Disk,” 14th USENIX Conf. File Storage Technol. (FAST 16), pp. 241–247, 2016.

[7] J. Yang, N. Plasson, G. Gillis, N. Talagala, and S. Sundararaman, “Don’t stack your Log on my Log,” 

[8] H. Lim, D. G. Andersen, M. Kaminsky, I. Labs, and S. Clara, “Towards Accurate and Fast Evaluation of Multi-Stage Log-structured Designs”, (FAST 16).