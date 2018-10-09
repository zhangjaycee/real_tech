# Affinity of CPU, cache and memory(资源亲和性/资源绑定，numactl/taskset/cgroups ...)

> Processor and memory binding, also called 'affinity'.[1]

[3]中可以看到Linux affinity管理的内容，包括numactl, taskset，也有OpenMP相关的方法。

## numactl

利用numactl可以将进程和指定的NUMA节点的processor或者memory进行绑定。详见[1,3]。
```bash
# 绑定一个NUMA节点到程序
numactl --cpunodebind=0 <program>
```

## taskset


taskset可以绑定CPU核到指定进程，taskset和numactl的对比在，详见[1,3]。例：

```bash
# 绑定一个核到程序
taskset 0x0001 <program>
```

* 一个将QEMU vCPUs 绑定到核的脚本，方法参考[4]：
https://gist.github.com/zhangjaycee/aa18bc75f671f097f5aee442e5a7115c


## cgroups

（待续、、、）

## Intel Memory Latency Checker

可以测试各个节点CPU到各个节点内存的延迟。

## Cache: Intel CAT (Cache Allocation Technology)[5]

Intel CAT为设置LLC cache进程间的隔离性提供了软件接口。

---
[1] Processor and memory binding, https://www.ibm.com/support/knowledgecenter/en/linuxonibm/liaai.hpctune/cpuandmemorybinding.htm

[2] numactl (8) - Linux Man Pages, https://www.systutorials.com/docs/linux/man/8-numactl/

[3] Managing Process Affinity in Linux, http://www.glennklockwood.com/hpc-howtos/process-affinity.html#3-defining-affinity

[4] (KVM连载)4.1.5 进程的处理器亲和性和VCPU的绑定, http://smilejay.com/2012/08/kvm-vcpu-binding/

[5] https://software.intel.com/en-us/articles/introduction-to-cache-allocation-technology
