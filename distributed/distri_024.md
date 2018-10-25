# 透明压缩存储

#### EROFS

4.19 内核的 erofs 是华为为安卓机开发的支持透明压缩的只读文件系统，主要针对安卓等嵌入式只读存储设备。现在主要的特点是透明压缩相对以前的“压缩前定长块”设计成了“压缩后定长块”，据说这样可以减少无用数据被解压的“读放大”，压缩算法采用的是修改过的LZ4。有个测试结果，相对ext4优势主要体现在高压缩比情况下随机读，但是存储设备只是HDD和UFS设备，并非高性能SSD设备。

* “压缩前定长块”:[1]
```
   ++-----------++-----------++         ++-----------++-----------++
...||           ||           ||   ...   ||           ||           ||  ... original data
   ++-----------++-----------++         ++-----------++-----------++
    \                         /          \                         /
       \                   /                \                    /
          \             /                      \               /
      ++---|-------++--|--------++       ++-----|----++--------|--++
      ||xxx|       ||  |xxxxxxxx||  ...  ||xxxxx|    ||        |xx||  compressed data
      ++---|-------++--|--------++       ++-----|----++--------|--++

```

* “压缩后定长块”:[1]
```
   |---- varient-length extent ----|------ VLE ------|---  VLE ---|
         /> clusterofs                  /> clusterofs     /> clusterofs /> clusterofs
   ++---|-------++-----------++---------|-++-----------++-|---------++-|
...||   |       ||           ||         | ||           || |         || | ... original data
   ++---|-------++-----------++---------|-++-----------++-|---------++-|
   ++->cluster<-++->cluster<-++->cluster<-++->cluster<-++->cluster<-++
        size         size         size         size         size  
         \                             /                 /            /
          \                      /              /            /
           \               /            /            /
            ++-----------++-----------++-----------++
        ... ||           ||           ||           || ... compressed clusters
            ++-----------++-----------++-----------++
            ++->cluster<-++->cluster<-++->cluster<-++
                 size         size         size
```

* 测试数据(HDD和手机UFS)[1]
```
Some numbers using fixed output compression (VLE, cluster size = block size = 4k) on
the server and Android phone (kirin970 platform):

Server (magnetic disk):

compression  EROFS seq read  EXT4 seq read        EROFS random read  EXT4 random read
ratio           bw[MB/s]       bw[MB/s]             bw[MB/s] (20%)    bw[MB/s] (20%)

  4              480.3          502.5                   69.8               11.1
 10              472.3          503.3                   56.4               10.0
 15              457.6          495.3                   47.0               10.9
 26              401.5          511.2                   34.7               11.1
 35              389.1          512.5                   28.0               11.0
 48              375.4          496.5                   23.2               10.6
 53              370.2          512.0                   21.8               11.0
 66              349.2          512.0                   19.0               11.4
 76              310.5          497.3                   17.3               11.6
 85              301.2          512.0                   16.0               11.0
 94              292.7          496.5                   14.6               11.1
100              538.9          512.0                   11.4               10.8

Kirin970 (A73 Big-core 2361Mhz, A53 little-core 0Mhz, DDR 1866Mhz):

compression  EROFS seq read  EXT4 seq read        EROFS random read  EXT4 random read
ratio           bw[MB/s]       bw[MB/s]             bw[MB/s] (20%)    bw[MB/s] (20%)

  4              546.7          544.3                    157.7              57.9
 10              535.7          521.0                    152.7              62.0
 15              529.0          520.3                    125.0              65.0
 26              418.0          526.3                     97.6              63.7
 35              367.7          511.7                     89.0              63.7
 48              415.7          500.7                     78.2              61.2
 53              423.0          566.7                     72.8              62.9
 66              334.3          537.3                     69.8              58.3
 76              387.3          546.0                     65.2              56.0
 85              306.3          546.0                     63.8              57.7
 94              345.0          589.7                     59.2              49.9
100              579.7          556.7                     62.1              57.7

* currently we use workqueue for the read-ahead process, which is still has some
minor issues and the value of sequential read is effected by work queue scheduling.
```

---
[1] https://lkml.org/lkml/2018/5/31/306

[2] https://lkml.org/lkml/2018/6/1/86