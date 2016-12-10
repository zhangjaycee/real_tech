## memory compression

Cleancache和Frontswap算是一个内核中内存压缩的“前端”，Zram、Zswap、Zcache和tmem这些属于”后端“。其中“Zproject”可以用于单机模式下，tmem更侧重xen虚拟化环境中的应用。

### Cleancache & Frontswap

* 参考

> [Cleancache and Frontswap](https://lwn.net/Articles/386090/)

### Zram & Zswap & Zcache

* 参考

> [zram vs zswap vs zcache](http://askubuntu.com/questions/471912/zram-vs-zswap-vs-zcache-ultimate-guide-when-to-use-which-one/472227#472227)

> [In-kernel memory compression](https://lwn.net/Articles/545244/)  [[翻译](http://blog.jcix.top/2016-12-09/inkernel_memory_compression/)]

> [zcache: a compressed page cache](https://lwn.net/Articles/397574/)(Jonathan Corbet)

> [zcache: a compressed file page cache](https://lwn.net/Articles/562254/)(bob liu)

> [LSFMM: In-kernel memory compression](https://lwn.net/Articles/548109/)

> [https://www.kernel.org/doc/Documentation/vm/zswap.txt](https://www.kernel.org/doc/Documentation/vm/zswap.txt)

> [Linux下使用zram（压缩内存）](https://segmentfault.com/a/1190000000380500)

* 现状

目前zram和zswap都在在内核中，而zcache进入过内核，后来被移出，其精简版由bob liu重写，并尝试加入mm模块中。

### Transcendent Memory (tmem)
* 参考

> [Transcendent memory in a nutshell](https://lwn.net/Articles/454795/) [[翻译](http://blog.chinaunix.net/uid-23531402-id-3199889.html)]

> [LINUX PATCH AND ENVIRONMENT FOR XEN TRANSCENDENT MEMORY](https://oss.oracle.com/projects/tmem/dist/documentation/internals/linuxpatch)

> [WHAT IS TRANSCENDENT MEMORY](https://oss.oracle.com/projects/tmem/)

> [kvm: Transcendent Memory (tmem) on KVM](https://groups.google.com/forum/#!starred/linux.kernel/KB2-YfAJhVc) [[github source](https://github.com/akshaykarle/kvm-tmem)]

