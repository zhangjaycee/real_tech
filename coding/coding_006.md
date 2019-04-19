# 整数编码和整数序列的压缩表示

整数编码在搜索引擎索引压缩中非常常用。相对单独的整数编码，倒排表相对更容易压缩。将docs按URL顺序分配ID或者专门的算法进行docID重排后的整数序列通常有较好的压缩效果。

下面的算法中Unary, Binary, Elias Gamma, Elias Delta, Golomb-Rice编码等属于以单个整数位单位的“变长比特码”。而VByte, Simple系列算法则以变长字节或者定长块为单位进行存储。RLE, Elias-Fano等算法适用于整数序列的压缩。PForDelta, Partitioned Elias-Fano等算法更是考虑了倒排索引docID列表的特点。

Golomb-Rice


## Unary (一元) 和 Bianry (二进制)编码

搜索引擎索引中，docID等信息一般为整数，用一元码、二进制编码或者两者的混合表示。

对于整数x，二进制编码一般大家都很熟悉；它的一元编码可以使x-1个0加一个1，或者x-1个1加一个0 (其中x-1也可能是x，取决于实现)。

## Delta Encoding

对于一个有序的序列，可以只存第一个数的原始大小，将后续的数字转换为与前面数字的差值，这样可以减少表示这个整数序列所需要的bit数。

## Elias Gamma和 Elias Delta 编码

Elias Gamma 编码先将数字转成n位的二进制表示，前面加n-1位0，方便解码。

Elias Delta 编码，把前缀0的部分改成γ(|B(x)|)，即x二进制位数的Gamma编码。

## Golomb-Rice 编码

Golomb-Rice这类编码的思想就是用较少的码字表示小数，可以理解成对信源这一种假设：信源中小数出现的概率更大。这也符合熵编码的思想，如果这种假设很接近实际分布，那么我们的压缩效果会比较好。最朴素的Golomb编码便是上面提到的一元码(Unary Code)。Rice编码是复杂一些的一种。

对于Rice编码，R_k(x) 有两部分：
```
1. 商quitient = (x-1)/2^k    (高位)
2. 余数 r = x - q*2^k - 1    (低位)
```
Golomb-Rice 也是两部分：首先q由unary形式表示，r直接用二进制表示。所以|R_k(x)| = q + k + 1。

只要存储参数k，解压也很容易。

## 变长字节压缩 Variable-Byte (VByte) 

由于单纯以bit为单元的"bit-aligned"码会导致现实应用时的性能严重下降，VByte将压缩后的整数存储于不定字节数的单元中。

Variable-Byte (VByte) 是常用的字节对齐码。每个字节中，前7位是数据区，第8位表示数据是否继续到下一个字节。最后一个字节的第8位为0。VByte 对于某个整数最小单元为1Byte，因此压缩率没有优势。但是解压速度有优势，因为每次只要读到小于128的数停下即可(最高位为0)。

Google 的Group-Varint 把VByte的控制位聚集起来。比如，若我们需要4个Bytes，控制位只要2位即可表示4，而不用4位。VByte-G8UI, Masked-VByte and Stream-VByte等也是使用SIMD的变种。

## 块粒度存储压缩 (如Simple9, Simple16)

以定长或变长块为单位，每块独立压缩。对于一个块中的所有整数，都可以用一个b=max-min和一个k=log(max-min)+1 位表示。是一个典型的Binary packing 问题，Simple-9和Simple-16都属于这种块编码。

## PForDelta

由于普通块压缩中max和min可能相差过大，提出找到可以表示90%整数的b和位数k。其他10%用单独的编码器。OptPFD则粒度更细，为每个块都有独立的b和k，压缩率更高，速度慢一点。

## Elias-Fano

## Partitioned Elias-Fano




---

[1] Pibiri, Giulio Ermanno, and Rossano Venturini. "Inverted index compression." Encyclopedia of Big Data Technologies (2018): 1-8.


[2] 《这就是搜索引擎--核心技术详解》