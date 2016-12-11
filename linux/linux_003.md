## 编译Linux内核

> [Linux-4.4-x86_64 内核配置选项简介 - 金步国](http://www.jinbuguo.com/kernel/longterm-linux-kernel-options.html)

> Enable cleancache driver to cache clean pages if tmem is present
CONFIG_CLEANCACHE
Cleancache是内核VFS层新增的特性,可以被看作是内存页的"Victim Cache"(受害者缓存),当回收内存页时,先不把它清空,而是把其加入到内核不能直接访问的"transcendent memory"中,这样支持Cleancache的文件系统再次访问这个页时可以直接从"transcendent memory"加载它,从而减少磁盘IO的损耗.目前只有zcache和XEN支持"transcendent memory",不过将来会有越来越多的应用支持.开启此项后即使此特性不能得到利用,也仅对性能有微小的影响,所以建议开启.更多细节请参考"Documentation/vm/cleancache.txt"文件.
Enable frontswap to cache swap pages if tmem is present
CONFIG_FRONTSWAP
Frontswap是和Cleancache非常类似的东西,在传统的swap前加一道内存缓冲(同样位于"transcendent memory"中).目的也是减少swap时的磁盘读写.CONFIG_ZSWAP依赖于它,建议开启.