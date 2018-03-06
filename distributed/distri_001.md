# QEMU 和 分布式系统

Ceph RBD和sheepdog在QEMU源码中支持的层次

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
                   |   +--------+--------+   e.g. 【sheepdog】/【RBD】/ file-posix / nbd
                   |   | Protocol Driver |
                   +-  +-----------------+   srcs in: QEMU_SRC/block/*

```

## 1. Ceph Cluster

Ceph Cluster的Block Device接口(RBD)和QEMU互相支持[1][2]，但是Ceph建议不要用qcow2，要用raw格式。相关源码在 `QEMU_SRC/block/rbd.c` 文件里。

Ceph支持纠删码[3]。

---

[1] [Ceph Docs]QEMU AND BLOCK DEVICES, http://docs.ceph.com/docs/master/rbd/qemu-rbd/

[2] [Ceph Docs]BLOCK DEVICES AND OPENSTACK, http://docs.ceph.com/docs/master/rbd/rbd-openstack/

[3] [Ceph Docs]ERASURE CODE, http://docs.ceph.com/docs/master/rados/operations/erasure-code/



## 2. Sheepdog Cluster分布式存储系统

与GlusterFS、Ceph作用类似，主要支持QEMU、OpenStack。

qemu源码中已经提供支持，相关源码在 `QEMU_SRC/block/sheepdog.c` 文件里，这是QEMU存储层次的最底层protocol layer(与file-posix、nbd等同级)，所以完全可以兼容protocol layer上面的层次（如raw、qcow2），从而使用qcow2的多种功能[4]。

同时sheepdog层也支持纠删码[5]。

---

[1] https://github.com/sheepdog/sheepdog/wiki

[2] http://blog.csdn.net/kidd_3/article/details/8154964

[3] http://blog.csdn.net/zonelan/article/details/7972587

[4] Which Format of QEMU Images Should I Run, https://github.com/sheepdog/sheepdog/wiki/Which-Format-of-QEMU-Images-Should-I-Run

[5] Erasure Code Support, https://github.com/sheepdog/sheepdog/wiki/Erasure-Code-Support

