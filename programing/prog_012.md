# 内核中数组的初始化

```cpp
void *sys_call_table[NR_syscalls] = {
    [0 ... NR_syscalls-1] = sys_ni_syscall,
#include <asm/unistd.h>
};
```

参考： https://stackoverflow.com/questions/10071304/what-is-this-style-of-syntax-in-c