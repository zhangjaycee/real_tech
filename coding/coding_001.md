# 压缩算法分类及对应的实现

## 1. 压缩算法

#### 整数压缩

详见本wiki的 [[整数编码和整数序列的压缩表示|coding_006]]。

#### 字典压缩

LZ77(LZ1) 和 LZ78(LZ2)是常见的字典压缩。

LZ77有一个"sliding window"的概念，假设相似的pattern会相邻出现(局部性？)，这就是说，如果重复模式的周期过大超出窗口，便无法检测到。

LZ78为编解码器维护了固定的字典，解决了LZ77的这个弊端。但是，若不限制字典的增长，字典会太大，因此具体应用时一定要最字典进行削减。LZW是LZ78的一种著名变种。

#### 熵编码

包括Huffman编码和Arithmetic编码，后者压缩效果要优于前者，但是压缩性能会差一些。

关于熵和熵编码压缩的详细讨论间本wiki [[无损压缩能否突破信息熵的限制|coding_007]] 。

#### 游长编码

游长编码(Run-Length Encoding, RLE)，对于连续出现相同字符的情况压缩效果非常好。在Wikipedia的例子中，字符串`WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW`经过RLE可以压缩为`12W1B12W3B24W1B14W`。

## 2. 压缩实现

#### Zlib

zlib的inflate和deflate是相对应的过程，inflate是解压的一个过程，deflate是压缩的一个过程

linux下使用zlib时，需要安装zlib-devel，编译时加`-lz`来链接。

#### LZ4

#### lzbench


---

[1] zlib: Differences Between the deflate and compress Functions, http://stackoverflow.com/questions/10166122/zlib-differences-between-the-deflate-and-compress-functions

[2] deflate和inflate用法, http://zlib.net/zlib_how.html

[3] compress和uncompress用法, http://blog.chinaunix.net/uid-24599332-id-2122842.html

