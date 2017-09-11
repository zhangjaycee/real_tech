## Cache

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

### 参考
[1] An overview of cache(pdf),  http://download.intel.com/design/intarch/papers/cache6.pdf

[2] An Introduction to Look-Aside Caching, https://content.pivotal.io/blog/an-introduction-to-look-aside-vs-inline-caching-patterns

[3] 《深入理解计算机系统(第二版)》中文版 P420


