# eBPF/BCC [1]

### eBPF和BCC的关系 [1]

eBPF[2](extended Berkeley Packet Filter)是Linux 3.15的新特性。eBPF其实是一种in-kernel的虚拟机，让kprobes能运行用户空间定义的被沙盒的字节码。eBPF前辈最初BPF(也就是著名的tcpdump)是被设计出来作网络抓包和过滤的[4]，eBPF最初也是用于网络包过滤，不过后来人们发现，这种做过sanity-checking的用户态定义的字节码对内核和产品开发者很有用。

BCC(BPF Compiler Collection)，使用了eBPF的用户空间定义字节码特性，让用户写eBPF字节码应用更简单，只要用python或lua就可以完成自己的定制，可以进行性能分析和网络流控制等。而在BCC之前，用户只能将自己的代码和内核代码一起编译，不方便[3]。BCC包括了编写、编译和加载eBPF应用的工具链，BCC也提供了很多已经写好的样例和实用eBPF工具。

### 一些我用过的工具

* stacksnoop (`BCC_PATH/examples/tracing/`) 可以打印出内核函数的调用栈。例如：

```bash
# 当185进程调用ext4_sync_fs时打印调用栈
./stacksnoop -p 185 ext4_sync_fs
```



---

[1] https://github.com/iovisor/bcc


[2] A thorough introduction to eBPF, https://lwn.net/Articles/740157/

[3] An introduction to the BPF Compiler Collection, https://lwn.net/Articles/742082/

[4] http://www.tcpdump.org/papers/bpf-usenix93.pdf