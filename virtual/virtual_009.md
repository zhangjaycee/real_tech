# Qemu进行读/写的流程

1. [流程分析](#流程分析)
2. [杂项讨论](#杂项讨论)  (主要为19年前更新)

## 流程分析
以virtio-blk -- qcow2 -- file-posix 为例，qemu版本： 4.1

### 1. guest --> host 通知

对于virtio-blk有两种方式，一种是普通的由guest使用vcpu向设备配置空间的写操作，另一种是在使用了iothread的情况下可以选择使用ioeventfd从guest获得通知。

#### 1.1. virtio的一般情况

虽然virtio-blk支持AioContext(IOthread)，但大部分virtio后端都是以监测virtio配置空间的方式实现对guest到host通知的监视。具体流程如下：

* 调用virtio-blk的realize函数时，`virtio_blk_handle_output`被注册

```cpp
virtio_blk_device_realize
--> virtio_add_queue(vdev, conf->queue_size, virtio_blk_handle_output);
```

* pci 配置空间的特定内存被KVM监视，guest写它是会发生VM-exit，进而通知QEMU，QEMU最终调用`virtio_blk_handle_output`函数：

```cpp
virtio_pci_config_write  (hw/virtio/virtio-pci.c)
    --> virtio_ioport_write
  	--> //case VIRTIO_PCI_QUEUE_NOTIFY:
	    virtio_queue_notify (hw/virtio/virtio.c)
  	    -->  vq->handle_output    
  							(这里即 virtio_blk_handle_output)

// 参考结构：(hw/virtio/virtio-pci.c)
static const MemoryRegionOps virtio_pci_config_ops = {
    .read = virtio_pci_config_read,
    .write = virtio_pci_config_write,
    //.....
};
```

#### 1.2. 使用ioeventfd

virtio-blk的dataplane思路即用单独的iothread来处理异步文件IO的完成，而不去占用QEMU main-loop的资源[3]。目前来说，AioContext、iothread和virtio-blk-dataplane基本都是这一实现的相关描述。

在使用iothread服务virtio-blk的情况下，QEMU还支持将guest到host的通知的监测纳入统一的epoll操作中，具体是将生成一个与guest对写配置空间关联的ioeventfd。这也意味着，iothread将同时负责两种事件的polling：(1)  QEMU对host文件aio的完成，以及 (2)guest对host的virtqueue的请求通知(notify)。在整条IO路径上，这两种事件都会出现，随意稍显混乱，本节主要关注后者，第4节将关注前者。[4]是一个描述QEMU如何优化polling时长的slide，其也说明两种polling在这里是统一起来的。

下面是使用eventfd监测guest->host通知的初始化流程和poll过程：

* 注册ioeventfd：

需要注意的是，对ioeventfd的使用的发起也是由写配置空间实现的，最终调用`virtio_blk_data_plane_handle_output`被作为virtio请求处理的函数被注册。

```cpp
virtio_pci_config_write
--> virtio_ioport_write
    --> virtio_pci_start_ioeventfd
        --> virtio_bus_start_ioeventfd
            --> vdc->start_ioeventfd
                (virtio_blk_data_plane_start)
                --> virtio_queue_aio_set_host_notifier_handler(vq, s->ctx, virtio_blk_data_plane_handle_output);
```

* poll

`aio_poll`会负责poll 对应的ioeventfd：

```cpp
aio_poll
--> try_poll_mode
    --> run_poll_handlers
        --> run_poll_handlers_once
            --> (foreach aio_handlers) node->io_poll
```

### 2. virtio-blk层

到了virtio-blk层，根据上节两种情况，`virtio_blk_data_plane_handle_output`或`virtio_blk_handle_output`会被调用，它们之后的代码路径相同，最后都会创建一个叫`blk_aio_read_entry`或`blk_aio_read_entry`的协程[1]，以下以读为例：

```cpp
virtio_blk_data_plane_handle_output
(或) virtio_blk_handle_output --> virtio_blk_handle_output_do
    --> virtio_blk_handle_vq 			(hw/block/virtio-blk.c)
        --> virtio_blk_handle_request 
        (同向相邻的请求进行一些合并)
    +-> virtio_blk_submit_multireq  
        --> submit_requests 
            --> blk_aio_preadv      (block/block-backend.c)
                (这里传入完成回调函数为virtio_blk_rw_complete)
                --> blk_aio_prwv
                    --> qemu_coroutine_create
                        (这里创建的协程函数为blk_aio_read_entry)
                    +-> bdrv_coroutine_enter
```

### 3. QEMU块层

QEMU的块层被设计成一种可递归叠加的驱动形式，这里以qcow2 -- posix文件为例：

```cpp
# coroutine:
[blk_aio_read_entry]           (block/block-backend.c)[co]
--> blk_co_preadv																			[co]
  -->bdrv_co_preadv(blk->root...            (io.c)  	[co]
    --> qcow2_co_preadv 									(qcow2.c)		[co]
      --> ret = bdrv_co_preadv(data_file... 					[co]
        --> bdrv_aligned_preadv(data_file... 					[co]
          --> bdrv_driver_preadv 											[co]
            --> drv->bdrv_co_preadv 
             (raw_co_preadv)      		(file-posix.c)	[co]
              --> raw_co_prw 													[co]
                --> 路径① laio_co_submit    (linux-aio.c)  [co]
                    --> laio_do_submit
                       --> io_prep_preadv
                       +-> io_set_eventfd
                       +-> ioq_submit
                          --> io_submit
                    +-> qemu_coroutine_yield
                +-> 路径② (用了线程池模拟异步IO，这里先不讨论)
                		--> raw_thread_pool_submit [co]
+-> blk_aio_complete
```

### 4. 文件aio的发起和完成

linux aio 的发起需要用户态应用(这里指QEMU)处理请求的开始、监测完成等步骤，因此在提交IO后，需要epoll请求的完成，这里QEMU用了和第1节一样eventfd机制。

首先可以看到，一个IOthread由一个`AioContext`结构所描述，其指针`aio_context`被保存在一个`struct LinuxAioState`中：

```cpp
// 参考结构 (ctx->linux_aio的类型LinuxAioState)
struct LinuxAioState {
    AioContext *aio_context;

    io_context_t ctx;
    EventNotifier e;

    /* io queue for submit at batch.  Protected by AioContext lock. */
    LaioQueue io_q;

    /* I/O completion processing.  Only runs in I/O thread.  */
    QEMUBH *completion_bh;
    int event_idx;
    int event_max;
};
```

一个虚拟机镜像文件被打开时，AioContext的eventfd (`EventNotifier e`)会被初始化，并最终关联linux native aio对应的回调函数`qemu_laio_completion_cb`和`qemu_laio_poll_cb`：

```cpp
// open镜像时，初始化aio的eventfd，并关联bs的AioContext(iothread)：
raw_open_common (block/file-posix.c)
			--> aio_setup_linux_aio (util/async.c)
          --> ctx->linux_aio =laio_init(..) (block/linux-aio.c)
              --> event_notifier_init(&s->e..)  --> eventfd
              +-> io_setup
  				# 以下分别将io_read和io_poll回调设置成
  				# qemu_laio_completion_cb和qemu_laio_poll_cb：
          +-> laio_attach_aio_context(ctx->linux_aio...)
							--> aio_set_event_notifier 
  								--> aio_set_fd_handler
```

在实际运行过程中，同第1节一样，`aio_poll`或轮询已经提交的异步文件IO的完成情况，若检测到完成事件会调用`qemu_laio_completion_cb`：

```cpp
// 轮询检测完成事件
aio_poll
--> try_poll_mode
    --> run_poll_handlers
        --> run_poll_handlers_once
            --> (foreach aio_handlers) node->io_poll

// 处理完成事件：
--> qemu_laio_completion_cb  (linux-aio.c)
    --> qemu_laio_process_completions_and_submit
        --> qemu_laio_process_completions
            --> qemu_laio_process_completion
                --> qemu_coroutine_entered
```

### 5. host--> guest通知

第4节的`qemu_coroutine_entered`会返回到第3节中`qemu_coroutine_yield`处，接着调用aio完成函数`blk_aio_complete`，最终调用被传入的virtio完成函数`virtio_blk_rw_complete`。同样对guest的通知还是两种方式，(1)对应于ioeventfd，可以用irqfd对guest通知；也可以(2)通过中断注入的形式进行通知。

```
blk_aio_complete              (block/block-backend.c)
    --> acb->common.cb (即virtio_blk_rw_complete)
        --> virtio_blk_data_plane_notify
            --> virtio_notify_irqfd
                --> event_notifier_set
        +-> (或) virtio_notify
            --> virtio_irq
                --> virtio_notify_vector
                    --> virtio_pci_notify
```

---

### 参考资料

[1] http://blog.vmsplice.net/2014/01/coroutines-in-qemu-basics.html

[2] https://www.cnblogs.com/kvm-qemu/articles/7856661.html

[3] https://github.com/qemu/qemu/blob/master/docs/devel/multiple-iothreads.txt

[4] https://vmsplice.net/~stefan/stefanha-kvm-forum-2017.pdf

[5] https://www.cnblogs.com/kvm-qemu/articles/7856661.html




## 杂项讨论

qemu版本： 2.7.0

### file协议/raw格式的命名问题

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
**(17年11月7日更新：从2.9.0开始已经把名字这样改了)**

这样修改防止造成混乱：因为驱动分两种驱动：protocol block driver和format block driver,现在还不太理解，有的信息是：

1. 
> main difference should be that bdrv_file_open() is invoked for protocol block drivers, whereas bdrv_open() is invoked for format block drivers（[参考 qemu-devel 的一个讨论](https://lists.gnu.org/archive/html/qemu-devel/2014-10/msg01938.html)）

2. raw-posix.c和raw-win32.c 中的`bdrv_file`中定义了`.format_name:"file"`和`.protocol_name:"file"`, 属于protocol block driver；而raw_bsd.c和qcow.c、qcow2.c等文件中的`bdrv_raw`、`bdrv_qcow2`等这些数据结构只定义了`.format_name:"raw"` / `.format_name:"qcow2"` 这些，属于format block driver。`bdrv_file`和`bdrv_raw`数据结构的定义如下：
```cpp
// block/raw-posix.c
bool aio_poll(AioContext *ctx, bool blocking)
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

### 大致io流走向


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
1.1.(ide) start_thread --> kvm_handle_io --> ... --> blk_aio_prwv --> [submit blk_aio_read_entry() to coroutine]
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

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1.2.(virtio) main --> main_loop --> ... --> glib_pollfds_poll --> ... --> virtio_queue_host_notifier_aio_read  --> ... --> blk_aio_prwv --> [submit blk_aio_read_entry() to coroutine]
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#0  blk_aio_prwv (blk=0x555556a6ff30, offset=0x0, bytes=0x200, qiov=0x555557dabe40, co_entry=0x555555b58df1 <blk_aio_read_entry>, flags=0, cb=0x5555557ce850 <virtio_blk_rw_complete>, opaque=0x555557dabde0) at block/block-backend.c:995
#1  blk_aio_preadv (blk=0x555556a6ff30, offset=0x0, qiov=0x555557dabe40, flags=0, cb=0x5555557ce850 <virtio_blk_rw_complete>, opaque=0x555557dabde0) at block/block-backend.c:1100
#2  submit_requests (blk=0x555556a6ff30, mrb=0x7fffffffdef0, start=0x0, num_reqs=0x1, niov=0xffffffff) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/block/virtio-blk.c:361
#3  virtio_blk_submit_multireq (blk=0x555556a6ff30, mrb=0x7fffffffdef0) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/block/virtio-blk.c:391
#4  virtio_blk_handle_vq (s=0x555556a54530, vq=0x555557ce6800) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/block/virtio-blk.c:600
#5  virtio_blk_data_plane_handle_output (vdev=0x555556a54530, vq=0x555557ce6800) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/block/dataplane/virtio-blk.c:158
#6  virtio_queue_notify_aio_vq (vq=0x555557ce6800) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/virtio/virtio.c:1243
#7  virtio_queue_host_notifier_aio_read (n=0x555557ce6860) at /home/jaycee/qemu-io_test/qemu-2.8.0/hw/virtio/virtio.c:2046
#8  aio_dispatch (ctx=0x555556a48530) at aio-posix.c:325
#9  aio_ctx_dispatch (source=0x555556a48530, callback=0x0, user_data=0x0) at async.c:254
#10 g_main_context_dispatch () from /lib/x86_64-linux-gnu/libglib-2.0.so.0
#11 glib_pollfds_poll () at main-loop.c:215
#12 os_host_main_loop_wait (timeout=0x2ef996c8) at main-loop.c:260
#13 main_loop_wait (nonblocking=0x0) at main-loop.c:508
#14 main_loop () at vl.c:1966
#15 main (argc=0xb, argv=0x7fffffffe618, envp=0x7fffffffe678) at vl.c:4684



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

> [KVM虚拟机IO处理过程(一) ----Guest VM I/O 处理过程](http://blog.csdn.net/dashulu/article/details/16820281)

> [KVM虚拟机IO处理过程(二) ----QEMU/KVM I/O 处理过程](http://blog.csdn.net/dashulu/article/details/17090293)

### IOthread的polling [1]

QEMU 的 iothread 会一直进行polling。但是polling并非用了一种机制，而是如[1]所述的一种动态调整的忙等/epoll机制。

```cpp

static void *iothread_run(void *opaque)
{
    //.............
    while (iothread->running) {
        aio_poll(iothread->ctx, true);
        if (iothread->running && atomic_read(&iothread->run_gcontext)) {
            g_main_loop_run(iothread->main_loop);
        }
    }
    //..............
}
```

一般iothread poll的是aio完成事件[2][3]以及virtqueue guest到host通知的ioeventfd请求事件。这种polling**首先**会在用户态ppoll，这会占用更多CPU，若timeout时间内没有完成，**转为**epoll，这里epoll并非在用户态CPU忙等轮询，epoll的实现决定于内核，所以并非占用CPU进行低延迟轮询，其实还是内核事件机制。在aio_poll函数调用的aio_epoll函数中，会进行一定时间的qemu用户态高效polling，然后是基于linux AIO epoll的IO完成事件事件polling(如下代码)。其中qemu_poll_ns(ppoll)返回值大于零说明poll到事件。

```cpp
static int aio_epoll(AioContext *ctx, GPollFD *pfds,
                     unsigned npfd, int64_t timeout)
{
    // ............
    if (timeout > 0) {
        ret = qemu_poll_ns(pfds, npfd, timeout);
    }
    if (timeout <= 0 || ret > 0) {
        ret = epoll_wait(ctx->epollfd, events,
                         ARRAY_SIZE(events),
                         timeout);
        if (ret <= 0) {
            goto out;
        }
        for (i = 0; i < ret; i++) {
            int ev = events[i].events;
            node = events[i].data.ptr;
            node->pfd.revents = (ev & EPOLLIN ? G_IO_IN : 0) |
                (ev & EPOLLOUT ? G_IO_OUT : 0) |
                (ev & EPOLLHUP ? G_IO_HUP : 0) |
                (ev & EPOLLERR ? G_IO_ERR : 0);
        }
    }
    // .............
}
```

并且第一步的qemu用户态polling的时间是自适应的[1]，如下是aio_poll随后对polling时间的调整流程：

```cpp
// QEMU_PATH/util/aio-posix.c

bool aio_poll(AioContext *ctx, bool blocking) 
{
    //.............

    /* Adjust polling time */
    if (ctx->poll_max_ns) {
        int64_t block_ns = qemu_clock_get_ns(QEMU_CLOCK_REALTIME) - start;

        if (block_ns <= ctx->poll_ns) {
            /* This is the sweet spot, no adjustment needed */
        } else if (block_ns > ctx->poll_max_ns) {
            /* We'd have to poll for too long, poll less */
            int64_t old = ctx->poll_ns;

            if (ctx->poll_shrink) {
                ctx->poll_ns /= ctx->poll_shrink;
            } else {
                ctx->poll_ns = 0;
            }

            trace_poll_shrink(ctx, old, ctx->poll_ns);
        } else if (ctx->poll_ns < ctx->poll_max_ns &&
                   block_ns < ctx->poll_max_ns) {
            /* There is room to grow, poll longer */
            int64_t old = ctx->poll_ns;
            int64_t grow = ctx->poll_grow;

            if (grow == 0) {
                grow = 2;
            }

            if (ctx->poll_ns) {
                ctx->poll_ns *= grow;
            } else {
                ctx->poll_ns = 4000; /* start polling at 4 microseconds */
            }

            if (ctx->poll_ns > ctx->poll_max_ns) {
                ctx->poll_ns = ctx->poll_max_ns;
            }

            trace_poll_grow(ctx, old, ctx->poll_ns);
        }
    }

    //.............
}
```


---

[1] S. Hajnoczi, “Applying Polling Techniques to QEMU,” KVM Forum 2017.

[2] QEMU下的eventfd机制及源代码分析, http://oenhan.com/qemu-eventfd-kvm

[3] Linux native AIO与eventfd、epoll的结合使用, http://www.lenky.info/archives/2013/01/2183



