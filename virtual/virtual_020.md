# GPU虚拟化


参考[1]讲了怎么利用opengl加速QEMU。

记录：https://github.com/zhangjaycee/real_tech/wiki/virtual_010#opengl

参考[2]介绍了virtio-gpu在4.2进入内核主线（2D），4.4内核主线加入3D功能。

参考[3]是virgil 3D GPU项目的github主页，貌似virgil 3D就是virtio-GPU。


## CUDA / OpenCL & Mesa（OpenGL）/Direct3D

>  [4]The Mesa project began as an open-source implementation of the OpenGL specification - a system for rendering interactive 3D graphics.

OpenCL和CUDA是利用GPU进行计算，OpenGL或者DirectX中的Direct3D是用来渲染3D（显卡最初的用途）。

## passthrough & virtualization

passthrough和virtualization是不同的。passthrough性能肯定更好，但是就没有虚拟化特性。比如很早之前vmware等虚拟机就支持显卡的passthrough，但是无法再虚拟机里支持虚拟的GPU。Nvdia也专门提出过专门支持virtualization的GPU系列GRID[5]。

在QEMU/KVM上，这种GRID是不支持的，只有vmware这种商用虚拟机支持。不过16年KVM Forum上英伟达的人讲过vGPU的实现，用了VFIO的方法。具体看这个[6]youtube视频。还有一个帖子[7]也讨论过类似的问题。先mark了，有时间再细看补充。。。


---

[1] QEMU with hardware graphics acceleration, https://at.projects.genivi.org/wiki/display/GDP/QEMU+with+hardware+graphics+acceleration

[2] virtio-gpu介绍, http://blog.csdn.net/ssdxiao0/article/details/52221422

[3] Virgil 3D GPU project, https://virgil3d.github.io/

[4] The Mesa 3D Graphics Library, https://www.mesa3d.org/intro.html

[5] NVIDIA GRID VIRTUAL GPU TECHNOLOGY, http://www.nvidia.com/object/grid-technology.html

[6] [2016] vGPU on KVM - A VFIO Based Framework by Neo Jia & Kirti Wankhede, https://www.youtube.com/watch?time_continue=1767&v=Xs0TJU_sIPc

[7] Sharing 1 graphics card across multiple guests or machines, https://forums.anandtech.com/threads/sharing-1-graphics-card-across-multiple-guests-or-machines.2393622/