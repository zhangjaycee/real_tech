
# Docker的存储层


根据docker文档中关于存储的部分[3]，docker的存储被分到两部分，一部分是容器中的存储，一部分是卷存储 

## 1. 容器本身的存储

#### 1.1. AUFS / overlay2

Ubuntu发行版支持AUFS，所有发行版(内核)支持overlay2，它们都是UnionFS，可以支持分层存储。

#### 1.2. device-mapper (LVM) [1][2]
由于主线内核不支持AUFS，CentOS等发行版默认用device-mapper，又分为loopback-lvm和direct-lvm两种。由于前者不用重新划分磁盘分区，默认为前者loopback-lvm，但是它性能很差。但是注意新版的CentOS是支持overlay2的，因此最好还是使用overlay2。

#### 1.3. 高级文件系统BtrFS或ZFS

这两种文件系统支持快照等功能，如果docker装在这些文件系统上，可以直接配置host 文件系统作为docker的存储driver。

#### 1.4. VFS

直接用VFS的话，创建新的层实际需要对之前的所有层作“深拷贝”，因此这种方法只用于测试。


---

[1] https://docs.docker.com/storage/storagedriver/device-mapper-driver

[2] DOCKER基础技术：DEVICEMAPPER, https://coolshell.cn/articles/17200.html

[3] https://www.centos.bz/2016/12/docker-device-mapper-in-practice/

## 2. 卷的存储

包括volumes, bind mount和tmpfs mount。

volumes和bind mount类似，但volume要优于bind mount。[1]

tmpfs mount则是针对memory的，而且只可用于linux。

---
[1] https://docs.docker.com/storage/volumes/

