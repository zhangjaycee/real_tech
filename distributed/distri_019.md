# 概率数据结构

## Bloom Filter


## Cuckoo Filter

* blocked cuckoo filter

为每个哈希key多加几个slot。

* stash cuckoo filter

额外添加一个stash区，如果被踢出的项寻找新位置失败，则存在stash区。这样，在query时，如果两个hash的位置没有找到，还需要查找stash区。


---

[1] http://blog.fastforwardlabs.com/2016/11/23/probabilistic-data-structure-showdown-cuckoo.html

[2] Probabilistic Data Structures for C#, https://github.com/mattlorimor/ProbabilisticDataStructures