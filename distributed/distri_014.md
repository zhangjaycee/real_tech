# 存储栈中的各种“放大”

### 1. FS写放大

文件系统中，读写单元固定，比如都是4K，这样，如果write函数写的数据小于4K，则要先把整块读入，再修改，再把新的4K整体写入。这个过程可以称为 **RMW** (Read-Modify-Write)，这就是File System的写放大问题。[1][2][5] 注意：Read-Modify-Write被更广泛地用在[[原子指令|prog_018]][3]和RAID[4]中。

### 2. RAID中的Read-Modify-Write

如前段所述，RAID中更新一个块，需要额外读原始块、校验块，额外写校验块，所以多了两个读，一个写，也称为Read-Modify-Write。[4]

---

[1] Why buffered writes are sometimes stalled, http://yoshinorimatsunobu.blogspot.com/2014/03/why-buffered-writes-are-sometimes.html

[2] Block size and read-modify-write, https://www.spinics.net/lists/linux-xfs/msg14456.html 

[3] https://en.wikipedia.org/wiki/Read-modify-write

[4] http://www.ecs.umass.edu/ece/koren/architecture/Raid/basicRAID.html

[5] https://utcc.utoronto.ca/~cks/space/blog/tech/AdvancedFormatDrives
### 3. SSD中的写放大问题

在SSD中，一个block可以分为多个page，在读的时候，可以以page为单位，但是写的时候，只能以block为单位。因此写的单元比较大。在上层（比如文件系统）读写单元相同的情况下，同样是读写1个page的大小，读的话直接读就行，写的话却需要先把与要写page同一个block的数据全复制一遍，加上修改的page后，再一起写入block。写入的数据量远比实际的大，这就是SSD的写放大问题。

### 4. 同步放大问题[1][2]

---
[1] Q. Chen, L. Liang, Y. Xia, and H. Chen, “Mitigating Sync Amplification for Copy-on-write Virtual Disk,” 14th USENIX Conf. File Storage Technol. (FAST 16), pp. 241–247, 2016.

[2] J. Yang, N. Plasson, G. Gillis, N. Talagala, and S. Sundararaman, “Don’t stack your Log on my Log,” Inf