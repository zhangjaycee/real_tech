# 利用QEMU Monitor限制内存、I/O和vCPU数

## 如果接入QEMU

* 启动QEMU虚拟机时，加入`-curses`启动参数，然后在虚拟机开始启动后按`ESC+2`进入QEMU Monitor

* 类似上边的方法，也可以加入`-vnc :1`启动参数，在VNC界面调出QEMU Monitor

* 还可以选择加入`-qmp unix:./qmp-sock,server,nowait`参数，这时会在当前目录新建一个名为“qmp-sock”的Unix Socket文件，QEMU源码树的`scripts/qmp`文件夹中已经提供了相关的连接脚本，可以直接这样连接：

```bash
/PATH_TO_QEMU_SRCS/scripts/qmp/qmp-shell -H ~/vmimgs/qmp-sock
```
注意其中的`-H`是指以HMP模式启动QEMU Monitor，如果不加是以low-level的QMP模式启动。

然后就会出现欢迎语和以`(qemu)`开头的交互式qmp-shell。


## 内存
* 利用balloon限制内存

开启虚拟机时需要加入参数`-balloon virtio`

在QEMU Monitor中，使用`info balloon`可以查看当前的内存，使用`balloon [mem_size]`可以将当前内存限制在某个值。

在开启虚拟机的时候会用`-m`设置内存，这个是balloon的最大内存值。

* 利用hotpluggable memory来限制内存

?貌似还需要在虚拟机内插拔内存，待续。。

## 限制I/O

是利用QEMU Monitor的`block_set_io_throttle`命令。基本格式：
```bash
block_set_io_throttle device bps bps_rd bps_wr iops iops_rd iops_wr
```

例子：
```bash
# 查询磁盘设备
info block
# 进行I/O限流，比如这里是限制virtio2这个设备的iops为100
block_set_io_throttle virtio2 0 0 0 100 0 0
```

## 插拔vCPU

待续。。。


[1] Documentation/QMP, https://wiki.qemu.org/Documentation/QMP

[2] QEMU CPU Hotplug,http://events.linuxfoundation.org/sites/events/files/slides/CPU%20Hot-plug%20support%20in%20QEMU.pdf

[3] Features/CPUHotplug, https://wiki.qemu.org/Features/CPUHotplug

[3] qemu-docs, memory-hotplug, https://github.com/qemu/qemu/blob/master/docs/memory-hotplug.txt

[4] I/O bursts with QEMU 2.6, https://blogs.igalia.com/berto/2016/05/24/io-bursts-with-qemu-2-6/

[5] QEMU DOC, https://qemu.weilnetz.de/doc/qemu-doc.html