# 几种常见分布式存储系统(Ceph、Swift、HDFS ...)

## Ceph

Ceph已经集成于Linux内核里，既提供类似于Openstack Swift、Amazon S3的 **对象存储** ，又提供类似Hadoop HDFS的 **文件存储** ，也提供类似Openstack Cinder的 **块存储** 。

Ceph的Filesystem接口，可以用内核提供的文件系统挂载，也可以用FUSE实现的Ceph-fuse挂载。

---
 
[1] http://blog.csdn.net/quqi99/article/details/32939509

[2] http://docs.ceph.com/docs/master/rbd/rbd/

## Swift

OpenStack的对象存储组件。

---

[1] http://docs.openstack.org/developer/swift/

## HDFS

Hadoop的存储引擎。

---

[1] http://hadoop.apache.org/docs/r1.2.1/hdfs_user_guide.html

