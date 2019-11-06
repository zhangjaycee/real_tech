# 代码性能分析和监控

# perf


### 实时事件监控

```bash
perf stat MY_PROGRAM
```

### 热点分析：
先record再report。

```bash
perf record MY_PROGRAM
perf report
```

# go 语言自带性能分析工具

go自带的test 和 tool pprof可以作profiling[1]：
 
例子：
```bash
go test -cpuprofile=cpu.out -blockprofile=block.out
# 结果打印在命令行
go tool pprof --text MY_PROGRAM cpu.out
# 结果生成PDF图片
go tool pprof --pdf MY_PROGRAM cpu.out > cpu.pdf
```

---
[1] https://godoc.org/github.com/pkg/profile