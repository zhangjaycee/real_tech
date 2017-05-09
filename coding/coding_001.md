# 关于Zlib

> [zlib: Differences Between the `deflate` and `compress` Functions]http://stackoverflow.com/questions/10166122/zlib-differences-between-the-deflate-and-compress-functions
>
> [deflate和inflate用法] http://zlib.net/zlib_how.html
>
> [compress和uncompress用法] http://blog.chinaunix.net/uid-24599332-id-2122842.html

zlib的inflate和deflate是相对应的过程，inflate是解压的一个过程，deflate是压缩的一个过程


linux下使用zlib时，需要安装zlib-devel，编译时加`-lz`来链接。