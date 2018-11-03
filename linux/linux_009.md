# 阅读kernel源码

## 1. 查找某个系统调用的定义

系统调用在内核中的定义并不直观，其通过`SYSCALL_DEFINE`系列宏进行定义，在`KERNEL_SRC/include/linux/syscalls.h`中可以看到：
```cpp
#define SYSCALL_DEFINE1(name, ...) SYSCALL_DEFINEx(1, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE2(name, ...) SYSCALL_DEFINEx(2, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE3(name, ...) SYSCALL_DEFINEx(3, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE4(name, ...) SYSCALL_DEFINEx(4, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE5(name, ...) SYSCALL_DEFINEx(5, _##name, __VA_ARGS__)
#define SYSCALL_DEFINE6(name, ...) SYSCALL_DEFINEx(6, _##name, __VA_ARGS__)
```

数字1~6是某个系统调用的参数个数。比如我现在要找mmap这个系统调用在kernel中的定义，由于mmap有6个参数，所以它是这么定义的：
```cpp
YSCALL_DEFINE6(mmap, unsigned long, addr, unsigned long, len,
        unsigned long, prot, unsigned long, flags,
        unsigned long, fd, unsigned long, off)
{
    long error;
    error = -EINVAL;
    if (off & ~PAGE_MASK)
        goto out;

    error = ksys_mmap_pgoff(addr, len, prot, flags, fd, off >> PAGE_SHIFT);
out:
    return error;
}
```
又比如`read`这个系统调用有3个参数，其是这样定义的：
```cpp
SYSCALL_DEFINE3(read, unsigned int, fd, char __user *, buf, size_t, count)
{
    return ksys_read(fd, buf, count);
}
```

可以观察到，定义之内又多调用`ksys_XXX`的函数实现，继续往里看即可。

---
[1] Linux系统调用之SYSCALL_DEFINE, https://blog.csdn.net/hxmhyp/article/details/22699669

## 2. 如何掌握内核的最新特性

* 阅读man page，直接google即可搜索到。

* 一般新出的特性例程很少，但在内核源码`KERNEL_SRC/tools/testing/selftests`文件夹中，很可能有高质量的新特性例程。

* 搜索LKML邮件列表。

## 3. kernel的目录结构

#### 3.1. 整体结构


以下为摘抄[1]：

