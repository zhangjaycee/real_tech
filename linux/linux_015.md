# Linux Block Layer中的I/O队列和调度器

Linux Block layer 中有几个重要的概念：请求、请求队列、调度器(调度程序，调度算法)等。

## 1. 块IO请求(bio request)

`submit_bio`函数负责传递bio实例，然后调用`generic_make_request`函数创建新的request，`__generic_make_request`函数是块层的通用实现，具体分三步工作:[1-p567][2]
1. `bdev_get_queue`找到涉及的块设备对应的**request queue**。
2. `blk_partition_map`重新映射该请求。
3. `q->make_request_fn`用来根据bio产生request并插入到**request queue**中，一般会调用内核标准的`__make_request`函数

(最新内核中没有"__make_request"这个函数，从内核版本3.1改名叫`blk_queue_bio`了；blk_mq出来之后，其和原来的io scheduler处于同等地位，因此有了`blk_mq_make_request`这个函数，`blk_queue_bio`和`blk_mq_make_request`这两个较为通用的函数和其他"make_request_fn"一样都通过blk_queue_make_request()函数进行注册，其中`blk_queue_bio`在`block/blk-core.c`中，`blk_mq_make_request`在`block/blk-mq.c`中。

？blk_mq_make_request 不再是把bio请求放入原来单一的**request queue**中，而是放入blk-mq的多队列software staging queue中)

4.13内核中，使用了blk_queue_make_request注册make_request_fn函数的文件如下：
```
arch/m68k/emu/nfblock.c|126| <<nfhd_init_one>> blk_queue_make_request(dev->queue, nfhd_make_request);
arch/powerpc/sysdev/axonram.c|263| <<axon_ram_probe>> blk_queue_make_request(bank->disk->queue, axon_ram_make_request);
arch/xtensa/platforms/iss/simdisk.c|277| <<simdisk_setup>> blk_queue_make_request(dev->queue, simdisk_make_request);


block/blk-core.c|990| <<blk_init_allocated_queue>> blk_queue_make_request(q, blk_queue_bio);
block/blk-mq.c|2347| <<blk_mq_init_allocated_queue>> blk_queue_make_request(q, blk_mq_make_request);


drivers/block/brd.c|428| <<brd_alloc>> blk_queue_make_request(brd->brd_queue, brd_make_request);
drivers/block/drbd/drbd_main.c|2845| <<drbd_create_device>> blk_queue_make_request(q, drbd_make_request);
drivers/block/null_blk.c|767| <<null_add_dev>> blk_queue_make_request(nullb->q, null_queue_bio);
drivers/block/pktcdvd.c|2474| <<pkt_init_queue>> blk_queue_make_request(q, pkt_make_request);
drivers/block/ps3vram.c|758| <<ps3vram_probe>> blk_queue_make_request(queue, ps3vram_make_request);
drivers/block/rsxx/dev.c|286| <<rsxx_setup_dev>> blk_queue_make_request(card->queue, rsxx_make_request);
drivers/block/umem.c|897| <<mm_pci_probe>> blk_queue_make_request(card->queue, mm_make_request);
drivers/block/zram/zram_drv.c|1160| <<zram_add>> blk_queue_make_request(queue, zram_make_request);

drivers/lightnvm/core.c|283| <<nvm_create_tgt>> blk_queue_make_request(tqueue, tt->make_rq);
drivers/md/bcache/super.c|805| <<bcache_device_init>> blk_queue_make_request(q, NULL);
drivers/md/dm.c|2068| <<dm_setup_md_queue>> blk_queue_make_request(md->queue, dm_make_request);
drivers/md/md.c|5268| <<md_alloc>> blk_queue_make_request(mddev->queue, md_make_request);
drivers/nvdimm/blk.c|266| <<nsblk_attach_disk>> blk_queue_make_request(q, nd_blk_make_request);
drivers/nvdimm/btt.c|1292| <<btt_blk_init>> blk_queue_make_request(btt->btt_queue, btt_make_request);
drivers/nvdimm/pmem.c|369| <<pmem_attach_disk>> blk_queue_make_request(q, pmem_make_request);
drivers/s390/block/dcssblk.c|633| <<dcssblk_add_store>> blk_queue_make_request(dev_info->dcssblk_queue, dcssblk_make_request);
drivers/s390/block/xpram.c|352| <<xpram_setup_blkdev>> blk_queue_make_request(xpram_queues[i], xpram_make_request);
```

