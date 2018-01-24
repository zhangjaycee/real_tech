# 分散/聚集 I/O(scatter-gather I/O)


## 1. 定义
readv、 writev、 preadv、 pwritev这些函数名字比一般的函数多一个v，称为分散-聚集IO。v的意思是vector，其将原来的缓冲区参数换成一个iov缓冲区向量(数组)，iov数组的每个元素是一个存储有buffer地址--长度对(iov_base--iov_len)的数据结构struct iov:

```cpp
struct iovec {
        char   *iov_base;  /* Base address. */
        size_t iov_len;    /* Length. */
};
```

对于IO，其实就是内存对持久存储的读写，这些由于iov数组中每个元素是可以不连续的，所以，内存就可以将不连续的内存区域中的数据 **聚集写(gather write)** 到存储设备中，或者从存储设备 **分散读(scatter)** 入不连续的内存区域中。

## 2. 优缺点

摘抄[1]：
```
除了同时操作多个缓冲区外，readv/writev函数功能和read/write函数功能一致。

与线性 I/O 相比，分散/聚集 I/O 的优势：

编码模式更自然

如果数据本身是分段的（比如预定义的结构体的变量），向量 I/O 提供了直观的数据处理方式。

效率更高

单个向量 I/O 操作可以取代多个线性 I/O 操作。

性能更好

除了减少了发起的系统调用次数，通过内部优化，向量 I/O 可以比线性 I/O 提供更好的性能。

支持原子性

和多个线性 I/O 操作不同，一个进程可以执行单个向量 I/O 操作，避免了和其他进程交叉操作的风险。
```

---

[1] 分散/聚集 I/O(scatter-gather I/O), http://blog.csdn.net/u012432778/article/details/47323805