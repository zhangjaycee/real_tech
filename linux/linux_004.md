# Memory-mapped IO(MMIO)和mmap()函数

MMIO就是把文件对象映射到内存。MMIO主要用mmap()于msync()函数，msync之于mmap，类似于fsync之于write，用于将内容马上刷到磁盘上。

#### 1. 普通文件映射 (file-backed mmapping)

mmap简单的应用是把一个普通文件映射到一段内存buffer，这样，读写这段buffer的时候，就会发生文件的读写，换页是“按需“（lazy）进行的。mmap返回的内存时内核空间内存，而不是用户空间的，所以读写频繁时，mmap相对于read/write，不用内核和用户空间间的额外内存拷贝，直接操作page cache(内核空间)内存，效率应该更高。

例如，实现一个类似于cp命令的程序，对于mmap，只需要映射源和目标两个文件到一个地址（进程的一个缓冲区），然后用memcpy就可以完成从一个内核缓冲区(page cache)到内核另一个缓冲区的拷贝；而不用像read和write拷贝一样先把内容从内核缓冲区拷贝到程序（用户空间）缓冲区，然后再拷贝回内核缓冲区。

#### 2. 设备映射 (MMIO)

若设备驱动支持mmap的情况下，使用mmap可能会将设备文件的内存或者寄存器映射到用户进程的内存空间中。

#### 3. 匿名映射和进程内存共享&通信 (anonymous mapping)

传入某些参数后， mmap 函数也可以从OS申请内存，OS会在你的程序中创建匿名(anonymous)内存区域（一个和swap space相关的区域，而不是某个文件），这个区域可以像Heap一样进行管理。

具有亲缘关系的进程之间可以利用mmap进行通信，这时，fd参数应该设置为-1。

---

[1] mmap与read/write的区别, http://www.cnblogs.com/beifei/archive/2011/06/12/2078840.html)

[2] APUE p422

[3] LDD Chapter 15

[4] mmap File-backed mapping vs Anonymous mapping in Linux, https://stackoverflow.com/questions/41529420/mmap-file-backed-mapping-vs-anonymous-mapping-in-linux