# 概率数据结构
# 1. 分类
## Bloom Filter

* Counting Bloom filter

* Deletable Bloom filter

* Inverse Bloom filter

* Partitioned Bloom Filter

* Scalable Bloom filter

* Stable Bloom filter

## Cuckoo Filter

[[distri_019_p1.png]]

上图是[1]中提出cuckoo filter的示意图，ab是cuckoo hashing，c是cuckoo filter。其利用了cuckoo hashing的思想，。其中：

~~~
#filter中每个slot存的是fingerprint(x)而非x:
item_x = fingerprint(x)

#位置h1和h2的计算方式：
h1(x) = hash(x)
h2(x) = h1(x) ^ hash(item_x)

#由于异或的可逆性，已知任意一个位置和item_x可以算出另以位置：
hi(x) = hj(x) ^ hash(item_x)
~~~

#### cuckoo filter变种：

* blocked cuckoo filter

为每个哈希key多加几个slot。

* stash cuckoo filter

额外添加一个stash区，如果被踢出的项寻找新位置失败，则存在stash区。这样，在query时，如果两个hash的位置没有找到，还需要查找stash区。

* Dynamic cuckoo filter[2]

[[distri_019_p2.png]]

---

[1] and M. K. Bin Fan, David G. Andersen, “Cuckoo Filter: Better Than Bloom,” ;Login, vol. 38, pp. 36–40, 2013.

[2] H. Chen, L. Liao, H. Jin, and J. Wu, “The Dynamic Cuckoo Filter,” pp. 1–10.

## Count-Min Sketch

## HyperLogLog

## quotient filter

## MinHash

## TopK

---

[1] http://blog.fastforwardlabs.com/2016/11/23/probabilistic-data-structure-showdown-cuckoo.html

[2] Probabilistic Data Structures for C#, https://github.com/mattlorimor/ProbabilisticDataStructures

# 2. 持久化相关：


[1] A. Abraham, P. Krömer, and V. Snášel, “Flash Assisted Segmented Bloom Filter for Deduplication,” Adv. Intell. Syst. Comput., vol. 334, no. November 2014, 2015.

[2] M. Canim, G. Mihaila, and B. Bhattacharjee, “Buffered Bloom filters on solid state storage,” Proc. Int. Work. Acceclerating Data Manag. Syst. using Mod. Process. Storage Archit., pp. 1–8, 2010.

[3] M. Goswami, D. Medjedovic, E. Mekic, and P. Pandey, “Buffered Count-Min Sketch on SSD: Theory and Experiments,” no. Esa, 2018.

[4] B. Debnath, S. Sengupta, J. Li, D. J. Lilja, and D. H. C. Du, “BloomFlash: Bloom filter on flash-based storage,” Proc. - Int. Conf. Distrib. Comput. Syst., pp. 635–644, 2011.

[5] L. Luo, D. Guo, R. T. B. Ma, O. Rottenstreich, and X. Luo, “Optimizing Bloom Filter: Challenges, Solutions, and Comparisons,” pp. 1–34, 2018.

[6] L. Guanlin, B. Debnath, and D. H. C. Du, “A Forest-structured Bloom Filter with flash memory,” IEEE Symp. Mass Storage Syst. Technol., pp. 1–6, 2011.

# 3. 一些相关源码下载：
morton filter (include BF and CF): https://github.com/Roudovic/Filter-Tester/tree/master

cuckoo filter (原版) https://github.com/efficient/cuckoofilter

cuckoo filter 2 https://github.com/begeekmyfriend/CuckooFilter

Counting Quotient Filter: (A General-Purpose Counting Filter, 2017)  https://github.com/splatlab/cqf/tree/master

path hashing https://github.com/Pfzuo/Path-Hashing

(from A General-Purpose Counting Filter: counting quotient filter)

C++ Bloom filter library: https://code.google.com/p/bloom/

Counting Bloom filter source code in C++:   https://github.com/mavam/libbf


