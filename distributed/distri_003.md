# 局部性原理及Cache

## 局部性原理

包括空间局部性和时间局部性。硬件层引入高速缓存存储器来缓存指令和数据项，操作系统层用页/块高速缓存缓存磁盘块或文件，应用程序也会用局部性原理提高性能(如浏览器用本地磁盘缓存网络数据)。

对于程序员来说，编写具有良好局部性的程序，更有助于使所编程序从“存储器山”中较高的存储层次获取数据，提高程序的效率。

( UTLK p642有Linux page cache的预读策略，这就是利用了空间局部性。应用page cache缓存文件页本身就是利用了时间局部性。)

paper[1] 中强调了自己用了局部性原理来进行缓存数据换出算法标准的优化：比如“（页面使用频数/请求大小）是同时利用了时间局部性和访问模式，使用频数是时间局部性，请求大小是访问模式”，这里用频数代替LRU能防止弱局部性程序的cache污染问题。

--- 
[1] F. Chen, D. Koufaty, and X. Zhang, “Hystor: making the best use of solid state drives in high performance storage systems,” Ics ’11, pp. 22–32, 2011.

## Cache读写模式

### Cache读策略 

* look-aside
同时请求磁盘和cache，如果命中，自然是cache先返回，完成请求；如果没有命中，等待磁盘请求完成即可。


* look-through
先请求cache，若未命中，再访问磁盘


### Cache写策略 

* write-back

  * 若cache中命中要写的数据块，写到Cache后就返回，cache再在磁盘空闲时写回到磁盘。

  * 若cache中没有命中要写的数据块，先加载进cache再处理。(write-allocate，写匹配)

* wirte-through

  * 若cache中命中要写的数据块，写到cache后不立即返回，直到数据从cache真正写到磁盘后才返回。这种策略不及write-back快。

  * 若cache中没有命中要写的数据块，直接绕过cache将数据写到下一层存储设备。(not-write-allocate，非写匹配)

---

### 参考
[1] An overview of cache(pdf),  http://download.intel.com/design/intarch/papers/cache6.pdf

[2] An Introduction to Look-Aside Caching, https://content.pivotal.io/blog/an-introduction-to-look-aside-vs-inline-caching-patterns

[3] 《深入理解计算机系统(第二版)》中文版 P420

[4] ULTK


## 文件Cache 和 Swap Space

文件Cache(如Linux VFS的page cache)是利用空闲的内存空间用作磁盘数据的缓存，使硬盘读写获得内存的特性（读写更高速，但是内存的随机字节寻址不需要）；坏处是并不持久，如果有改动，需要刷回磁盘。

Swap是利用空闲廉价的磁盘空间来逻辑上增加内存空间，为更多进程正常运行提供内存空间上的保证，这使内存获得了硬盘的特性（大容量，但是存储的持久性是不需要）；缺点是换出的内存再次加载进物理内存很慢。

若外存和内存设备性能差距拉近，则对swap功能更有利；若外存和内存性能差距变大，则文件Cache的特性。

如果内存有了持久特性且价格小于外存，应该就没有外存什么事了。