# ZFS

## ZFS 和 openZFS的关系

OpenZFS项目包括illumos、FreeBSD、Linux、OS X等多个系统的开源ZFS实现[1]。linux实现为ZFS on Linux[2]。[3]中阐述了ZFS和openZFS的联系：

ZFS是Sun公司2005年随OpenSolaris操作系统发布的文件系统，由于其高级特性其他系统开发者在08年陆续开始将ZFS移植到其他操作系统。最开始，ZFS整合了checksumming、压缩、快照等功能。所有ZFS中，管理员可以用`ztool`工具管理磁盘设备、用`zfs`工具管理文件系统。

但是后来ZFS成为了Oracle的资产，并在2010年被停止公开开发。一些OpenSolaris的用户和开发者因此将ZFS最后的公开release版本fork为Illumos项目；后来在此基础上，OpenZFS项目开始。后来，Oracle ZFS和OpenZFS就成为了技术上的两个分支，据称相对ZFS，openZFS中50%的代码已经改过，所以两者已经不同了，但是还都是用`zfs`命令进行管理。

## 编译ZFS on Linux

[4]

---

[1] OpenZFS, http://open-zfs.org/wiki/Main_Page

[2] ZFS on Linux, http://zfsonlinux.org/

[3] ZFS vs. OpenZFS, https://www.ixsystems.com/blog/zfs-vs-openzfs/

[4] Building ZFS, https://github.com/zfsonlinux/zfs/wiki/Building-ZFS