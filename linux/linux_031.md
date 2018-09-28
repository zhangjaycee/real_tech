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

EPT分页机制详见本wiki ([硬件辅助的虚拟化](https://github.com/zhangjaycee/real_tech/wiki/virtual_021#%E5%86%85%E5%AD%98%E8%99%9A%E6%8B%9F%E5%8C%96ept))。

KVM辅助的虚拟机内存虚拟化也有缺页的问题，主要有两个方面：
1. GVA到GPA的缺页，其实就是GuestOS的缺页，由于KVM中，Guest的页表地址可以加载到CR3寄存器中，GuestOS的缺页与Host无关，由GuestOS内核进行管理。

2. HVA到HPA(PFN)的缺页才涉及到Host及EPT页表。由于EPT页表不完整或导致EPT voilation，这时空缺的、需要补充的是Host EPT页表，也由HostOS 内核的KVM模块进行管理。

类似于page fault的处理过程，KVM的voilation处理程序`handle_ept_violation`会负责找到可用的物理页填充适当的内容，然后以这个物理页补全不完整的EPT页表项。

## 3. userfaultfd

即用户空间的page fault handler，它为用户处理缺页提供了可能，增加了灵活性。(？但可能由于类似FUSE之于内核FS的问题影响性能)

要使用此功能，首先应该用userfaultfd调用来创建一个fd，然后用ioctl来配置这个fd，比如可能需要用ioctl-userfaultfd支持的UFFDIO_API、UFFDIO_REGISTER等进行设置。关于userfaultfd系统调用及例子见[1]，关于ioctl设置选项ioctl_userfaultfd见[2]。

此特性目前只对匿名页、shmem以及hugetlb等页支持，内核中对应的`handle_userfault`函数可能被这几部分的page fault handler所调用，普通文件映射的mmap暂时不支持userfault。

---
[1] http://man7.org/linux/man-pages/man2/userfaultfd.2.html

[2] http://man7.org/linux/man-pages/man2/ioctl_userfaultfd.2.html

[3] Caldwell, Blake, et al. "FluidMem: Memory as a Service for the Datacenter." arXiv preprint arXiv:1707.07780 (2017). (https://arxiv.org/pdf/1707.07780.pdf)

[4] The next steps for userfaultfd(), https://lwn.net/Articles/718198/

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
