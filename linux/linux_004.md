## Memory-mapped IO(mmio)


> [mmap与read/write的区别](http://www.cnblogs.com/beifei/archive/2011/06/12/2078840.html)

> apue p422

例如，实现一个类似于cp命令的程序，对于mmap，只需要映射源和目标两个文件到一个地址（进程的一个缓冲区），然后用memcpy就可以完成从一个内核缓冲区(page cache)到内核另一个缓冲区的拷贝；而不用像read和write拷贝一样先把内容从内核缓冲区拷贝到程序缓冲区，然后再拷贝回内核缓冲区。