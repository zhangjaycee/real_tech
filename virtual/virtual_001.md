# KVM(利用virsh)在Ubuntu上的安装和基本使用


>1. [安装](#安装)

>1. [创建虚拟机](#创建虚拟机)

>1. [其他常用virsh命令](#其他常用virsh命令)

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

## 其他常用virsh命令

```shell
virt-manager                                    #调出gui的虚拟机管理器
virsh list --all                                #列出所有虚拟机
virsh list                                      #只列出本地活动虚拟机
virsh define [xml_name].xml                     #通过配置文件定义一个虚拟机（这个虚拟机还不是活动的）
virsh start [vm_name]                           #启动名字为ubuntu的非活动虚拟机
virsh create [xml_name].xml                     #创建虚拟机（创建后，虚拟机立即执行，成为活动主机）
virsh suspend [vm_name]                         #暂停虚拟机
virsh resume [vm_name]                          #启动暂停的虚拟机
virsh shutdown [vm_name]                        #正常关闭虚拟机
virsh destroy [vm_name]                         #强制关闭虚拟机
virsh dominfo [vm_name]                         #显示虚拟机的基本信息
virsh domname [id_num]                          #显示id号为id_num的虚拟机名
virsh domid [vm_name]                           #显示虚拟机id号
virsh domuuid [vm_name]                         #显示虚拟机的uuid
virsh domstate [vm_name]                        #显示虚拟机的当前状态
virsh dumpxml [vm_name]                         #显示虚拟机的当前配置文件（可能和定义虚拟机时的配置不同，因为当虚拟机启动时，需要给虚拟机分配id号、uuid、vnc端口号等等）
virsh setmem [vm_name] [size]                   #给不活动虚拟机设置内存大小
virsh setvcpus [vm_name] [number]               #给不活动虚拟机设置cpu个数
virsh edit [vm_name]                            #编辑配置文件（一般是在刚定义完虚拟机之后）
```

>（参考） 

> http://jingyan.baidu.com/article/b907e627cfffc946e7891cd5.html

> http://blog.fens.me/vps-kvm/
