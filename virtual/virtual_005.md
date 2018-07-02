# 用QEMU创建一个虚拟机



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
#不启用vnc
qemu-system-x86_64 -m [memory_size] -enable-kvm [img_name].img -cdrom [system_iso_name].iso
#启用vnc 端口号为设置的参数端口号+5900 比如这里是5901
qemu-system-x86_64 -m [memory_size] -enable-kvm [img_name].img -cdrom [system_iso_name].iso -vnc :1
```
当不启用vnc的时候，qemu会自动弹出窗口，启用vnc的时候需要用`vncviewer ip:port`的形式连接虚拟机。

### 4. 启动系统
```shell
#最简单的命令：
 qemu-system-x86_64 -m [mem_size] -enable-kvm [img_name].img

#比较复杂的命令：
qemu-system-x86_64 -smp [vCPU_number] -m [memory_size] -enable-kvm\
-drive file=~/ubuntu_img.qcow2,if=virtio,cache=none,format=qcow2 \
-drive file=~/mysql-data.raw,if=virtio,cache=writethrough,format=raw \
-net nic -net user,hostfwd=tcp::2333-:22 -daemonize
#这条命令可以改变vcpu数、内存数，开启了kvm，关联了两个镜像文件，采用virtio-blk，
#cachemode分别是none和writethrough，格式分别为qcow2和raw，
#将网络端口22映射到2333，这样登陆的时候就可以用以下命令登陆了：
ssh root@localhost -p 2333

# 更复杂的命令：
/home/zjc/bin/qemu-2.12/bin/qemu-system-x86_64 -smp 6 -m 6144M -accel kvm \
-object iothread,id=jciothread2 \
-blockdev file,node-name=c7mini_file,cache.direct=on,filename=/home/zjc/vmimgs/c7mini_new_kernel.qcow2,aio=native \
-blockdev qcow2,node-name=c7mini_qcow2,cache.direct=on,file=c7mini_file \
-device virtio-blk,iothread=jciothread2,drive=c7mini_qcow2 \
-object iothread,id=jciothread1 \
-blockdev file,node-name=optane_file,cache.direct=on,filename=/OPTANE/optane.raw,aio=native \
-blockdev raw,node-name=optane_raw,cache.direct=on,file=optane_file \
-device virtio-blk,iothread=jciothread2,drive=optane_raw \
-object iothread,id=jciothread3 \
-blockdev file,node-name=optane_file2,cache.direct=on,filename=/OPTANE/optane2.raw,aio=native \
-blockdev raw,node-name=optane_raw2,cache.direct=on,file=optane_file2 \
-device virtio-blk,iothread=jciothread3,drive=optane_raw2 \
-object memory-backend-ram,id=ram,size=4096M -numa node,memdev=ram,cpus=0,nodeid=0 \
-object memory-backend-file,id=optane,size=2G,mem-path=/pmem0/mem_backend,share=on,discard-data=off,merge=off,align=2M -numa node,memdev=optane,cpus=1,nodeid=1 \
-net nic -net user,hostfwd=tcp::2333-:22 -nographic
```
---

[1] https://my.oschina.net/kelvinxupt/blog/265108

[2] https://wiki.archlinux.org/index.php/QEMU

[3] http://smilejay.com/2013/12/qemu-kvm-install-guest-in-text-mode/

[4] 本wiki：[[Difference between qemu\qemu-kvm\qemu-system-x86_64\qemu-x86_64|virtual_004]]


### 5. 远程服务器安装和使用需要注意

* 可以使用`-curses`来在当前终端显示虚拟机终端文字界面。要使用这个特性，需要在（Ubuntu为例）编译QEMU前安装`libcurses5-dev`和`libcursesw5-dev`两个包。
对于Ubuntu作为guest系统，需要注意，默认不支持curses，需要更改两个grub参数。

* 可以使用`-daemonize`来使QEMU后台运行，这样关闭启动终端也不会中断虚拟机运行了。

---

[1] http://blog.zorinaq.com/ubuntu-1004-as-a-guest-under-qemukvm-using-the-curses-driver/

[2] Jonathan wrote: I didnt need to blacklist any modules, grub and sort this all for us:

>In `/etc/default/grub`, 
>Add nomodeset to this line to prevent most things changing resolution:
>
>GRUB_CMDLINE_LINUX_DEFAULT="nomodeset"
>
>Uncomment this line to keep grub in text mode:
>
>GRUB_TERMINAL=console
>
>run 'update-grub' to appy your changes.
>
>reboot and enjoy
>07 Feb 2015 09:13 UTC




