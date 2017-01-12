# 怎样理解Qemu的I/O流程
qemu版本： 2.8.0
### 块设备驱动BlockDriver

在`include/block/block_int.h`中声明了三种块设备驱动
```cpp
/* Essential block drivers which must always be statically linked into qemu, and
 * which therefore can be accessed without using bdrv_find_format() */
extern BlockDriver bdrv_file;
extern BlockDriver bdrv_raw;
extern BlockDriver bdrv_qcow2;
```
目测`bdrv_file`才是raw镜像文件的块设备驱动，在`block/raw-posix.c`和`block/raw-win32.c`中都有定义。而`bdrv_raw`只在`block/raw_bsd.c`中定义，关于raw_bsd.c这个文件名可能造成一些误解([详情](https://lists.gnu.org/archive/html/qemu-devel/2016-12/msg00286.html))。


>  摘自：[qemu-kvm0.12.1.2原生态读写] http://blog.chinaunix.net/uid-26000137-id-4425615.html

> * io流走向
>
vm-guset-os ---> hw(ide/virtio) ---> block.c --->raw-posix.c--->img镜像文件
> * 具体流程
>
1. 在虚拟机系统中进行复制、新建文件等操作
2. 虚拟机系统中该卷所在的磁盘驱动捕获读写操作，并记录操作所在的文件和内容，向qemu程序发送中断
3. qemu子线程(ap_main_loop)捕获到该操作，并退出(vm-exit), 然后进行端口IO读写(kvm_handle_io)
4. 使用vm-exit的端口参数和qemu初始化的地址进行对比操作，找到合适的驱动(ide or virtio)将虚拟机系统的读写操作解析
5. 调用block.c文件中bdrv_aio_writev函数，选择原始写函数。详见文章末尾附录1(block函数初始化过程)
6. 调用raw-posix.c中的原始读写函数将内容写入文件中。


---

> [[Qemu-devel] qemu io path] https://lists.gnu.org/archive/html/qemu-devel/2016-01/msg04699.html