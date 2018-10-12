# Linux中的性能调试、函数追踪工具(perf / strace / ftrace / 
 ...)

我们可以将perf看做应用级、strace看做系统调用级、ftrace看做内核级，详细如下：

## perf

---
[1] http://www.brendangregg.com/perf.html

[2] Perf -- Linux下的系统性能调优工具，第 1 部分, https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/index.html

[3] Perf -- Linux下的系统性能调优工具，第 2 部分, 
https://www.ibm.com/developerworks/cn/linux/l-cn-perf2/index.html


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



## crash

内核分析工具
http://people.redhat.com/anderson/

## kprobe
[使用 Kprobes 调试内核] https://www.ibm.com/developerworks/cn/linux/l-kprobes.html