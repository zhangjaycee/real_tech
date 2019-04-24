# Linux NVMe Driver

### NVMe IO command


**PRP** (Physical Region Page) 的每个entry描述一个物理页，IO command中高端PRP1和PRP2描述要写数据或所需读数据内存在host中的位置。PRP1和PRP2可能直接指向目标page，也可能是目标page的指针。

**SGL** (Scatter/Gather List) 在IO command (SQ entry)中的SGL Entry回事一个SGL Descriptor，多个descriptors会以链表的形式连起来。

SGL和PRP区别是，PRP的每个entry只能映射一个物理页，SGL的一个entry可以是一个连续的不定长范围。

---
[1] http://www.ssdfans.com/blog/2017/08/03/%E8%9B%8B%E8%9B%8B%E8%AF%BBnvme%E4%B9%8B%E4%B8%89/

### NVMe Queues

[[linux_026_001.png]]

如图[1]，逻辑上是环形缓冲区，实际上是线性实现。`Head == Tail`代表Queue为空；`Head == (Tail + 1) % QueueSize`时Queue为满。

---
[1] https://www.flashmemorysummit.com/English/Collaterals/Proceedings/2013/20130812_PreConfD_Marks.pdf


### NVMe driver的multi-queue和block layer的multi-queue

NVMe协议支持多队列 (multiple queue)，这就需要NVMe块设备驱动对其进行实现。而Linux内核中，近年来的block layer中的blk-mq也有类似的思想。现在NVMe driver的实现正好与其是对接的。

blk-mq本wiki中也有介绍([[Linux Block Layer中的I/O队列和调度器|linux_015]])，其用于代替原始的IO scheduler。blk-mq分为software staging queue和hardware dispatch queue[1]，而NVMe driver中又分submission queue(SQ)和completion queue(CQ)，SQ/CQ对应于blk-mq中的hardware dispatch queue。当driver的SQ/CQ较多时，较多时，其可以和hardware dispatch queue 1：1对应，较少时，可能和hardware dispatch queue N：1对应[2]。

---

[1] M. Bjørling, J. Axboe, D. Nellans, and P. Bonnet, “Linux block IO: Introducing Multi-queue SSD Access on Multi-core Systems,” Systor ’13, p. 1, 2013.

[2] K. Joshi and P. Choudhary, “Enabling NVMe WRR support in Linux Block Layer,” Hotstorage, 2017.


### NVMe驱动中multiple Submission Queue的创建

NVMe块存储设备支持 multiple queue (submission queue)。Linux内核中的NVMe驱动中，指定了创建多少个queue的规则：

可以看到`nvme_loop_init_io_queues`函数中有一句`nr_io_queues = min(opts->nr_io_queues, num_online_cpus());`，io queue的数目是根据某种opts（？）和cpu的最小值来确定。`nr_io_queues`被赋值后，后边跟的循环来进行sq (submission queue)初始化。

```cpp
// KERNEL_SRC/drivers/nvme/target/loop.c
static int nvme_loop_init_io_queues(struct nvme_loop_ctrl *ctrl)
{
    struct nvmf_ctrl_options *opts = ctrl->ctrl.opts;
    unsigned int nr_io_queues;
    int ret, i;

    nr_io_queues = min(opts->nr_io_queues, num_online_cpus());
    ret = nvme_set_queue_count(&ctrl->ctrl, &nr_io_queues);
    if (ret || !nr_io_queues)
        return ret;

    dev_info(ctrl->ctrl.device, "creating %d I/O queues.\n", nr_io_queues);

    for (i = 1; i <= nr_io_queues; i++) {
        ctrl->queues[i].ctrl = ctrl;
        ret = nvmet_sq_init(&ctrl->queues[i].nvme_sq);
        if (ret)
            goto out_destroy_queues;

        ctrl->ctrl.queue_count++;
    }   

    return 0;

out_destroy_queues:
    nvme_loop_destroy_io_queues(ctrl);
    return ret;
}
```

这个函数的调用关系：
```cpp
// KERNEL_SRC/drivers/nvme/target/loop.c


// 1) init模块的函数中有名为nvme_loop_transport的nvmf_transport_ops结构
static int __init nvme_loop_init_module(void)
{   
    int ret;
    
    ret = nvmet_register_transport(&nvme_loop_ops);
    if (ret)
        return ret;
    
    ret = nvmf_register_transport(&nvme_loop_transport);
    if (ret)
        nvmet_unregister_transport(&nvme_loop_ops);
    
    return ret;
}   


// 2) 名为nvme_loop_transport中有nvme_loop_create_ctrl函数指针
static struct nvmf_transport_ops nvme_loop_transport = {
    .name       = "loop",
    .create_ctrl    = nvme_loop_create_ctrl,
};


// 3) nvme_loop_create_ctrl函数的调用栈，最后到了nvme_loop_init_io_queue函数
nvme_loop_create_ctrl  
    \-> nvme_loop_create_io_queues 
             \-> nvme_loop_init_io_queues --> nr_io_queues = min(..., ...)



```