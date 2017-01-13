# 怎样理解Qemu的I/O流程
### 版本
qemu版本： 2.7.0

### 块设备驱动BlockDriver

* 在`include/block/block_int.h`中默认声明了三种块设备驱动
```cpp
/* Essential block drivers which must always be statically linked into qemu, and
 * which therefore can be accessed without using bdrv_find_format() */
extern BlockDriver bdrv_file;
extern BlockDriver bdrv_raw;
extern BlockDriver bdrv_qcow2;
```
目测`bdrv_file`才是raw镜像文件的块设备驱动，在`block/raw-posix.c`和`block/raw-win32.c`中都有定义；而`bdrv_raw`只在`block/raw_bsd.c`中定义，关于`raw_bsd.c`这个文件名可能造成一些误解([详情](https://lists.gnu.org/archive/html/qemu-devel/2016-12/msg00286.html))；`bdrc_qcow2`的定义在`block/qcow2.c`中。

* 定义这些驱动的文件名貌似将会在以后的某个版本中被修改([详情](https://lists.gnu.org/archive/html/qemu-devel/2016-12/msg00284.html))，这样也防止造成更多混乱，修改如下：
```
 block/{raw-posix.c => file-posix.c}
 block/{raw-win32.c => file-win32.c}        
 block/{raw_bsd.c => raw-format.c}
```
这样修改防止造成混乱：因为驱动分两种驱动：protocol block driver和format block driver,现在还不太理解，有的信息是：

1. 
> main difference should be that bdrv_file_open() is invoked for protocol block drivers, whereas bdrv_open() is invoked for format block drivers（[参考 qemu-devel 的一个讨论](https://lists.gnu.org/archive/html/qemu-devel/2014-10/msg01938.html)）

2. raw-posix.c和raw-win32.c 中的`bdrv_file`中定义了`.format_name:"file"`和`.protocol_name:"file"`, 属于protocol block driver；而raw_bsd.c和qcow.c、qcow2.c等文件中的`bdrv_raw`、`bdrv_qcow2`等这些数据结构只定义了`.format_name:"raw"` / `.format_name:"qcow2"` 这些，属于format block driver。`bdrv_file`和`bdrv_raw`数据结构的定义如下：
```cpp
// block/raw-posix.c

BlockDriver bdrv_file = {
    .format_name = "file",
    .protocol_name = "file",
    .instance_size = sizeof(BDRVRawState),
    .bdrv_needs_filename = true,
    .bdrv_probe = NULL, /* no probe for protocols */
    .bdrv_parse_filename = raw_parse_filename,
    .bdrv_file_open = raw_open,
    .bdrv_reopen_prepare = raw_reopen_prepare,
    .bdrv_reopen_commit = raw_reopen_commit,
    .bdrv_reopen_abort = raw_reopen_abort,
    .bdrv_close = raw_close,
    .bdrv_create = raw_create,
    .bdrv_has_zero_init = bdrv_has_zero_init_1,
    .bdrv_co_get_block_status = raw_co_get_block_status,
    .bdrv_co_pwrite_zeroes = raw_co_pwrite_zeroes,

    .bdrv_co_preadv         = raw_co_preadv,
    .bdrv_co_pwritev        = raw_co_pwritev,
    .bdrv_aio_flush = raw_aio_flush,
    .bdrv_aio_pdiscard = raw_aio_pdiscard,
    .bdrv_refresh_limits = raw_refresh_limits,
    .bdrv_io_plug = raw_aio_plug,
    .bdrv_io_unplug = raw_aio_unplug,

    .bdrv_truncate = raw_truncate,
    .bdrv_getlength = raw_getlength,
    .bdrv_get_info = raw_get_info,
    .bdrv_get_allocated_file_size
                        = raw_get_allocated_file_size,

    .create_opts = &raw_create_opts,
};

// block/raw_bsd.c

BlockDriver bdrv_raw = {
    .format_name          = "raw",
    .bdrv_probe           = &raw_probe,
    .bdrv_reopen_prepare  = &raw_reopen_prepare,
    .bdrv_open            = &raw_open,
    .bdrv_close           = &raw_close,
    .bdrv_create          = &raw_create,
    .bdrv_co_preadv       = &raw_co_preadv,
    .bdrv_co_pwritev      = &raw_co_pwritev,
    .bdrv_co_pwrite_zeroes = &raw_co_pwrite_zeroes,
    .bdrv_co_pdiscard     = &raw_co_pdiscard,
    .bdrv_co_get_block_status = &raw_co_get_block_status,
    .bdrv_truncate        = &raw_truncate,
    .bdrv_getlength       = &raw_getlength,
    .has_variable_length  = true,
    .bdrv_get_info        = &raw_get_info,
    .bdrv_refresh_limits  = &raw_refresh_limits,
    .bdrv_probe_blocksizes = &raw_probe_blocksizes,
    .bdrv_probe_geometry  = &raw_probe_geometry,
    .bdrv_media_changed   = &raw_media_changed,
    .bdrv_eject           = &raw_eject,
    .bdrv_lock_medium     = &raw_lock_medium,
    .bdrv_aio_ioctl       = &raw_aio_ioctl,
    .create_opts          = &raw_create_opts,
    .bdrv_has_zero_init   = &raw_has_zero_init
};
```

### io流走向
#### 摘抄
> 摘自：[qemu-kvm0.12.1.2原生态读写] http://blog.chinaunix.net/uid-26000137-id-4425615.html
>vm-guset-os ---> hw(ide/virtio) ---> block.c --->raw-posix.c--->img镜像文件
> * 具体流程
>
1. 在虚拟机系统中进行复制、新建文件等操作
2. 虚拟机系统中该卷所在的磁盘驱动捕获读写操作，并记录操作所在的文件和内容，向qemu程序发送中断
3. qemu子线程(ap_main_loop)捕获到该操作，并退出(vm-exit), 然后进行端口IO读写(kvm_handle_io)
4. 使用vm-exit的端口参数和qemu初始化的地址进行对比操作，找到合适的驱动(ide or virtio)将虚拟机系统的读写操作解析
5. 调用block.c文件中bdrv_aio_writev函数，选择原始写函数。详见文章末尾附录1(block函数初始化过程)
6. 调用raw-posix.c中的原始读写函数将内容写入文件中。

#### 自行GDB调试

~~~

---------------------------------------------------------------------------------------
1. start_thread --> kvm_handle_io --> ... --> blk_aio_prwv --> [submit blk_aio_read_entry() to coroutine]
---------------------------------------------------------------------------------------

#0  blk_aio_prwv (blk=0x555556a6fc60, offset=0x0, bytes=0x200, qiov=0x7ffff0059e70, co_entry=0x555555b58df1 <blk_aio_read_entry>, flags=0, cb=0x555555997813 <ide_buffered_readv_cb>, opaque=0x7ffff0059e50) at block/block-backend.c:995
#1  blk_aio_preadv (blk=0x555556a6fc60, offset=0x0, qiov=0x7ffff0059e70, flags=0, cb=0x555555997813 <ide_buffered_readv_cb>, opaque=0x7ffff0059e50) at block/block-backend.c:1100
#2  ide_buffered_readv (s=0x555557f66a68, sector_num=0x0, iov=0x555557f66d60, nb_sectors=0x1, cb=0x555555997b41 <ide_sector_read_cb>, opaque=0x555557f66a68) at hw/ide/core.c:637
#3  ide_sector_read (s=0x555557f66a68) at hw/ide/core.c:760
#4  cmd_read_pio (s=0x555557f66a68, cmd=0x20) at hw/ide/core.c:1452
#5  ide_exec_cmd (bus=0x555557f669f0, val=0x20) at hw/ide/core.c:2043
#6  ide_ioport_write (opaque=0x555557f669f0, addr=0x7, val=0x20) at hw/ide/core.c:1249
#7  portio_write (opaque=0x555558044e00, addr=0x7, data=0x20, size=0x1) at /home/jaycee/qemu-io_test/qemu-2.8.0/ioport.c:202
#8  memory_region_write_accessor (mr=0x555558044e00, addr=0x7, value=0x7ffff5f299b8, size=0x1, shift=0x0, mask=0xff, attrs=...) at /home/jaycee/qemu-io_test/qemu-2.8.0/memory.c:526
#9  access_with_adjusted_size (addr=0x7, value=0x7ffff5f299b8, size=0x1, access_size_min=0x1, access_size_max=0x4, access=0x5555557abd17 <memory_region_write_accessor>, mr=0x555558044e00, attrs=...) at /home/jaycee/qemu-io_test/qemu-2.8.0/memory.c:592
#10 memory_region_dispatch_write (mr=0x555558044e00, addr=0x7, data=0x20, size=0x1, attrs=...) at /home/jaycee/qemu-io_test/qemu-2.8.0/memory.c:1323
#11 address_space_write_continue (as=0x555556577d20 <address_space_io>, addr=0x1f7, attrs=..., buf=0x7ffff7fef000 " \237\006", len=0x1, addr1=0x7, l=0x1, mr=0x555558044e00) at /home/jaycee/qemu-io_test/qemu-2.8.0/exec.c:2608
#12 address_space_write (as=0x555556577d20 <address_space_io>, addr=0x1f7, attrs=..., buf=0x7ffff7fef000 " \237\006", len=0x1) at /home/jaycee/qemu-io_test/qemu-2.8.0/exec.c:2653
#13 address_space_rw (as=0x555556577d20 <address_space_io>, addr=0x1f7, attrs=..., buf=0x7ffff7fef000 " \237\006", len=0x1, is_write=0x1) at /home/jaycee/qemu-io_test/qemu-2.8.0/exec.c:2755
#14 kvm_handle_io (port=0x1f7, attrs=..., data=0x7ffff7fef000, direction=0x1, size=0x1, count=0x1) at /home/jaycee/qemu-io_test/qemu-2.8.0/kvm-all.c:1800
#15 kvm_cpu_exec (cpu=0x555556a802a0) at /home/jaycee/qemu-io_test/qemu-2.8.0/kvm-all.c:1958
#16 qemu_kvm_cpu_thread_fn (arg=0x555556a802a0) at /home/jaycee/qemu-io_test/qemu-2.8.0/cpus.c:998
#17 start_thread (arg=0x7ffff5f2a700) at pthread_create.c:333
#18 clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:109


---------------------------------------------------------------------------------------
2. [(start from a coroutine) coroutine_trampoline] --> blk_aio_read_entry --> ... --> paio_submit_co --> [thread_pool_submit_co --> thread_pool_submit_aio (submit aio_workder() to thread pool)]
---------------------------------------------------------------------------------------

#0  thread_pool_submit_aio (pool=0x555558122740, func=0x555555b5f9a8 <aio_worker>, arg=0x7ffff00c41c0, cb=0x555555b030bf <thread_pool_co_cb>, opaque=0x7ffff41ff9a0) at thread-pool.c:240
#1  thread_pool_submit_co (pool=0x555558122740, func=0x555555b5f9a8 <aio_worker>, arg=0x7ffff00c41c0) at thread-pool.c:278
#2  paio_submit_co (bs=0x555556a763f0, fd=0xb, offset=0x0, qiov=0x7ffff0040c10, count=0x200, type=0x1) at block/raw-posix.c:1222
#3  raw_co_prw (bs=0x555556a763f0, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, type=0x1) at block/raw-posix.c:1276
#4  raw_co_preadv (bs=0x555556a763f0, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0x0) at block/raw-posix.c:1283
#5  bdrv_driver_preadv (bs=0x555556a763f0, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0x0) at block/io.c:834
#6  bdrv_aligned_preadv (bs=0x555556a763f0, req=0x7ffff41ffc50, offset=0x0, bytes=0x200, align=0x1, qiov=0x7ffff0040c10, flags=0x0) at block/io.c:1071
#7  bdrv_co_preadv (child=0x555556a7ba90, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0) at block/io.c:1165
#8  raw_co_preadv (bs=0x555556a6fe30, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0x0) at block/raw_bsd.c:182
#9  bdrv_driver_preadv (bs=0x555556a6fe30, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0x0) at block/io.c:834
#10 bdrv_aligned_preadv (bs=0x555556a6fe30, req=0x7ffff41ffec0, offset=0x0, bytes=0x200, align=0x1, qiov=0x7ffff0040c10, flags=0x0) at block/io.c:1071
#11 bdrv_co_preadv (child=0x555556a7bae0, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0) at block/io.c:1165
#12 blk_co_preadv (blk=0x555556a6fc60, offset=0x0, bytes=0x200, qiov=0x7ffff0040c10, flags=0) at block/block-backend.c:818
#13 blk_aio_read_entry (opaque=0x7ffff0040c50) at block/block-backend.c:1025
#14 coroutine_trampoline (i0=0xf0040cb0, i1=0x7fff) at util/coroutine-ucontext.c:79
#15 ?? () from /lib/x86_64-linux-gnu/libc.so.6
#16 ?? ()
#17 ?? ()


---------------------------------------------------------------------------------------
3.1. [(start from a thread) start_thread --> worker_thread] --> aio_worker --> handle_aiocb_rw --> handle_aiocb_rw_vector --> qemu_preadv --> preadv
---------------------------------------------------------------------------------------
#0  qemu_preadv (fd=0xb, iov=0x7ffff019d590, nr_iov=0x3, offset=0x4000) at block/raw-posix.c:790
#1  handle_aiocb_rw_vector (aiocb=0x7ffff019d670) at block/raw-posix.c:828
#2  handle_aiocb_rw (aiocb=0x7ffff019d670) at block/raw-posix.c:906
#3  aio_worker (arg=0x7ffff019d670) at block/raw-posix.c:1157
#4  worker_thread (opaque=0x555558122740) at thread-pool.c:105
#5  start_thread (arg=0x7fffb11ff700) at pthread_create.c:333
#6  clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:109

---------------------------------------------------------------------------------------
3.2. [(start from a thread) start_thread --> worker_thread] --> aio_worker --> handle_aiocb_rw --> handle_aiocb_rw_linear --> pread64
---------------------------------------------------------------------------------------
#0  pread64 () at ../sysdeps/unix/syscall-template.S:84
#1  handle_aiocb_rw_linear (aiocb=0x7ffff01f0c50, buf=0x7fffe6083000 "") at block/raw-posix.c:858
#2  handle_aiocb_rw (aiocb=0x7ffff01f0c50) at block/raw-posix.c:897
#3  aio_worker (arg=0x7ffff01f0c50) at block/raw-posix.c:1157
#4  worker_thread (opaque=0x555558122740) at thread-pool.c:105
#5  start_thread (arg=0x7fffb11ff700) at pthread_create.c:333
#6  clone () at ../sysdeps/unix/sysv/linux/x86_64/clone.S:109

~~~

---

> [[Qemu-devel] qemu io path] https://lists.gnu.org/archive/html/qemu-devel/2016-01/msg04699.html