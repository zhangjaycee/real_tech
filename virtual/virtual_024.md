
# Docker的存储层


## 1. 容器本身的存储

#### 1.1. AUFS / overlay2

Ubuntu发行版支持AUFS，所有发行版(内核)支持overlay2，它们都是UnionFS，可以支持分层存储。

#### 1.2. device-mapper (LVM) [1][2]
由于主线内核不支持AUFS，CentOS等发行版默认用device-mapper，又分为LVM-loopback和LVM-direct两种。由于前者不用重新划分磁盘分区，默认为前者，但是性能较差。

* LVM-loopback

* LVM-direct

---

[1] https://docs.docker.com/storage/storagedriver/device-mapper-driver

[2] DOCKER基础技术：DEVICEMAPPER, https://coolshell.cn/articles/17200.html

[3] https://www.centos.bz/2016/12/docker-device-mapper-in-practice/

## 2. 卷的存储