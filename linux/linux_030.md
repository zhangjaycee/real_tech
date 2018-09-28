# 文件打洞 (Hole Punching)

文件的长度和文件实际占用的磁盘大小是不同的，这主要是存在一个稀疏文件(sparse file)的概念，稀疏文件中有一个或多个空洞，这些空洞不占用磁盘块。

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
zjc@~$ ls -lsh file*
4.0K -rwxr-xr-x. 1 zjc zjc   3 9月  28 11:45 file_normal
4.0K -rwxr-xr-x. 1 zjc zjc 98K 9月  28 11:45 file_sparse
```
可以看到，两个文件的长度分别为3字节和98K字节，但是占用的磁盘空间却是相同的，即文件系统的最小存储单元4 KB。这时因为file_sparse在100000偏移量前根本没有使用磁盘块。
