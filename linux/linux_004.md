# Memory-mapped IO(MMIO)和mmap()函数

MMIO就是把文件对象映射到内存。MMIO主要用mmap()于msync()函数，msync之于mmap，类似于fsync之于write，用于将内容马上刷到磁盘上。

## 1. 普通文件映射 (file-backed mmapping)

mmap简单的应用是把一个普通文件映射到一段内存buffer，这样，读写这段buffer的时候，就会发生文件的读写，换页是“按需“（lazy）进行的。若mmap的是文件，那么返回的指针所指向的内存在内核空间分配(page cache?)，而不在用户进程的堆中，所以读写频繁时，mmap相对于read/write，没有内核page cache和用户进程堆间的额外内存拷贝，直接操作page cache(内核空间)内存，效率应该更高。

例如，实现一个类似于cp命令的程序，对于mmap，只需要映射源和目标两个文件到一个地址（进程的一个缓冲区），然后用memcpy就可以完成从一个内核缓冲区(page cache)到内核另一个缓冲区的拷贝；而不用像read和write拷贝一样先把内容从内核缓冲区拷贝到程序（用户空间）缓冲区，然后再拷贝回内核缓冲区。

在NVM中运用mmap，虽然会去除I/O栈，但还是无法避免内存的page fault、page table construction等开销。[1] (关于page fault， 详见另一wiki页： [Page fault](https://github.com/zhangjaycee/real_tech/wiki/linux_031))

### 1.1 重映射

重点关注 [mremap](http://man7.org/linux/man-pages/man2/mremap.2.html) 系统调用。

```cpp
       void *mremap(void *old_address, size_t old_size,
                    size_t new_size, int flags, ... /* void *new_address */);
```

可以扩大或者缩小原来的映射区，区域整体的addr地址也可能随之改变。

### 1.2 非线性映射

重点关注 [remap_file_pages](http://man7.org/linux/man-pages/man2/remap_file_pages.2.html) 系统调用。

可以改变已映射文件各个page区域和addr地址的对应关系，使之不是线性映射。[3]中有个例子是将已经映射的文件段按page为粒度前后颠倒。

```cpp
       int remap_file_pages(void *addr, size_t size, int prot,
                            size_t pgoff, int flags);
```

addr 是要改变位置的目的地址，应该在之前的mmap调用所映射的范围内；pgoff是要改变的位置的源地址，只不过是以mmap所映射的addr开始的page粒度的偏移量；size则是要重新映射位置的区域的大小。详细可以看[3]中例子。

size和addr都要是page size的整数倍，而源地址pgoff直接用page粒度的offset表示所以其地址肯定也是page size的整数倍。

但是这个接口处于弃用状态，可以用多次的mmap调用代替！

---

[1] J. Choi and J. Kim, “Efficient Memory Mapped File I / O for In-Memory File Systems.” (Slides:https://www.usenix.org/sites/default/files/conference/protected-files/hotstorage17_slides_choi.pdf)

[2] http://imagewzh.blogspot.com/2010/03/page-fault-and-mmap_21.html

[3] https://www.technovelty.org/linux/remap_file_pages-example.html

## 2. 设备映射 (MMIO)

若设备驱动支持mmap的情况下，使用mmap可能会将设备文件的内存或者寄存器映射到用户进程的内存空间中。

## 3. 匿名映射和进程内存共享&通信 (anonymous mapping)

传入某些参数后， mmap 函数也可以从OS申请内存，OS会在你的程序中创建匿名(anonymous)内存区域（一个和swap space相关的区域，而不是某个文件），这个区域可以像Heap一样进行管理。

具有亲缘关系的进程之间可以利用mmap进行通信，这时，fd参数应该设置为-1。

---

[1] mmap与read/write的区别, http://www.cnblogs.com/beifei/archive/2011/06/12/2078840.html)

[2] APUE p422

[3] LDD Chapter 15

[4] mmap File-backed mapping vs Anonymous mapping in Linux, https://stackoverflow.com/questions/41529420/mmap-file-backed-mapping-vs-anonymous-mapping-in-linux