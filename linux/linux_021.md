# Linux中的“存储虚拟化”

## dm(Device Mapper)

## loopback

简单理解：将file虚拟为disk。

一个用法：可以用于将guest中格式化过的raw格式的qemu镜像文件挂到host上。具体方法参考[2]中Mounting an Image on a VM Host Server一节。

Set a loop device on the disk image whose partition you want to mount.
```bash
# 从raw镜像文件，创建一个loop设备。
losetup /dev/loop0 [QEMU_IMG_NAME].raw
Create a device map from the disk image's partitions.

# 创建一个从这个loop0分区，创建一个device map，这样在guest中分好的分区就可映射过来了。
kpartx -a /dev/loop0

# 由于我在guest中用对这个raw镜像格式化了一个ext4文件系统的分区，所以现在用lsblk看到有loop0设备和loop0p1分区。现在直接挂载：
mount /dev/mapper/loop0p1 [MOUNT_POINT]

# 现在就可以正常使用了。下面是umount步骤：
umount [MOUNT_POINT]
losetup -d /dev/loop0





---
### 参考

[1] Linux 内核中的 Device Mapper 机制, https://www.ibm.com/developerworks/cn/linux/l-devmapper/

[2] Managing Disk Images with qemu-img, https://www.suse.com/documentation/sles11/book_kvm/data/cha_qemu_guest_inst_qemu-img.html