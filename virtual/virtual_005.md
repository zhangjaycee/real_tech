# 用QEMU创建一个虚拟机

> 参考

>https://my.oschina.net/kelvinxupt/blog/265108#comment-list

>https://wiki.archlinux.org/index.php/QEMU

>[[Difference between qemu\qemu-kvm\qemu-system-x86_64\qemu-x86_64|virtual_004]]

### 环境
```
Host系统:    Ubuntu 16.04 desktop 64bit
软件/工具:    QEMU
             virt-manager
Guest镜像:    Ubuntu 16.04 server 64bit
```
### 1. 安装
```shell
sudo apt install qemu
sudo apt install virt-manager
```
这里安装virt-manager不是必要的，但是其图形界面可以让你在忘记命令行时方便操作。（`sudo virt-manager` 启动gui vm管理器）

### 2. 创建镜像
以qcow2格式为例,用`qemu-img`命令创建一个5G的镜像。
```shell
qemu-img create -f qcow2 [img_name].img 5G
```

### 3. 安装系统
首先可以验证是否支持CPU虚拟化加速`grep -E 'vmx|svm' /proc/cpuinfo`
然后，用`qemu-system-x86_64` 命令开始从系统安装镜像安装系统
```shell
qemu-system-x86_64 -m [memory_size] -enable-kvm [img_name].img -cdrom [system_iso_name].iso
```

### 4. 启动系统
```shell
 qemu-system-x86_64 -m [mem_size] -enable-kvm [img_name].img

```


