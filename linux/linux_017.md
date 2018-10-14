# Linux中的性能调试、函数追踪工具(perf / strace / ftrace ...)


## 引言

我们可以将perf看做应用级、strace看做系统调用级、ftrace看做内核级，PCM则是硬件微架构级的，详细如下。

Linux还有很多tracer或profilter可以选择。[1]

---
[1] Choosing a Linux Tracer (2015) http://www.brendangregg.com/blog/2015-07-08/choosing-a-linux-tracer.html

## perf -- 对应用的全面性能分析

虽然perf用于分析用户应用，但是其实现涉及内核hook和处理器性能计数器，所以可以对某个程序进行深入的分析。

具体的，perf 利用了内核中的tracepoint和Intel处理器的performance counter unit(PMU)，tracepoint即内核中的hook，触发时会通知perf，perf生成report以便perf用户分析所运行的应用，PMU是一些处理器中的计数器，可以记录cache miss次数、内存访问大小等。

* perf list - 列出事件

用`perf list`可以列出perf可以进行记录的所有事件：
```
$ perf list

branch-instructions OR branches                    [Hardware event]
branch-misses                                      [Hardware event]
...
alignment-faults                                   [Software event]
...
L1-dcache-load-misses                              [Hardware cache event]
...
branch-instructions OR cpu/branch-instructions/    [Kernel PMU event]
```

* perf record 和 perf report

一般可以先用`perf record`记录perf分析所需的数据到`perf.data`，例如：
```bash
#加-g可以记录函数调用关系，-e后接时间名称，用逗号分隔，这里记录了a.out程序
sudo perf record -g -e cpu-clock,topdown-slots-retired ./a.out
```

然后可以用`perf report`进行分析，比如：
```bash
sudo perf report #用perf的控制器查看
sudo perf report --stdio #结果打印到终端
...
```

* perf probe

除了内核、硬件已定好的“静态”事件，还可以创建“动态”事件，比如我们可以为由debuginfo(vmlinux?)的当前内核的某个函数或者某行作为一个“perf event”，之后可以在`perf record`的`-e`选项后用`probe:XXX`来表示，例如：
```bash
# 加入”统计vfs_write这个内核函数的调用次数“的事件
sudo perf probe -v vfs_write
# 统计并分析这个新加入的vfs_write调用事件
sudo perf record -g -e probe:vfs_write ./a.out
sudo perf report --call-graph
``` 

* perf_event_open 系统调用

perf_event_open 是一个perf对应的系统调用，可以在程序代码中调用来查看硬件计数器。 [4]

---
[1] http://www.brendangregg.com/perf.html

[2] Perf -- Linux下的系统性能调优工具，第 1 部分, https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/index.html

[3] Perf -- Linux下的系统性能调优工具，第 2 部分, 
https://www.ibm.com/developerworks/cn/linux/l-cn-perf2/index.html

[4] http://man7.org/linux/man-pages/man2/perf_event_open.2.html

## strace -- 应用程序的系统调用追踪

strace可以追踪一个用户程序调用系统调用的情况，包括调用栈、调用时间等，默认会打印调用栈，例如还是对于程序`hello.c`，运行程序后，运行strace的结果：

```bash
$ strace -p 107917
Process 107917 attached
restart_syscall(<... resuming interrupted call ...>) = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 5), ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fdb2b2c2000
write(1, "hello,\n", 7)                 = 7
rt_sigprocmask(SIG_BLOCK, [CHLD], [], 8) = 0
rt_sigaction(SIGCHLD, NULL, {SIG_DFL, [], 0}, 8) = 0
rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
nanosleep({15, 0}, 0x7fff9946fbf0)      = 0
write(1, "world!\n", 7)                 = 7
exit_group(0)                           = ?
+++ exited with 0 +++
```

若加上参数`-c`会在程序结束时给出每个系统调用所占用了时间（这个时间应该属于system time）。

在Mac 中类似的工具叫做 **dtruss** 。

---

[1] Linux操作系统的pstack工具, http://nanxiao.me/linux-pstack/


## ftrace -- 内核级函数的追踪
(CentOS 7 下的简单用法)

- 1, 创建一个文件夹，比如我创建到了`/debug`，然后挂载debugfs到这个文件夹
```bash
mount -t debugfs nodev /debug
```
- 2, 进入`/debug/tracing`，可以看到很多文件，其中`available_tracers`是可以选择的ftrace tracers，`current_tracer`是当前的tracer，默认是nop，就是没有。可以把一个想用的tracer写到`current_tracer`文件，然后将`1`写入`tracing_on`文件(默认其实就是1，只不过用了nop所以相当于没开)开启追踪。
```
# 检查可用tracers和当前使用的tracer
$> cat available_tracers                                                                                           
blk function_graph wakeup_dl wakeup_rt wakeup function nop
$> cat current_tracer
nop
# 设置并开启tracer
$> echo function > current_tracer
$> echo 1 > tracing_on
```
- 3, 可以打开`/sys/kernel/debug/tracing/trace`文件查看追踪内容，比如我这里用的是`function` tracer，所以可以看到调用关系，这个文件貌似有个最大长度的限制。
```
$> vim /sys/kernel/debug/tracing/trace
```

[1] ftrace 简介, https://www.ibm.com/developerworks/cn/linux/l-cn-ftrace/

[2] Red Hat Guide - Ftrace, https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/developer_guide/ftrace

[3] 使用 ftrace 调试 Linux 内核，第 2 部分, https://www.ibm.com/developerworks/cn/linux/l-cn-ftrace2/index.html

[4] Secrets of the Ftrace function tracer, https://lwn.net/Articles/370423/

## 通过处理器性能计数器进行分析 -- PCM, PAPI, SystemTap ... 

* PCM

processor counter monitor[1] 继承了 Intel Performance Counter Monitor[2] 进行继续开源开发。与perf相比，PCM不只可以使用core的计数器，还可以使用uncore的计数器[2]，这两种counter分别如下。但是现在perf也支持一些uncore计数器了，所以我还不知道PCM相对perf的优势。

>**core**: instructions retired, elapsed core clock ticks, core frequency including Intel® Turbo boost technology, L2 cache hits and misses, L3 cache misses and hits (including or excluding snoops).
>
>**uncore**: read bytes from memory controller(s), bytes written to memory controller(s), data traffic transferred by the Intel® QuickPath Interconnect links.


* PAPI

PAPI[3]的目的是提供一个读取各种硬件计数器的统一API，支持很多计数器，列表在[4]。

* SystemTap



---
[1] https://github.com/opcm/pcm

[2] https://software.intel.com/en-us/articles/intel-performance-counter-monitor

[3] http://icl.cs.utk.edu/projects/papi/wiki/Main_Page

[4] http://icl.cs.utk.edu/projects/papi/wiki/PAPIC:PAPI_presets.3

## crash

内核分析工具
http://people.redhat.com/anderson/

## kprobe
[使用 Kprobes 调试内核] https://www.ibm.com/developerworks/cn/linux/l-kprobes.html