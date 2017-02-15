# Qemu实际应用的各种小技巧

# qemu-kvm宿主机和客户机之间的文件共享

## 方法1
通过搭建网桥网络传输，比如搭建scp、ftp等方式。
搭建方式见[[关于Qemu/KVM 虚拟机的网络配置|virtual_007]]
## 方法2
> 摘自：http://blog.csdn.net/scaleqiao/article/details/45197093

在虚拟机环境下，我们可能会遇到在宿主机和客户机之间传输文件的需求，目前有几种方法可以实现这个例如通过9p协议，或者为客户机和宿主机之间搭建一个网络等。这些都太不容易实现，下面我介绍一种简单的方法。

1. 使用dd创建一个文件，作为虚拟机和宿主机之间传输桥梁
`dd if=/dev/zero of=/var/lib/libvirt/images/share.img bs=1M count=350`

2. 格式化share.img文件
`mkfs.ext4/var/lib/libvirt/images/share.img`

3. 在宿主机上创建一个文件夹，`
mkdir /tmp/share
mount -o loop/var/lib/libvirt/images/share.img /tmp/share`
这样，在宿主机上把需要传输给虚拟机的文件放到/tmp/share 下即可。

4. 启动qemu-kvm虚拟机，可以额外为客户机添加上一块硬盘。

-drive file=/var/lib/libvirt/images/share.img,if=virtio

5. 在虚拟机中 mount上添加的一块硬盘。即可以获得宿主机上放在/tmp/share文件夹下的文件，具体做法是：通过dmesg的输出找到新挂在的硬盘是什么，然后将硬盘直接mount上来。

mount -t ext4 /dev/vdb /mnt/   

当然，该方法虽然简单，但它也有缺点：
     宿主机和虚拟机文件传输不能实时传输。如果需要传输新文件，需要重启虚拟机。



