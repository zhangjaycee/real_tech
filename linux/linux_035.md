# Hugepage 和 hugeTLB

### Transparent Hugepage [1]

由 `/sys/kernel/mm/transparent_hugepage/enabled` 决定开启还是关闭：

```
$ cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never
```

---
[1] https://www.kernel.org/doc/Documentation/vm/transhuge.txt