# 存储I/O中的multi-queue

### 内核块层 (blk-mq)

（本wiki中的相关链接：[[Linux Block Layer中的I/O队列和调度器|https://github.com/zhangjaycee/real_tech/wiki/linux_015#22-block-layer----blk-mq-block-multi-queue]]）

用于替代原先的块IO调度层，用多Queue代替单Queue，并且取消了电梯调度算法。

### NVMe设备及驱动 (SQs, CQs)

（本wiki中的相关链接：[[Linux NVMe Driver|https://github.com/zhangjaycee/real_tech/wiki/linux_026]]、
[[从内核空间到用户空间（FUSE / VFIO / SPDK / DPDK ...)|https://github.com/zhangjaycee/real_tech/wiki/linux_014#3-spdk]]）

内核NVMe驱动中，SQ和CQ是多个，和核数相等。而SPDK中，用了SPDK库的每个用户应用都有一个专门的SQ，有SPDK从内核空间映射绑定给应用。类似SPDK，NVMeDirect[1]也是在用户空间管理多个Queue。

---

[1] H. Kim, Y.-S. Lee, and J.-S. Kim, “NVMeDirect: A User-space I/O Framework for Application-specific Optimization on NVMe SSDs,” Hotstorage, 2016.

### Virtio (multiple virtqueue)

（本wiki中的相关链接：[[关于virtio|https://github.com/zhangjaycee/real_tech/wiki/virtual_008#virtio-blk%E5%92%8Cmultiqueue]]）

当前QEMU的virtio-blk-data-plane支持了multiple virtqueue。但QEMU的存储IO还并不是真正的multi-queue，因为不支持IOthread始终是一个，这比较难以修改，因为QEMU的block layer不易改成multiple IOthread，比如qcow2不是线程安全的，强行修改可能会导致qcow2更新数据时出现元数据不一致的情况[1]。但是，在raw格式上应该是没有问题的，虽然主线QEMU没有这个功能，但有一篇论文[2]做了这个工作。

---

[1] https://www.youtube.com/watch?v=KVD9FVlbqmY

[2] T. Y. Kim, D. H. Kang, D. Lee, and Y. I. Eom, “Improving performance by bridging the semantic gap between multi-queue SSD and I/O virtualization framework,” IEEE Symp. Mass Storage Syst. Technol., vol. 2015–Augus, 2015.