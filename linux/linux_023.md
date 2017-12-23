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

## 存储
```
lsblk
df -h
fdisk -l
```



* 参考

[1] hwlock and lstopo to easily check out the cpu topology, https://community.centminmod.com/threads/hwloc-and-lstopo.4317/