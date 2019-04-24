# Page fault


> [1. Linux的page fault](#1-linux的page-fault)
>
> [2. KVM(EPT)的缺页](#2-kvmept的缺页)
>
> [3. Userfaultfd](#3-userfaultfd)
>
> [4. 关系图](#4-关系图)

## 1. Linux的page fault

内存也可以分为三种状态：[1]

1. **未映射页(unmapped)**: 如果memory region在被程序分配后，没有被写过，那么它会被看作全零的，OS也因此无须找物理页来存这些零。多数OS在内存被分配时将地址范围返回给用户，但是把这些页标记为unmapped，暂不与物理页关联。

2. **驻留页(resident)**：页实实在在在物理RAM中。

3. **换出页(swapped)**：页在RAM中存在过，但现在被换出(swap)到了磁盘中。

访问一个页时，若非状态(2)，会引起page fault，page fault一般又可以分为两种：

1. 状态(1)会引起**minor page fault**，这时虽然被分配了，但是进程还没有读写过对应的线性区(memory region)，所以读写时会产生一次minor page fault。内核中的`handle_mm_fault`会返回`VM_FAULT_MINOR`(注意，最新内核中已经返回0表示minor fault，并删除了`VM_FAULT_MINOR`这个宏定义)。

2. 状态(3)会引起**major page fault**，需要磁盘IO来恢复页。核中的`handle_mm_fault`会返回`VM_FAULT_MAJOR`。

---
[1] https://frogatto.com/2009/10/30/what-every-programmer-should-know-about-memory-management/

## 2. KVM(EPT)的缺页

EPT分页机制详见本wiki ([硬件辅助的虚拟化](https://github.com/zhangjaycee/real_tech/wiki/virtual_021#%E5%86%85%E5%AD%98%E8%99%9A%E6%8B%9F%E5%8C%96ept))。

KVM辅助的虚拟机内存虚拟化也有缺页的问题，主要有两个方面：
1. GVA到GPA的缺页，其实就是GuestOS的缺页，由于KVM中，Guest的页表地址可以加载到CR3寄存器中，GuestOS的缺页与Host无关，由GuestOS内核进行管理。

2. HVA到HPA(PFN)的缺页才涉及到Host及EPT页表。由于EPT页表不完整或导致EPT voilation，这时空缺的、需要补充的是Host EPT页表，也由HostOS 内核的KVM模块进行管理。

类似于page fault的处理过程，KVM的voilation处理程序`handle_ept_violation`会负责找到可用的物理页填充适当的内容，然后以这个物理页补全不完整的EPT页表项。

## 3. userfaultfd

即用户空间的page fault handler，它为用户处理缺页提供了可能，增加了灵活性。(？但可能由于类似FUSE之于内核FS的问题影响性能)

### 3.1 基本使用步骤

以最基本的用户空间进行匿名页缺页处理为例，(例子代码基本来自userfaultfd的man page[1]，)步骤大致如下：

**STEP 1. 创建一个描述符uffd**

要使用此功能，首先应该用userfaultfd调用[1]来创建一个fd，例如:
```cpp
// userfaultfd系统调用创建并返回一个uffd，类似一个文件的fd
uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
```
然后，所有的注册内存区间、配置和最终的缺页处理等就都需要用ioctl来对这个uffd操作。ioctl-userfaultfd[2]支持UFFDIO_API、UFFDIO_REGISTER、UFFDIO_UNREGISTER、UFFDIO_COPY、UFFDIO_ZEROPAGE、UFFDIO_WAKE等选项。比如UFFDIO_REGISTER用来向userfaultfd机制注册一个监视区域，这个区域发生缺页时，需要用UFFDIO_COPY来向缺页的地址拷贝自定义数据。

**STEP 2. 用ioctl的UFFDIO_REGISTER选项注册监视区域**

比如，UFFDIO_REGISTER对应的注册操作如下：
```cpp
// 注册时要用一个struct uffdio_register结构传递注册信息:
// struct uffdio_range {
// __u64 start;    /* Start of range */
// __u64 len;      /* Length of range (bytes) */
// };
//
// struct uffdio_register {
// struct uffdio_range range;
// __u64 mode;     /* Desired mode of operation (input) */
// __u64 ioctls;   /* Available ioctl() operations (output) */
// };

addr = mmap(NULL, page_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0)
// addr 和 len 分别是我匿名映射返回的地址和长度，赋值到uffdio_register
uffdio_register.range.start = (unsigned long) addr;
uffdio_register.range.len = len;
// mode 只支持 UFFDIO_REGISTER_MODE_MISSING
uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
// 用ioctl的UFFDIO_REGISTER注册
ioctl(uffd, UFFDIO_REGISTER, &uffdio_register);
```

**STEP 3. 创建一个处理专用的线程轮询和处理"user-fault"事件**

要使用userfaultfd，需要创建一个处理专用的线程轮询和处理"user-fault"事件。主进程中就要调用`pthread_create`创建这个自定义的handler线程：

```cpp
// 主进程中调用pthread_create创建一个fault handler线程
pthread_create(&thr, NULL, fault_handler_thread, (void *) uffd);
```

一个自定义的线程函数举例如下，这里处理的是一个普通的匿名页用户态缺页，我们要做的是把我们一个已有的一个page大小的buffer内容拷贝到缺页的内存地址处。用到了`poll`函数轮询`uffd`，并对轮询到的`UFFD_EVENT_PAGEFAULT`事件(event)用拷贝(ioctl的`UFFDIO_COPY`选项)进行处理。

```cpp
static void * fault_handler_thread(void *arg)
{    
    // 轮询uffd读到的信息需要存在一个struct uffd_msg对象中
    static struct uffd_msg msg;
    // ioctl的UFFDIO_COPY选项需要我们构造一个struct uffdio_copy对象
    struct uffdio_copy uffdio_copy;
    uffd = (long) arg;
      ......
    for (;;) { // 此线程不断进行polling，所以是死循环
        // poll需要我们构造一个struct pollfd对象
        struct pollfd pollfd;
        pollfd.fd = uffd;
        pollfd.events = POLLIN;
        poll(&pollfd, 1, -1);
        // 读出user-fault相关信息
        read(uffd, &msg, sizeof(msg));
        // 对于我们所注册的一般user-fault功能，都应是UFFD_EVENT_PAGEFAULT这个事件
        assert(msg.event == UFFD_EVENT_PAGEFAULT);
        // 构造uffdio_copy进而调用ioctl-UFFDIO_COPY处理这个user-fault
        uffdio_copy.src = (unsigned long) page;
        uffdio_copy.dst = (unsigned long) msg.arg.pagefault.address & ~(page_size - 1);
        uffdio_copy.len = page_size;
        uffdio_copy.mode = 0;
        uffdio_copy.copy = 0;
        // page(我们已有的一个页大小的数据)中page_size大小的内容将被拷贝到新分配的msg.arg.pagefault.address内存页中
        ioctl(uffd, UFFDIO_COPY, &uffdio_copy);
          ......
    }
}

```

在userfaultfd man page[1]及内核源码中的测试文件`KERNEL_SRC/linux-4.18.8/tools/testing/selftests/vm/userfaultfd.c`中，分别关于userfaultfd系统调用有两个例程。上述最一般的“缺页-用户态拷贝数据”例子源自前者中的例程；后者中的例程则涵盖了目前内核中user-fault机制的所有选项和功能。

### 3.2 其他的ioctl选项

目前为止，user-fault机制支持UFFDIO_REGISTER、UFFDIO_UNREGISTER、UFFDIO_COPY、UFFDIO_ZEROPAGE、UFFDIO_WAKE、UFFDIO_API等五种选项，分别用于注册、配置或处理用户态缺页功能如下。
```
# 2 个用于注册、注销的ioctl选项：
UFFDIO_REGISTER                 注册将触发user-fault的内存地址
UFFDIO_UNREGISTER               注销将触发user-fault的内存地址
# 3 个用于处理user-fault事件的ioctl选项：
UFFDIO_COPY                     用已知数据填充user-fault页
UFFDIO_ZEROPAGE                 将user-fault页填零
UFFDIO_WAKE                     用于配合上面两项中 UFFDIO_COPY_MODE_DONTWAKE 和
                                UFFDIO_ZEROPAGE_MODE_DONTWAKE模式实现批量填充  
# 1 个用于配置uffd特殊用途的ioctl选项：
UFFDIO_API                      它又包括如下feature可以配置：
                                UFFD_FEATURE_EVENT_FORK         (since Linux 4.11)
                                UFFD_FEATURE_EVENT_REMAP        (since Linux 4.11)
                                UFFD_FEATURE_EVENT_REMOVE       (since Linux 4.11)
                                UFFD_FEATURE_EVENT_UNMAP        (since Linux 4.11)
                                UFFD_FEATURE_MISSING_HUGETLBFS  (since Linux 4.11)
                                UFFD_FEATURE_MISSING_SHMEM      (since Linux 4.11)
                                UFFD_FEATURE_SIGBUS             (since Linux 4.14)

(详见 ioctl_userfaultfd man page [2])
```

### 3.2.1 ioctl-UFFDIO_API选项的最新特性

值得注意的是，4.11后的UFFDIO_API选项。UFFDIO_API提供的features，让匿名(anonymous)页之外的hugetlbfs、shared-memory(shmem)页也得到了支持；也提供了对"non-cooperative events"的支持，包括mapping、unmapping、fork()、remove等操作[4]。我理解，这里的non-cooperative events指user-fault handler(处理程序)对产生fork/madvise/mremap等事件的进程是透明的，user-fault handler读取到这些事件后，产生事件的进程就会继续进行[5]，而不会被阻塞。

`UFFD_FEATURE_SIGBUS`是最新被加入的。加入它最初的目的是，很多数据库系统采用hugetlbfs中的大页文件，并且这些文件时(带洞的)稀疏文件，当数据库程序有bug时，可能错误地将洞进行mmap，这会导致内核尝试自动地填洞最终导致文件非预期地扩大，为了让bug“误触”到文件洞时直接返回`SIGBUS`信号，`UFFD_FEATURE_SIGBUS`被提出。这个feature不需要对应的user-fault handler处理线程。

总之，要正确理解这些较新的features，还是推荐看一下`KERNEL_SRC/linux-4.18.8/tools/testing/selftests/vm/userfaultfd.c`代码及最新的用户文档。

此特性目前只对匿名页、shmem以及hugetlb等页支持，内核中对应的`handle_userfault`函数可能被这几部分的page fault handler所调用，普通文件映射的mmap暂时不支持userfault。

---
[1] http://man7.org/linux/man-pages/man2/userfaultfd.2.html

[2] http://man7.org/linux/man-pages/man2/ioctl_userfaultfd.2.html

[3] Caldwell, Blake, et al. "FluidMem: Memory as a Service for the Datacenter." arXiv preprint arXiv:1707.07780 (2017). (https://arxiv.org/pdf/1707.07780.pdf)

[4] The next steps for userfaultfd(), https://lwn.net/Articles/718198/

[5] https://lkml.org/lkml/2018/2/27/78

[6] https://marc.info/?l=linux-mm&m=149857975906880&w=2

# 4. 关系图

下面是以`handle_mm_fault`为中心的，上面三方面之间的内核调用关系。

### 4.1 Linux内核page fault

mm/fault.c 中的do_page_fault 会调用handle_mm_fault，然后调用关系如图：

1. 其中`do_swap_page`应该是所谓Major fault；
2. `do_anonymous_page`是匿名页的Minor fault；
3. `__do_fault`则会调用其他文件系统或者驱动中mmap所对应的page fault，比如`do_shared_fault`-->`ext4_dax_fault`是开启`dax`支持的ext4文件系统对应的fault实现。因为ext4的视线中，定义了`struct vm_operations_struct ext4_dax_vm_ops`:
```cpp
// (fs/ext4/file.c)
static const struct vm_operations_struct ext4_dax_vm_ops = {
	.fault		= ext4_dax_fault,   // [这里面没有涉及userfaultfd]
	.huge_fault	= ext4_dax_huge_fault,
	.page_mkwrite	= ext4_dax_fault,
	.pfn_mkwrite	= ext4_dax_pfn_mkwrite,
};
```


```
(mm/memory.c)       (mm/hugetlb.c)                           (fs/userfaultfd.c)
handle_mm_fault -+-> hugetlb_fault --> hugetlb_no_page -----> handle_userfault <---------+
                 |  (mm/memory.c)        (mm/huge_memory.c)                              |
                 +-> create_huge_pmd --> do_huge_pmd_anonymous_page----------------------+
                 |  (mm/memory.c)                                                        |
                 +-> __handle_mm_fault --> handle_pte_fault -+-> do_anonymous_page ------+
                                                             |  +--> do_wp_page          |
                +--------------- do_fault <------------------+--+--> do_swap_page (MAJOR)|    
                |                                 (mm/shmem.c)  +--> do_numa_page        |   
                +---> do_read_fault          +--> shmem_fault --> shmem_getpage_gfp -----+
                |                            |         
                +---> do_cow_fault           +-----+--> ext4_dax_fault (fs/ext4/file.c)
                |                            |     +--> ... (FS&driver page faulthandlers)
                +---> do_shared_fault -+--> __do_fault(--> vma->vm_ops->fault)
                |                      +--> do_page_mkwrite(--> vma->vm_ops->page_mkwrite)
                +---> VM_FAULT_SIGBUS        |
                                             +--> ext4_dax_pfn_mkwrite (fs/ext4/file.c)
                                             +--> ... (FS&driver handlers)
```

### 4.2 userfaultfd

还是上边的关系图，可以看到，`do_anonymous_page`、`do_shared_fault`中的某些驱动的handler(shmem)、`hugetlb_fault`、`create_huge_pmd`等最终都会指向`handle_userfault`，但是基于ext4、XFS中文件的mmap则不会调用`handle_userfault`，这是因为它们的handler没有对应的实现。

### 4.3 KVM (EPT)

参考[1] 并阅读代码：(还未经调试确认)

```
handle_ept_violation {
        vmcs_readl(EXIT_QUALIFICATION)       // 获取 EPT 退出的原因。
        vmcs_read64(GUEST_PHYSICAL_ADDRESS)  // 获取发生缺页的 GPA 根据 exit_qualification 
                                             // 内容得到 error_code，可能是 read fault / 
                                             // write fault / fetch fault / 
                                             // ept page table is not present
        kvm_mmu_page_fault 
        vcpu->arch.mmu.page_fault (tdp_page_fault ① ) 
    }   
--> tdp_page_fault ① { 
        gfn = gpa >> PAGE_SHIFT      //将 GPA 右移 pagesize 得到 gfn(guest frame number)
        mapping_level                //计算 gfn 在页表中所属 level，不考虑 hugepage 则为 L1  
        try_async_pf ②               //将 gfn 转换为 pfn(physical frame number)
        __direct_map ③
    }   
--> try_async_pf ② { 
        kvm_vcpu_gfn_to_memslot --> __gfn_to_memslot         //找到 gfn 对应的 slot
        __gfn_to_pfn_memslot {                               //找到 gfn 对应的 pfn 
            __gfn_to_hva_many --> __gfn_to_hva_memslot       //计算 gfn 对应的起始 HVA 
            hva_to_pfn ④                                     //计算 HVA 对应的 pfn，
        }                                                    //同时确保该物理页在内存中
}

--> __direct_map ③ {                      //更新 EPT，将新的映射关系逐层添加到 EPT 中
        for_each_shadow_entry {           //从 level4(root) 开始，逐层补全页表，对于每一层：
            mmu_set_spte                  //对于 level1 的页表，其页表项肯定是缺的，
                                          //所以不用判断直接填上 pfn 的起始 hpa 
            is_shadow_present_pte {       //如果下一级页表页不存在，即当前页表项没值 (*sptep = 0)
                kvm_mmu_get_page          //分配一个页表页结构
                link_shadow_page          //将新页表页的 HPA 填入到当前页表项 (sptep) 中
            }   
        }   
    }   

--> hva_to_pfn ④ (先尝试hva_to_pfn_fast失败了)
--> hva_to_pfn_slow 
--> get_user_pages_unlocked 
--> __get_user_pages_locked 
--> __get_user_pages (没有找到存在的页框?)
--> faultin_page 
--> handle_mm_fault (这个函数在关系图中!)
```
---
[1] https://www.binss.me/blog/qemu-note-of-memory/



### 4.4 对page fault的一些改进

#### Spective page fault: 

[1] https://lwn.net/Articles/730531/

[2] https://marc.info/?l=linux-mm&m=125747798627503&w=2