```
From c20e8de27fef9f59869c81c288ad6cf28200e00c Mon Sep 17 00:00:00 2001
From: Jens Axboe <jaxboe@fusionio.com>
Date: Mon, 12 Sep 2011 12:03:37 +0200
Subject: block: rename __make_request() to blk_queue_bio()

Now that it's exported, lets put it in a more sane namespace.

Signed-off-by: Jens Axboe <jaxboe@fusionio.com>
```

然后`__make_request`函数又分为几步：
1. 由bio新创建的请求后，首先检查IO scheduler的queue(elv_queue)是不是空的
2. 
3. 
...


[1] UTLK

[2] PLKA

## 2.1 Block Layer -- I/O Scheduler

### 单队列

block layer 中，分为请求队列(**request queue**)和调度队列(**dispatch queue**)。如第1节所说，**request queue**是用于接收上层发来bio请求，而调度队列是**request queue**的`struct list_head queue_head`字段，是经过IO电梯调度之后的结果队列。虽然下边所说的很多调度算法在调度过程中都用到了多个队列来辅助IO请求重排，但是**request queue**和**dispatch queue**都是但队列的(single-queue)。

### 调度算法

* CFQ(complete fairness queue): 多个请求队列，用hash将一个进程号的请求发到一个请求队列（因此，一个进程常发到一个队列）。

* deadline: 有4个请求队列。其中有一对分别是放读写请求队列(排序队列)；另一对是按最后期限排列的读写请求队列(deadline队列)。

  * 注意：这里读请求的超时时间(比如500ms)一般比写请求的超时时间长(比如5s)，这是由于读一般都是阻塞调用的。

* Anticipatory("预期", 默认算法[2]): 类似deadline，但加入了一些启发式准则。

  * (空间局部性？)比如，在合适的情况下，排序队列的有可能选择当前位置之后的一个请求，使磁头从后搜索。
  * (时间局部性？)比如根据一个进程的统计信息，如果确定这个进程很快发来一个请求，可以延迟一小段时间(比如7ms)。

* noop(no operation): 简单的FIFO，直接插入到调度队列的末尾。

#### Linux系统中修改调度算法的方法：
```
# 比如修改`/dev/sda`的调度算法为noop
echo 'noop' > /sys/block/sda/queue/scheduler
```

[1] Using the Deadline IO Scheduler, https://access.redhat.com/solutions/32376

[2] UTLK

## 2.2 Block Layer -- blk-mq (block multi-queue)

### 多队列

根据multi-queue的paper[1]，作者将原来的block layer的一个queue(request queue)，分为两层多个queue，分别称为software queue和hardware queue：

* **Software staging queues**: 对应原先的一个**request queue**，现在是一个核或一个socket一个queue。负责接收上层的bio请求。由于现在CPU都有较大的L3缓存，所以一个socket一个queue效果就比较好。

* **Hardware dispatch queues**: 数量决定于每个device driver支持多少个queue，比如NVMe设备和驱动支持多个CQ / SQ，所以这时**hardware dispatch queues**就可能和每对CQ/SQ 1:1对应或N:1对应[4]。而原先的单队列块层中，附属于请求队列**request queue**的调度队列**dispatch queue**和只是和设备(而非设备的某对CQ/SQ)1:1对应的关系。**hardware dispatch queues**不能进行重排序调度，只能由device driver进行FIFO操作，这样减少了锁。需要注意的是，即使在不支持多对CQ/SQ的device driver上用blk-mq，也是可以的，这时只要在 **Hardware dispatch queues**提交到device driver SQ时，进行多对一的队列合并即可，并且这种操作并不影响顺序、随机在一个延迟数量级的SSD设备(?但会影响HDD慢设备，所以HDD不太合适用blk-mq)。

总之，**software staging queue**对应于原来IO scheduler的**request queue** (是single-queue)，但这里的Software staging queue是multi-queue的，每个核或者socket对应一个queue。**hardware dispatch queues**类似与原来经过io重排的**dispatch queue**的多队列版本。

---

[1] Bjørling, Matias, et al. "[Linux block IO: introducing multi-queue SSD access on multi-core systems.](http://kernel.dk/blk-mq.pdf)" Proceedings of the 6th international systems and storage conference. ACM, 2013.

[2] Linux Multi-Queue Block IO Queueing Mechanism (blk-mq), 
https://www.thomas-krenn.com/en/wiki/Linux_Multi-Queue_Block_IO_Queueing_Mechanism_(blk-mq)

[3] kernel 3.10内核源码分析--块设备层request plug/unplug机制, 
 http://blog.chinaunix.net/xmlrpc.php?r=blog/article&uid=14528823&id=4778396

[4] K. Joshi and P. Choudhary, “Enabling NVMe WRR support in Linux Block Layer,” Hotstorage, 2017.


