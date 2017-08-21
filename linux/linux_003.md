# Linux内核&内核模块的升级/更换/编译

## 升级centos的内核

> [How to Install or Upgrade to Latest Kernel Version in CentOS 7]https://www.tecmint.com/install-upgrade-kernel-version-in-centos-7/

## 编译内核模块

（以centos7的virtio_blk模块为例）

#### 1. 由于要修改的是内核模块，所以要下载完整版的内核源码
* 先要查看下内核版本和CentOS系统版本，然后去http://vault.centos.org/ 可以下载到系统对应的内核具体在[系统版本]/[updates]/Source/SPackages 文件夹中。

```bash
uname -r
cat /etc/redhat-release
```

* 然后安装源代码
```bash
rpm -i xxx.src.rpm
cd ~/rpmbuild/SPECS
rpmbuild -bp --target=$(uname -m) kernel.spec
```

#### 2. 修改drivers/block/virtio_blk.c
比如我在init函数里面加了一行printk
```cpp
static int __init init(void)
{
    ...
        printk(KERN_ALERT "hello!!~!~!!~~~,im JAYCEE !!...~~!~!~~!\n");
        virtblk_wq = alloc_workqueue("virtio-blk", 0, 0);
    ...
        error = register_virtio_driver(&virtio_blk);
    ...
}
```
#### 3. 编译virtio_blk.ko模块
```bash
cd /path/to/kernel_src
make oldconfig && make prepare
make scripts
make modules SUBDIRS=drivers/block
```
#### 4. 安装virtio_blk.ko
```bash
make modules_install SUBDIRS=drivers/block
```
#### 5. 重建/boot文件夹中的ramdisk镜像文件(initial ramdisk)
```bash
dracut -f 
```
#### 6. 完成，看结果
```bash
reboot
dmesg|grep JAYCEE
```

> [Creating a New Initial RAM Disk] https://wiki.centos.org/TipsAndTricks/CreateNewInitrd
> 
> [内核与ramdisk的关系] http://blog.sina.com.cn/s/blog_6a37498301013f9b.html
> 
> [centos 7.1 获取内核源码] http://blog.csdn.net/u010654572/article/details/51745817
>
> [initial ramdisk] https://en.wikipedia.org/wiki/Initial_ramdisk


## 内核编译配置

> [Linux-4.4-x86_64 内核配置选项简介 - 金步国](http://www.jinbuguo.com/kernel/longterm-linux-kernel-options.html)

> * Enable cleancache driver to cache clean pages if tmem is present (CONFIG_CLEANCACHE)

>Cleancache是内核VFS层新增的特性,可以被看作是内存页的"Victim Cache"(受害者缓存),当回收内存页时,先不把它清空,而是把其加入到内核不能直接访问的"transcendent memory"中,这样支持Cleancache的文件系统再次访问这个页时可以直接从"transcendent memory"加载它,从而减少磁盘IO的损耗.目前只有zcache和XEN支持"transcendent memory",不过将来会有越来越多的应用支持.开启此项后即使此特性不能得到利用,也仅对性能有微小的影响,所以建议开启.更多细节请参考"Documentation/vm/cleancache.txt"文件.

>* Enable frontswap to cache swap pages if tmem is present (CONFIG_FRONTSWAP)

>Frontswap是和Cleancache非常类似的东西,在传统的swap前加一道内存缓冲(同样位于"transcendent memory"中).目的也是减少swap时的磁盘读写.CONFIG_ZSWAP依赖于它,建议开启.
