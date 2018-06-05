# 内存操作指令
图片（来自[1]）：

[[prog_018_001.png]]

## 内存排序指令 mfence、sfence、sfence

sfence保证它之前的CPU到内存的store是按顺序执行的，一般在`clflushopt`后使用。类似的，mfence用于load和store，lfence仅用于load。

代码如下：[2]
```cpp
// asm
lfence
sfence
mfence
// c or cpp
void _mm_lfence(void)
void _mm_sfence(void)
void _mm_mfence(void)
```

## 内存操作原子指令

内存原子指令compare-and-swap(CAS)，在x86中的实现称为CMPXCHG (compare-exchange)，CAS指令是实现信号量、互斥量的基础，也是实现一些无锁数据结构的基础。[3]

CAS属于Read-modify-write指令的一种，read-modify-write指的是一组原子指令，包括 test-and-set, fetch-and-add和compare-and-swap。[5]

通过`lock cmpxchg16b`指令，x86最大的内存原子操作单位是16 Bytes，这在不支持它的CPU中也是不可能模拟出来的。内存排序指令(mfense和sfence)无法保证原子性，因为虽然cache line对于一个处理器是原子的，但是每个处理器都有cache，多个处理器的不同线程把cache line刷到相同的内存位置时，还是可能导致中间的分裂（不一致），因此只能用内存原子指令保证8 B或者16 B的原子性。[4]

--- 
[1] D. J. Sorin, “Persistent Memory Programming,” Computer (Long. Beach. Calif)., vol. 50, no. 3, p. 12, 2017.

[2] https://en.wikipedia.org/wiki/Memory_ordering#cite_note-vtune-sfence-10

[3] https://en.wikipedia.org/wiki/Compare-and-swap

[4] https://stackoverflow.com/questions/38219226/what-is-wrong-with-this-emulation-of-cmpxchg16b-instruction

[5] https://en.wikipedia.org/wiki/Read-modify-write