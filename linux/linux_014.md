# 从内核空间到用户空间（FUSE / VFIO / SPDK / DPDK ...)

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


## 2. VFIO

## 3. SPDK

```
sudo scripts/setup.sh # kernel nvme driver ---> spdk
sudo HUGEMEM=4096 scripts/setup.sh # spdk ---> kernel driver
```
---

[1] Storage Performance Development Kit, http://www.spdk.io/doc/getting_started.html

[2] DOC(getting started) http://www.spdk.io/doc/getting_started.html

[3] Accelerate Your NVMe Drives with SPDK, https://software.intel.com/en-us/articles/accelerating-your-nvme-drives-with-spdk


## 4. DPDK