# Memory-mapped IO(MMIO)和mmap()函数

MMIO就是把文件对象映射到内存。MMIO主要用mmap()于msync()函数，msync之于mmap，类似于fsync之于write，用于将内容马上刷到磁盘上。

#### 1. 普通文件映射 (file-backed mmapping)

mmap简单的应用是把一个普通文件映射到一段内存buffer，这样，读写这段buffer的时候，就会发生文件的读写，换页是“按需“（lazy）进行的。mmap返回的内存时内核空间内存，而不是用户空间的，所以读写频繁时，mmap相对于read/write，不用内核和用户空间间的额外内存拷贝，直接操作page cache(内核空间)内存，效率应该更高。

例如，实现一个类似于cp命令的程序，对于mmap，只需要映射源和目标两个文件到一个地址（进程的一个缓冲区），然后用memcpy就可以完成从一个内核缓冲区(page cache)到内核另一个缓冲区的拷贝；而不用像read和write拷贝一样先把内容从内核缓冲区拷贝到程序（用户空间）缓冲区，然后再拷贝回内核缓冲区。

在NVM中运用mmap，虽然会去除I/O栈，但还是无法避免内存的page fault、page table construction等开销。[1]

* mmap 和 page fault:

内存page有三种状态：[3]
```
(1) unmapped: if the program has not written to the memory region since requesting its allocation, then it is by definition filled with all-zeroes. The Operating System does not have to store it at all, since it knows it’s just filled with zero bytes. Thus the OS will just mark the page as ‘unmapped’ until the program actually writes to it. Thus, on most Operating Systems, when you allocate “memory”, the OS will give you an address range but won’t actually map it to physical storage (yet).

(2) resident: the page corresponds to a page in RAM.

(3) swapped: the page corresponds to a page that has been swapped to disk.
```
访问一个页时，应在状态(2)。

状态(1)会引起minor page fault，这时虽然被分配了，但是进程还没有读写过对应的线性区(memory region)，所以读写时会产生一次minor page fault。

状态(3)会引起major page fault，需要磁盘IO来恢复页, minor page fault指

---

[1] J. Choi and J. Kim, “Efficient Memory Mapped File I / O for In-Memory File Systems.” (Slides:https://www.usenix.org/sites/default/files/conference/protected-files/hotstorage17_slides_choi.pdf)

[2] http://imagewzh.blogspot.com/2010/03/page-fault-and-mmap_21.html

[3] https://frogatto.com/2009/10/30/what-every-programmer-should-know-about-memory-management/

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