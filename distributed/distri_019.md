# 概率数据结构

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

## MinHash

## TopK



---

[1] http://blog.fastforwardlabs.com/2016/11/23/probabilistic-data-structure-showdown-cuckoo.html

[2] Probabilistic Data Structures for C#, https://github.com/mattlorimor/ProbabilisticDataStructures