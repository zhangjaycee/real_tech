# FUSE (Filesystem in Userspace)

fuse是内核中已经有的模块，要写自己的fuse文件系统，要安装libfuse。


## 安装和编译libfuse

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


## 开发fuse文件系统


---

使用 FUSE 开发自己的文件系统  https://www.ibm.com/developerworks/cn/linux/l-fuse/

fuse： https://github.com/libfuse/libfuse

一个golang版的fuse：https://github.com/bazil/fuse