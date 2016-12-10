## zram & zswap & zcache | tmem(transcendent memory)?

> [zram vs zswap vs zcache](http://askubuntu.com/questions/471912/zram-vs-zswap-vs-zcache-ultimate-guide-when-to-use-which-one/472227#472227)

> [Transcendent memory in a nutshell](https://lwn.net/Articles/454795/)

> [LSFMM: In-kernel memory compression](https://lwn.net/Articles/548109/)

> [zcache: a compressed page cache](https://lwn.net/Articles/397574/)(Jonathan Corbet)

> [LINUX PATCH AND ENVIRONMENT FOR XEN TRANSCENDENT MEMORY](https://oss.oracle.com/projects/tmem/dist/documentation/internals/linuxpatch)

> [WHAT IS TRANSCENDENT MEMORY](https://oss.oracle.com/projects/tmem/)

> [Transcendent memory 技术](http://blog.chinaunix.net/uid-23531402-id-3199889.html)

> * [Cleancache and Frontswap](https://lwn.net/Articles/454795/)

>While Cleancache holds the page, it can do creative things with it. Pages with duplicate contents are not uncommon, especially in virtualized situations; often, significant numbers of pages contain only zeroes. The backing store behind Cleancache can detect those duplicates and store a single copy. Compression of stored pages is also possible; there is currently work afoot to implement ramzswap (CompCache) as a Cleancache backend. It might also be possible to use Cleancache as part of a solid-state cache in front of a normal rotating drive.

> * [https://www.kernel.org/doc/Documentation/vm/zswap.txt](https://www.kernel.org/doc/Documentation/vm/zswap.txt)

> [Linux下使用zram（压缩内存）](https://segmentfault.com/a/1190000000380500)

> [In-kernel memory compression](https://lwn.net/Articles/545244/)[[翻译](http://blog.jcix.top/2016-12-09/inkernel_memory_compression/)]

> [zcache: a compressed file page cache](https://lwn.net/Articles/562254/)(bob liu)