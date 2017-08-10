## Cache

### Cache读策略 

* look-aside
同时请求磁盘和cache，如果命中，自然是cache先返回，完成请求；如果没有命中，等待磁盘请求完成即可。


* look-through
先请求cache，若未命中，再访问磁盘


### Cache写策略 

* write-back
写到Cache后就返回，cache再在磁盘空闲时写回到磁盘。

* wirte-through
写到cache后不立即返回，直到数据从cache真正写到磁盘后才返回。这种策略不及write-back快。

### 参考
[An overview of cache(pdf)]  http://download.intel.com/design/intarch/papers/cache6.pdf

[An Introduction to Look-Aside Caching] https://content.pivotal.io/blog/an-introduction-to-look-aside-vs-inline-caching-patterns

