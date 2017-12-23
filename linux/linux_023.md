# 查看系统软硬件配置

## 1. CPU & NUMA

### 1.1
```
lscpu
```

### 1.2 hwloc
参考[1]中，hwloc中的`lstopo`命令可以查看服务器CPU拓扑，包括NUMA架构txt示意图。
```
yum -y install hwloc hwloc-gui
lstopo --of txt --no-io # 查看从CPU核NUMA分布、各级缓存到memory的分布和大小
lstopo # gui显示包括IO连接的拓扑图
```
pci设备会给出设备编号，可以在 http://pci-ids.ucw.cz/ 中查询。

## 存储
```
lsblk
df -h
fdisk -l
```



* 参考

[1] Display Hardware Topology in Linux, http://www.tuxfixer.com/display-hardware-topology-in-linux/