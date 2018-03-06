# Sheepdog Cluster分布式存储系统

与GlusterFS、Ceph作用类似，主要支持QEMU、OpenStack。

qemu源码中已经提供支持，相关源码在 `QEMU_SRC/block/sheepdog.c` 文件里，这是QEMU存储层次的最底层protocol layer(与file-posix、nbd等同级)，所以完全可以兼容protocol layer上面的层次（如raw、qcow2），从而使用qcow2的多种功能[4]。

```
                        +---------------+    e.g. virtio-blk / nvme / ide
Frontend Devices  +-->  | Guest Devices |
                        +-------+-------+    srcs in: QEMU_SRC/hw/block/*
                                |                     QEMU_SRC/hw/ide/*
                                |
                                |
                   +-   +-------+-------+    e.g. qcow2 / raw
                   |    | Format Driver |
                   |    +---------------+    srcs in: QEMU_SRC/block/*
                   |
Backend Drivers  +-+            |
                   |   +--------+--------+   e.g. file-posix / nbd / 【sheepdog】
                   |   | Protocol Driver |
                   +-  +-----------------+   srcs in: QEMU_SRC/block/*

```


同时sheepdog层还支持纠删码[5]。

---

[1] https://github.com/sheepdog/sheepdog/wiki

[2] http://blog.csdn.net/kidd_3/article/details/8154964

[3] http://blog.csdn.net/zonelan/article/details/7972587

[4] Which Format of QEMU Images Should I Run, https://github.com/sheepdog/sheepdog/wiki/Which-Format-of-QEMU-Images-Should-I-Run

[5] Erasure Code Support, https://github.com/sheepdog/sheepdog/wiki/Erasure-Code-Support