# 文件打洞 (Hole Punching) 及其应用

一个文件的长度和它实际所占用的磁盘空间很可能是不同的，这主要涉及到稀疏文件(sparse file)和文件打洞(hole punching)的概念。这两个特性需要操作系统和文件系统的支持，目前Linux的ext4、XFS等文件系统都支持这两个特性。

### 稀疏文件 (Sparse File)

了解系数文件最直观的例子是，创建一个文件，然后用lseek定位到较大的偏移量，在这个偏移量实际写一些内容，这时实际占用的磁盘空间很小，但文件的长度却比较大。比如：

```cpp
#include <fcntl.h>
#include <assert.h>

int main()
{
    // 打开两个文件file_normal和file_sparse
    int fd = open("file_normal", O_RDWR|O_CREAT, 0755);
    int fd_sparse = open("file_sparse", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);

    // 一个从0写入3个字节，一个从1000偏移写入3个字节
    lseek(fd, 0, SEEK_SET);
    lseek(fd_sparse, 100000, SEEK_SET);
    write(fd, "ABCDEFG", 3);
    write(fd_sparse, "ABCDEFG", 3);
    close(fd);
    close(fd_sparse);
    return 0;
}
```

`ls`的`-s`选项可以在第一列打印出文件所占的磁盘空间：
```bash
zjc@~$ ./sparse_file
zjc@~$ ls -lsh file*
4.0K -rwxr-xr-x. 1 zjc zjc   3 9月  28 11:45 file_normal
4.0K -rwxr-xr-x. 1 zjc zjc 98K 9月  28 11:45 file_sparse
```
可以看到，两个文件的长度分别为3字节和98K字节，但是占用的磁盘空间却是相同的，即文件系统的最小存储单元4 KB。这时因为file_sparse在100000偏移量前根本没有使用磁盘块。

### 文件打洞 (Hole Punching)

上边例子中稀疏文件，是通过在空文件中的某个偏移量写入了3个字节得到的。而某些情况下，一个文件开始并非稀疏的，它已经占用了若干的磁盘空间，这时如果文件中间的一些数据没有用了，我们为了减小文件所占用的磁盘空间，就只能通过文件打洞 (Hole Punching)的方式将非稀疏文件转为稀疏文件。

具体方法是通过`fallocate`系统调用。通过`man 2 fallocate `，我们可以看到`fallocate`调用的原型如下：[1]
```cpp
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <fcntl.h>

int fallocate(int fd, int mode, off_t offset, off_t len);
```
此调用的常规用法可以称为“allocation”： 指定`mode`为0，此时会将文件的[`offset`, `offset+len`)区域的内容写为0。

我们要用它做文件打洞，这种用法可以对应地称为“deallocation”：我们指定`mode`为`FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE`，这时[`offset`, `offset+len`)区域中全零的块就会被“打洞”，从而减小文件的磁盘占用。

正是由于`fallocate`系统调用的“allocation”模式将的文件的一段全置零，所以我们正好可以用这一个调用先“allocation”，再“deallocation”测试文件打洞功能。

**注意**：虽然man page中写明只包含`#include <fcntl.h>`即可，但是在我的CentOS 7系统中还需要包含`linux/falloc.h`，否则会出现以下编译错误：

```bash
hole_punching.c: In function 'main':
hole_punching.c:33:25: error: 'FALLOC_FL_PUNCH_HOLE' undeclared (first use in this function)
     ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
                         ^
hole_punching.c:33:25: note: each undeclared identifier is reported only once for each function it appears in
hole_punching.c:33:46: error: 'FALLOC_FL_KEEP_SIZE' undeclared (first use in this function)
     ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
```

我们测试的例程如下：
```cpp
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
// 注意在CentOS 7中还需要包含linux/falloc.h：
#include <linux/falloc.h>
#include <sys/stat.h>
#include <assert.h>

int main()
{
    off_t offset;
    int ret;
    struct stat st; 

    // do allocation
    printf("===== Allocation =====\n");
    int fd = open("./file_nohole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);

    // do dedallocation
    printf("==== Deallocation ====\n");
    fd = open("./file_withhole", O_RDWR|O_CREAT, 0755);
    assert(fd != -1);
    ret = fallocate(fd, 0 , 0, 1024000);
    ret = fallocate(fd, FALLOC_FL_PUNCH_HOLE|FALLOC_FL_KEEP_SIZE, 409600, 1024000);
    assert(ret == 0); 
    offset = lseek(fd, 0, SEEK_END);
    printf("SEEK_END offset:\t %d\n", offset);
    fstat(fd, &st);
    printf("fstat:\t\t\t file size %d, %d allocated (%d Bytes).\n",
                            st.st_size, st.st_blocks, st.st_blocks * 512);
    close(fd);
    return 0;
}
```
运行结果：
```bash
zjc@~$ ./hole_punching
===== Allocation =====
SEEK_END offset:         1024000
fstat:                   file size 1024000, 2000 allocated (1024000 Bytes).
==== Deallocation ====
SEEK_END offset:         1024000
fstat:                   file size 1024000, 800 allocated (409600 Bytes).

zjc@~$  ls -lsh file*
1000K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_nohole
 400K -rwxr-xr-x. 1 zjc zjc 1000K Sep 28 11:59 file_withhole
```
可以看到无论是用`struct stat`中的`st_blocks`字段还是`ls`的`-s`选项，都告诉我们"file_withhole"这个文件被打出了一个600 KB的洞(1000 K --> 400 K)。


### 打洞在MySQL页压缩中的应用

在我以前的文章中曾经分析过MySQL InnoDB的透明页压缩 [[2]](http://blog.jcix.top/2017-04-16/transparent_page_compression/)，这种压缩机制就是基于文件打洞的。详细可以看下那篇博客，下边在简单说明下：

InnoDB的以InnoDB页为单元进行存储，对于一般的情况，InnoDB页默认为16KB，文件系统默认为4KB。当InnoDB要存储一个页时，会对16KB进行压缩若，压缩后大小为12KB，那么12KB到16KB之间的内容会首先被填零，然后用`fallocate`作“deallocation”打洞，这是额外的一个文件系统块就因压缩而被节约了；同样，若压缩后的页小于8 KB或小于4 KB，那么分别就可以节约8 KB 或 12 KB。


---

[1] fallocate - manipulate file space, http://man7.org/linux/man-pages/man2/fallocate.2.html

[2] MySQL InnoDB透明页压缩的简单分析, [http://blog.jcix.top/2017-04-16/transparent_page_compression/](http://blog.jcix.top/2017-04-16/transparent_page_compression/)