```
浏览内核代码之前，有必要知道内核源码的整体分布情况，按照惯例，内核代码安装在/usr/src/linux目录下，该目录下的每一个子目录都代表了一个特定的内核功能性子集，下面针对2.6.23版本进行简单描述。

（1）Documentation。
这个目录下面没有内核代码，只有很多质量参差不齐的文档，但往往能够给我们提供很多的帮助。

（2）arch。
所有与体系结构相关的代码都在这个目录以及include/asm-*/目录中，Linux支持的每种体系结构在arch目录下都有对应的子目录，而在每个体系结构特有的子目录下又至少包含3个子目录。

kernel：存放支持体系结构特有的诸如信号量处理和SMP之类特征的实现。

lib：存放体系结构特有的对诸如strlen和memcpy之类的通用函数的实现。

mm：存放体系结构特有的内存管理程序的实现。

除了这3个子目录之外，大多数体系结构在必要的情况下还有一个boot子目录，包含了在这种硬件平台上启动内核所使用的部分或全部平台特有代码。

此外，大部分体系结构所特有的子目录还根据需要包含了供附加特性使用的其他子目录。比如，i386目录包含一个math-emu子目录，其中包括了在缺少数学协处理器（FPU）的CPU上运行模拟FPU的代码。

（3）drivers。
这个目录是内核中最庞大的一个目录，显卡、网卡、SCSI适配器、PCI总线、USB总线和其他任何Linux支持的外围设备或总线的驱动程序都可以在这里找到。

（4）fs。
虚拟文件系统（VFS，Virtual File System）的代码，和各个不同文件系统的代码都在这个目录中。Linux支持的所有文件系统在fs目录下面都有一个对应的子目录。比如ext2文件系统对应的是fs/ext2目录。

一个文件系统是存储设备和需要访问存储设备的进程之间的媒介。存储设备可能是本地的物理上可访问的，比如硬盘或CD-ROM驱动器，它们分别使用ext2/ext3和isofs文件系统；也可能是通过网络访问的，使用NFS文件系统。

还有一些虚拟文件系统，比如proc，它以一个标准文件系统出现，然而，它其中的文件只存在于内存中，并不占用磁盘空间。

（5）include。
这个目录包含了内核中大部分的头文件，它们按照下面的子目录进行分组。

include/asm-*/，这样的子目录有多个，每一个都对应着一个arch的子目录，比如include/asm-alpha、include/asm-arm、include/asm-i386等。每个子目录中的文件都定义了支持给定体系结构所必须的预处理器宏和内联函数，这些内联函数多数都是全部或部分使用汇编语言实现的。

编译内核时，系统会建立一个从include/asm目录到目标体系结构特有的目录的符号链接。比如对于arm平台，就是include/asm-arm到include/asm的符号链接。因此，体系结构无关部分的内核代码可以使用如下形式包含体系相关部分的头文件。

#include <asm/some-file> 
include/linux/，与平台无关的头文件都在这个目录下面，它通常会被链接到目录/usr/include/linux（或者它里面的所有文件会被复制到/usr/include/linux目录下面）。因此用户应用程序里和内核代码里的语句：

#include <linux/some-file> 
包含的头文件的内容是一致的。

include目录下的其他子目录，在此不做赘述。

（6）init。
内核的初始化代码。包括main.c、创建早期用户空间的代码以及其他初始化代码。

（7）ipc。
IPC，即进程间通信（interprocess communication）。它包含了共享内存、信号量以及其他形式IPC的代码。

（8）kernel。
内核中最核心的部分，包括进程的调度（kernel/sched.c），以及进程的创建和撤销（kernel/fork.c和kernel/exit.c）等，和平台相关的另外一部分核心的代码在arch/*/kernel目录。

（9）lib。
库代码，实现了一个标准C库的通用子集，包括字符串和内存操作的函数（strlen、mmcpy和其他类似的函数）以及有关sprintf和atoi的系列函数。与arch/lib下的代码不同，这里的库代码都是使用C编写的，在内核新的移植版本中可以直接使用。

（10）mm。
包含了体系结构无关部分的内存管理代码，体系相关的部分位于arch/*/mm目录下。

（11）net。
网络相关代码，实现了各种常见的网络协议，如TCP/IP、IPX等。

（12）scripts。
该目录下没有内核代码，只包含了用来配置内核的脚本文件。当运行make menuconfig或者make xconfig之类的命令配置内核时，用户就是和位于这个目录下的脚本进行交互的。

（13）block。
block层的实现。最初block层的代码一部分位于drivers目录，一部分位于fs目录，从2.6.15开始，block层的核心代码被提取出来放在了顶层的block目录。

（14）crypto。
内核本身所用的加密API，实现了常用的加密和散列算法，还有一些压缩和CRC校验算法。

（15）security。
这个目录包括了不同的Linux安全模型的代码，比如NSA Security-Enhanced Linux。

（16）sound。
声卡驱动以及其他声音相关的代码。

（17）usr。
实现了用于打包和压缩的的cpio等。
```

#### 3.2.include/uapi目录是干什么的[2]

简单来说，把暴漏给用户的api接口都移到了uapi目录中的相应文件中。

#### 3.3.samples/ 和 tools/ 文件夹是干什么的[3]

---
[1] http://www.cnblogs.com/youngerchina/p/5624501.html

[2] The UAPI header file split, https://lwn.net/Articles/507794/ ([翻译](http://blog.jcix.top/2017-02-24/the_uapi_header_file_split/))

[3] http://unix.stackexchange.com/questions/78714/what-are-some-of-these-directories-in-the-linux-kernel-src

## 4. 追踪git仓库某个文件的历史

clone内核的git仓库，可以利用git的各种功能来看源码的演化历史。这些方法同样适合于其他开源项目。

```
git blame [filename]
```
可以看到这个文件每一行代码对应的commit时间。 
```
git log -p [filename]
```
可以看到包含这个文件修改的所有commit的详细信息。
```
gitk [filename]
```
通过`gitk`图形工具可以对提交信息、代码等进行全面的搜索。

---

[1] View the change history of a file using Git versioning, https://stackoverflow.com/questions/278192/view-the-change-history-of-a-file-using-git-versioning

[2] 使用 GIT 获得Linux Kernel的代码并查看，追踪历史记录, http://blog.csdn.net/caspiansea/article/details/25172615

[3]Install gitk on Mac,  https://stackoverflow.com/questions/17582685/install-gitk-on-mac
