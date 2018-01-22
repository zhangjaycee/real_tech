# Memory-mapped IO(MMIO)和mmap()

### mmap()

mmap是把文件映射到一段内存buffer，这样，读写这段buffer的时候，就会发生文件的读写，换页是“按需“（lazy）进行的。

例如，实现一个类似于cp命令的程序，对于mmap，只需要映射源和目标两个文件到一个地址（进程的一个缓冲区），然后用memcpy就可以完成从一个内核缓冲区(page cache)到内核另一个缓冲区的拷贝；而不用像read和write拷贝一样先把内容从内核缓冲区拷贝到程序缓冲区，然后再拷贝回内核缓冲区。

---

[1] mmap与read/write的区别, http://www.cnblogs.com/beifei/archive/2011/06/12/2078840.html)

[2]apue p422

### Memory-mapped I/O (MMIO)

MMIO是把IO设备内存映射到内存地址。