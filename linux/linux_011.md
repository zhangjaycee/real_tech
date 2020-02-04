# Linux下如何创建分区、格式化分区、挂载分区

### 查看当前分区信息

```bash
# 查看磁盘分区（树状较直观）名称、大小、挂载点、文件系统：
(bash)$ lsblk -f
# 查看磁盘分区名称、大小、挂载点、使用情况、文件系统格式：
(bash)$ df -hT
```
### 创建分区

从上述命令找好要在哪个磁盘创建后，（如）/dev/sdc
```bash
(bash)$ fdisk /dev/sdc
```
然后会进入fdisk的交互终端，按照提示继续即可，输入`m`是命令帮助。

如果创建分区成功后，`/dev`中没有显示新创建的设备，可以用`partprobe`重新扫描分区。

### 格式化分区
linux一般格式化命令是以`mkfs`开头的
```bash
#以把sdc1分区格式化为ext4文件系统为例：
(bash)$ mkfs.ext4 /dev/sdc1
```

### 挂载分区
mount [分区][挂载点]
```
#e.g.
(bash)$ mount /dev/sdc1 /home/new_part
```

### 卸载分区
umount [分区]
```
#e.g.
(bash)$ umount /dev/sdc1
```

### 删除分区

找好要删除的分区在哪个磁盘后，用fdisk操作，比如/dev/sdc1 在 /dev/sdc 上：
```bash
(bash)$ fdisk /dev/sdc
```
然后会进入fdisk的交互终端，按照提示继续即可，输入`m`是命令帮助

### 开机自动挂载
编辑`/etc/fstab`

#### 注
mkfs.ext2/3/4 属于 mke2fs 工具，在我使用中发现kernel 5.4可能和centos 7自带mke2fs不兼容导致格式化ext文件系统挂载时出现superblock读取错误，所以可以编译安装新版mke2fs[2]。

但是升级后会在编译内核使用dracut时因blkid版本太旧导致问题，可以通过以下命令重新安装util-linux解决：
```bash
yum install -y util-linux
```


---
[1] http://blog.csdn.net/nahancy/article/details/52201121

[2] http://e2fsprogs.sourceforge.net/
