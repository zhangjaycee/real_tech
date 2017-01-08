# 从源码编译Qemu的流程及简述

要理解甚至修改Qemu，肯定要会编译它，不能老是apt－get，所以做个流程记录，并带上简单的解释。

## 1. 下载源码

 http://wiki.qemu.org/Download 从这里下就可以了

## 2. 解压

比如我下载的是`qemu-2.8.0.tar.bz2`
~~~bash
# 解压
tar -xvf qemu-2.8.0.tar.bz2
＃ 进入源码目录
cd qemu-2.8.0
~~~

## 3. 配置
~~~bash
# 配置
./configure [--enable_debug --prefix=/PATH/TO/INSTALL --target_list=x86_64-softmmu]
~~~
configure文件中有很多可选的配置，可以通过`./configure --help`查看详细配置帮助。

这里简单解释下上边中括号中的可选配置的含义：

`--enable_debug`: 打开后可以用gdb debug了

`--prefix=[path]`: 指定二进制程序的安装目录

`--target_list=[target]`: 编译指定的模拟器，可选的列表在`./configure --help`中有写，注意这里"xxx-soft"和"xxx-linux-user"分别指系统模拟器和应用程序模拟器, 分别生成的二进制文件名字为"qemu-system-xxx"和"qemu-xxx"

## 4. 编译
~~~bash
make
~~~

## 5. 安装
~~~bash
make install
~~~
