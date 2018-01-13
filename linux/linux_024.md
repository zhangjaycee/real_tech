# Linux 中监控锁的使用情况(Lock stat)


貌似大多数发行版需要重新编译内核才支持这个功能，使用方法：

```
- USAGE

Enable collection of statistics:

# echo 1 >/proc/sys/kernel/lock_stat

Disable collection of statistics:

# echo 0 >/proc/sys/kernel/lock_stat

Look at the current lock statistics:

( line numbers not part of actual output, done for clarity in the explanation
  below )

# less /proc/lock_stat
```

---

[1] Linux 文档, https://www.kernel.org/doc/Documentation/locking/lockstat.txt