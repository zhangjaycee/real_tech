# PM(NVM)的存储虚拟化

存储虚拟化并非单指虚拟机中的存储管理。广义上，存储虚拟化包括软件或硬件实现的“多虚一”的存储池(storage pooling)、“一虚多”的卷管理(volume/image)、动态扩容(thin-provision)、快照(snapshot)、模板(templete/base image)等。

当前PM(也称SCM，有些人还称NVM)是内存接口的非易失存储设备，自然也会有类似的存储虚拟化需求。本文罗列现存的PM存储虚拟化实现，主要包括Linux内核支持的以及一些学术论文所提出的PM存储虚拟化方案。


### 1. 支持DAX设备的dm-linear和dm-stripe

device-mapper是Linux内核的存储虚拟化层，支持RAID等存储虚拟化功能。dm-linear和dm-stripe两种dm target目前支持DAX设备(即PM设备)。dm-linear即将多个PM设备线性“连接”起来，变为更大的PM分区；dm-stripe类似raid-0，chunks是在多个设备之间轮流写入的，总容量不会损失，有利于多个设备的并行提升吞吐。

### 2. BTT - PM虚拟成块设备

BTT (Block Translation Table) [2] 可以看做是一层间接(a level of indirection)，将PM的IO粒度由cache line(64 Bytes)转换为扇区大小(512 Bytes)。

### 3. 虚拟机中的PM虚拟化

QEMU[3][4], Vmware vSphere[5]。 相关学术论文[6][7]。

---

[1] https://pmem.io/2018/05/15/using_persistent_memory_devices_with_the_linux_device_mapper.html

[2] https://www.kernel.org/doc/Documentation/nvdimm/btt.txt

[3] https://github.com/qemu/qemu/blob/master/docs/devel/memory.txt

[4] https://github.com/qemu/qemu/blob/master/docs/nvdimm.txt

[5] https://storagehub.vmware.com/t/vsphere-storage/vsphere-6-7-core-storage-1/pmem-persistant-memory-nvdimm-support-in-vsphere/

[6] L. Liang et al., “A Case for Virtualizing Persistent Memory,” in Proceedings of the Seventh ACM Symposium on Cloud Computing - SoCC ’16.

[7] J. Zhang, L. Cui, P. Li, X. Liu, and G. Wang, “Towards Virtual Machine Image Management for Persistent Memory.”, MSST '19

