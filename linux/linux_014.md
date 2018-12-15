# 从内核空间到用户空间（FUSE / VFIO / SPDK / DPDK / userfaultfd ...)

近年，一些本为内核处理的任务，分别出现用户态的实现，有的是为了提升开发灵活性(FUSE、userfaultfd)，有的则是为了提高与外设通信的性能(SPDK、DPDK)。

## 1. FUSE (Filesystem in Userspace)

fuse是内核中已经有的模块，要写自己的fuse文件系统，要安装libfuse。


### 安装和编译libfuse

step 1. 安装meson
```
pip3 install meson
```
step 2. 安装ninja
```
git clone git://github.com/ninja-build/ninja.git && cd ninja
git checkout release
./configure.py --bootstrap
cp ninja /usr/bin/
```

step 3. 安装libfuse
```
# 下载源码如fuse-3.2.1.tar.xz
tar -xvf fuse-3.2.1.tar.xz
cd fuse-3.2.1
mkdir build; cd build
meson ..
ninja
python3 -m pytest test/  #这是测试，我在安装时第一次测试提示modprobe cuse
ninja install
```


---
[1] ninja, https://ninja-build.org/

[2] libfuse, https://github.com/libfuse/libfuse


### 开发fuse文件系统


---

使用 FUSE 开发自己的文件系统  https://www.ibm.com/developerworks/cn/linux/l-fuse/

fuse： https://github.com/libfuse/libfuse

一个golang版的fuse：https://github.com/bazil/fuse


## 2. 用户态IO: UIO/VFIO(mdev)/
[1]是内核文档，[2]是一个VFIO(mdev)和QEMU相关的论文。[3][4]是两个不错的说明博客。

---
[1] https://www.kernel.org/doc/Documentation/vfio-mediated-device.txt

[2] B. Peng, “MDev-NVMe : A NVMe Storage Virtualization Solution with Mediated,” 2018.

[3] https://zhuanlan.zhihu.com/p/28111201

[4] https://blog.csdn.net/zgy666/article/details/78649777

## 3. SPDK

SPDK是给高性能NVMe SSD设计的用户态驱动框架。主要利用了1）基于polling的设备完成状态检测来降低延迟和2）每个应用线程一个专用的共享自内核的硬件NVMe submission queue来减少锁的竞争。[1]

其中第2）点是针对原本的驱动设计而做出的优化： 在原本的内核NVMe驱动中，会创建和CPU核数相等数量的SQ/CQ对，这些SQ/CQ对与各个物理核对应的，由于应用的线程/进程运行在哪个物理核上是不一定的，所以多个应用同时运行在一个核上同时访问一个SQ是有可能的，这时需要对这个SQ加锁，这就引起的不必要的性能开销。

NVMe内核驱动这种实现虽然比以前的单queue少了很多锁竞争开销，但还是无法避免这种多个线程抢占同一个queue的情况。因此SPDK，作为一个用户态的程序，为调用它接口的应用提供了统一的管理，由SPDK来向内核申请某个应用专用的SQ绑定到特定的应用上，这样就实现了无锁的SQ。具体的，SPDK申请的SQ数目不一定局限于和core数相等，而是可能更多，这样就能满足应用较多的情况，同时又让各个queue没有锁的开销。

类似SPDK的还有NVMeDirect这个东西，其也是用户态的提升NVMe性能的框架。[4]


（下面是安装完SPDK开启它的命令的一个例子）

```
sudo [HUGEMEM=4096] scripts/setup.sh # kernel nvme driver ---> spdk
sudo scripts/setup.sh reset # spdk ---> kernel driver
```

## 4. DPDK

## 5. userfaultfd

userfaultfd是用户态的缺页处理机制。详见本wiki([userfaultfd](https://github.com/zhangjaycee/real_tech/wiki/linux_031))。

在Userfaultfd之前，用户态缺页处理使用 "mprotect + SIGSEGV信号处理" 来实现的，libsigsegv[5]就是专门用来干这个的一个GNU库。[7] 这种方法比较triky，效率不如新出的userfaultfd？[6]

---

[1] Storage Performance Development Kit, http://www.spdk.io/doc/userspace.html

[2] DOC(getting started) http://www.spdk.io/doc/getting_started.html

[3] Accelerate Your NVMe Drives with SPDK, https://software.intel.com/en-us/articles/accelerating-your-nvme-drives-with-spdk

[4] H. Kim, Y.-S. Lee, and J.-S. Kim, “NVMeDirect: A User-space I/O Framework for Application-specific Optimization on NVMe SSDs,” Hotstorage, 2016.

[5] https://www.gnu.org/software/libsigsegv/

[6] https://lists.gnu.org/archive/html/bug-libsigsegv/2015-03/msg00000.html

[7] https://stackoverflow.com/questions/49583685/older-alternatives-for-userfaultfd-syscall-in-linux
