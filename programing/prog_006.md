# hooking & callback的定义和用LD_PRELOAD进行hooking / shimming



根据目前的理解，一般来说：

1. callback技术相当于底层函数留了接口(比如函数参数有一个函数指针)，然后这个底层的函数在适宜的时候调用应用传入的函数。这个传入的函数称为回调函数。

1. 而hooking技术可以更为底层，可能是系统留有后门可以让我们用自己定义的函数代替系统的特定函数，来修改或增加相应底层函数的功能。

1. 总的来说，callback没有改变底层，只是上层告诉了底层一个方法，底层会在适宜的时候进行调用运行；而hooking改变了底层，底层的函数以某种方式被程序员重新定义了，从根本上影响了上层调用相应底层函数的所有应用。

1. 采用preload动态库的方式可以hooking(或者称为shimming[3])。

---
[1] http://www.eluminary.org/en/QnA/Hook_vs_callback_methods__(C++)

[2] https://www.zhihu.com/question/19801131

[3] https://www.quora.com/Is-Shim-computing-a-kind-of-hooking

## 用LD_PRELOAD hook函数

这里以hook read为例子：

* 要被hook的程序`read_to_hook.c`：
```cpp
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    char a[100];
    int fd = open("hello", O_RDWR);
    int ret = read(fd, a, 10);
    close(fd);
    for (int i = 0; i < 10; i++)
        printf("[%c]", a[i]);
    printf("\n%d chs \n", ret);
    return 0;
}
```
* 用来替代hook的假read `lib_for_hook_read.c`(写法参考了[1])
```cpp
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <dlfcn.h>

typedef ssize_t (*real_read_t)(int fd, void *buf, size_t count);
real_read_t real_read;

ssize_t read(int fd, void *buf, size_t count)
{
    if (!real_read)
        real_read = dlsym(RTLD_NEXT, "read");
    printf("in pre-loaded read\n");
    return real_read(fd, buf, count);
}
```

* 效果：
```bash
# 不用hook
zjc@~/test$ gcc read_to_hook.c; ./a.out
[a][a][a][a][a][a][a][a][b][b]
10 chs
# 用hook
zjc@~/test$ gcc -Wall -fPIC -ldl -shared -o pre.so lib_for_hook_read.c
zjc@~/test$ LD_PRELOAD=./pre.so ./a.out
in pre-loaded read
[a][a][a][a][a][a][a][a][b][b]
10 chs
```

---
[1] https://tbrindus.ca/correct-ld-preload-hooking-libc/