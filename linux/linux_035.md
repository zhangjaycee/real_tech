# Hugepage (大页)

文章[3]系列文章，介绍了Linux内核对大页的支持。[3]讲了使用shmget、hugetlbfs裸接口、匿名mmap (MAP_HUGETLB标志)和在hugetlfs基础上封装的libhugetlbfs、hugectl等库和工具。除了[3]讲的，本文还介绍透明大页THP、DAX文件系统大页映射等大页相关的新技术/工具。

## 1. Transparent Hugepages (THP) [1]

由 `/sys/kernel/mm/transparent_hugepage/enabled` 决定开启还是关闭：

```
$ cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never
```

除了`/sys`目录的相关控制项，`hugeadm`工具也可进行管理。

## 2. DAX文件所支持的大页映射 [2]

内核支持DAX的文件系统ext4和XFS现在支持2MB大小的hugepage了，但要使用这个特性，需要满足如下条件：

1. mmap()调用必须最少映射 2 MiB；
2. 文件系统块的最少以2 MiB被分配；
3. 文件系统块必须和mmap()调用有相同的对齐量。

其中，第1点(在用户态的调用)挺容易达到的，第2、3点得益于当年为了支持RAID所提出的特性，ext4和XFS也支持从底层分配一定大小和一定对齐量的块。

### 2.1 如何配置：

1. 确保所用的pmem namespace为 fsdax 模式。这里用`ndctl`工具进行设置。

2. 确保pmem block device从 2 MiB对齐的地址开始，这是因为当我们请求2 MiB对齐的块分配时，对齐是相对block device的开始地址而言的。具体怎么判断(利用`cat /proc/iomem`)和设置(利用`fdisk`对齐分区)还是参考[2]。

3. 格式化文件系统时注意加入适当参数，如：
```bash
# ext4:
mkfs.ext4 -b 4096 -E stride=512 -F /dev/pmem0
# XFS:
mkfs.xfs -f -d su=2m,sw=1 -m reflink=0 /dev/pmem0
mount /dev/pmem0 /mnt/dax
xfs_io -c "extsize 2m" /mnt/dax
```

配置之后，[2]中还介绍了怎么trace内核`dax_pmd_fault_done `函数的返回值(`NOPAGE`还是`FALLBACK`)判断配置是否生效。

## 3. 虚拟机的内存虚拟化和大页

根据QEMU docs[5]，`memory-backend-memfd`类型的内存可以实现以大页作为VM内存后端。

上一篇文章[4][6]讨论了大页对内存虚拟化(EPT)的性能影响。

---
[1] https://www.kernel.org/doc/Documentation/vm/transhuge.txt

[2] https://nvdimm.wiki.kernel.org/2mib_fs_dax

[3] https://lwn.net/Articles/375096/

[4] Wang, Xiaolin, et al. "Evaluating the impacts of hugepage on virtual machines." Science China Information Sciences 60.1 (2017): 012103.

[5] https://qemu.weilnetz.de/doc/qemu-doc.html

[6] T. Merrifield and H. R. Taheri, “Performance Implications of Extended Page Tables on Virtualized x86 Processors,” Proc. the12th ACM SIGPLAN/SIGOPS Int. Conf. Virtual Exec. Environ. - VEE ’16, no. July, pp. 25–35, 2016.