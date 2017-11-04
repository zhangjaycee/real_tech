# Linux内核调试、追踪工具(kprobe/perf/ftrace)

## kprobe
[使用 Kprobes 调试内核] https://www.ibm.com/developerworks/cn/linux/l-kprobes.html

## perf
[Perf -- Linux下的系统性能调优工具，第 1 部分] https://www.ibm.com/developerworks/cn/linux/l-cn-perf1/index.html

[Perf -- Linux下的系统性能调优工具，第 2 部分] 
https://www.ibm.com/developerworks/cn/linux/l-cn-perf2/index.html


## ftrace
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


## crash

内核分析工具
http://people.redhat.com/anderson/