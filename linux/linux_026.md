# Linux NVMe Driver

### NVMe driver的multi-queue和block layer的multi-queue

NVMe协议支持多队列 (multiple queue)，这就需要NVMe块设备驱动对其进行实现。而Linux内核中，近年来的block layer中的blk-mq也有类似的思想。现在NVMe driver的实现正好与其是对接的。

blk-mq本wiki中也有介绍([[Linux Block Layer中的I/O队列和调度器|linux_015]])，其用于代替原始的IO scheduler。blk-mq分为software queue和hardware queue，而NVMe driver中又分submission queue(SQ)和completion queue(CQ)，SQ和CQ两部分对应于blk-mq中的hardware queue。


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