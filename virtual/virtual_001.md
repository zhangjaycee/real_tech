# KVM在Ubuntu上的安装和基本使用

>1. （参考） http://jingyan.baidu.com/article/b907e627cfffc946e7891cd5.html

>1. [安装](#安装)

>2. [创建虚拟机](#创建虚拟机)

## 安装

* 检查CPU是否支持安装KVM：
```shell
$ egrep -o '(vmx|svm)' /proc/cpuinfo
```

* 安装KVM所需要的软件包：
```shell
$ apt-get install qemu-kvm libvirt-bin virt-manager bridge-utils
```
其中：virt-manager为GUI管理窗口，bridge-utils:用于网络桥接

* 检查下是否安装成功：
```shell
lsmod | grep kvm 或 virsh -c qemu:///system list
```

## 创建虚拟机

* 创建工作目录，准备镜像
~~~shell
cd ~
mkdir iso_kvm
mkdir vdisk_kvm
mv xxx.iso ~/iso_kvm
~~~

* 开始创建
~~~shell
virt-install --name ubuntutest --hvm --ram 1024 --vcpus 1 \
--disk path=~/vdisk_kvm/vdisk0.img,size=10  \
--network network:default --accelerate  --vnc --vncport=5911 \
--cdrom ~/iso_kvm/xxx.iso -d
~~~
>[参数说明]
* --name     虚拟机名称
* --hvm      使用全虚拟化（与para-irtualization向对），不支持xen hypervisor
* --ram      虚拟机内存大小
* --vcpus    虚拟机虚拟CPU个数
* --disk     虚拟机使用的磁盘（文件）的路径
* --network  网络设置，使用默认设置即可
* --vnc      设置连接桌面环境的vnc端口，本例是5911
* --cdrom    设置光驱获取虚拟光驱文件的路径 
* -d         指示从光驱启动（ -c 指示从硬盘启动）我们这里是iso