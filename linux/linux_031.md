# Page fault

## 1. Linux的缺页


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
