# Page fault

## 1. Linux的page fault

内存也可以分为三种状态：[1]

1. **未映射页(unmapped)**: 如果memory region在被程序分配后，没有被写过，那么它会被看作全零的，OS也因此无须找物理页来存这些零。多数OS在内存被分配时将地址范围返回给用户，但是把这些页标记为unmapped，暂不与物理页关联。

2. **驻留页(resident)**：页实实在在在物理RAM中。

3. **换出页(swapped)**：页在RAM中存在过，但现在被换出(swap)到了磁盘中。

访问一个页时，若非状态(2)，会引起page fault，page fault一般又可以分为两种：

1. 状态(1)会引起**minor page fault**，这时虽然被分配了，但是进程还没有读写过对应的线性区(memory region)，所以读写时会产生一次minor page fault。

2. 状态(3)会引起**major page fault**，需要磁盘IO来恢复页。





---
[1] https://frogatto.com/2009/10/30/what-every-programmer-should-know-about-memory-management/

## 2. KVM(EPT)的缺页


## 3. userfaultfd

即用户空间的page fault handler。

要使用此功能，首先应该用userfaultfd调用来创建一个fd，然后用ioctl来配置这个fd，比如可能需要用ioctl-userfaultfd支持的UFFDIO_API、UFFDIO_REGISTER等进行设置。

* 文档

关于userfaultfd系统调用及例子见[1]，关于ioctl设置选项ioctl_userfaultfd见[2]。

---
[1] http://man7.org/linux/man-pages/man2/userfaultfd.2.html

[2] http://man7.org/linux/man-pages/man2/ioctl_userfaultfd.2.html

[3] Caldwell, Blake, et al. "FluidMem: Memory as a Service for the Datacenter." arXiv preprint arXiv:1707.07780 (2017). (https://arxiv.org/pdf/1707.07780.pdf)

[4] The next steps for userfaultfd(), https://lwn.net/Articles/718198/

# 4. 关系图

下面是以`handle_mm_fault`为中心的，上面三方面之间的内核调用关系。mm/fault.c 中的do_page_fault 会调用handle_mm_fault，然后调用关系如图：


```
(mm/memory.c)       (mm/hugetlb.c)                           (fs/userfaultfd.c)
handle_mm_fault -+-> hugetlb_fault --> hugetlb_no_page -----> handle_userfault <---------+
                 |  (mm/memory.c)        (mm/huge_memory.c)                              |
                 +-> create_huge_pmd --> do_huge_pmd_anonymous_page----------------------+
                 |  (mm/memory.c)                                                        |
                 +-> __handle_mm_fault --> handle_pte_fault -+-> do_anonymous_page ------+
                                                             |                           |
                +--------------- do_fault <------------------+--+--> do_swap_page (MAJOR)|    
                |                                 (mm/shmem.c)  +--> do_numa_page        |   
                +---> do_read_fault          +--> shmem_fault --> shmem_getpage_gfp -----+
                |                            |         
                +---> do_cow_fault           +-----+--> ext4_dax_fault (fs/ext4/file.c)
                |                            |     +--> ... (FS&driver page faulthandlers)
                +---> do_shared_fault -+--> __do_fault    --> vma->vm_ops->fault
                |                      +--> do_page_mkwrite --> vma->vm_ops->page_mkwrite
                +---> VM_FAULT_SIGBUS
```

