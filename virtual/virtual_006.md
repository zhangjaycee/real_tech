#Qemu

> [QEMU Internals: How guest physical RAM works](http://blog.vmsplice.net/2016/01/qemu-internals-how-guest-physical-ram.html) [[翻译](https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/20160921?lang=zh)]

> [QEMU Internals: Big picture overview](http://blog.vmsplice.net/2011/03/qemu-internals-big-picture-overview.html) [[翻译](https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/20160805?lang=zh)]

> [QEMU Internals: Overall architecture and threading model
](http://blog.vmsplice.net/2011/03/qemu-internals-overall-architecture-and.html) [[翻译](https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/20161222?lang=en)]

> [QEMU Internals: vhost architecture
](http://blog.vmsplice.net/2011/09/qemu-internals-vhost-architecture.html) [[翻译](http://www.cnblogs.com/scottieyuyang/p/6050798.html)]

### 阅读代码的工具准备和经验
> http://www.hengtianyun.com/download-show-id-2603.html 

> * 工具准备

> 阅读代码的工具包括vim、ctags、gdb。
其中ctags会维持一个全局的tag表。通过在源代码主目录下使用ctags –R，可以生成对应的tag表的文件，文件名为tags。在打开一个源代码文件后，用户通过将光标移动到某一个函数调用或者数据结构的位置，同时按住ctrl+]，就可以跳转到函数或者数据结构的定义处，如果函数或者数据结构有多个定义，在vim中输入:tn可以看下一个函数的定义。通过ctrl+t可以跳转回原来的位置。另外，如果vim显示没有找到tags文件，需要显式地告知vim，tags的路径，命令:set tags=$tagspath。

> * 经验

>由于QEMU是相当大型的代码，定义了大量的数据结构，对于初学者，直接使用gdb调试，在学习和理解上会比较吃力。因此开始学习代码时，可以先使用vim+ctags，学习qemu的基本数据结构开始，这些代码的学习不需要动态调试，只需要静态地查看，就可以比较细致和系统地学习，主要包括include/qemu/文件夹下的.h文件和对应的.c文件、include/qom/文件夹下的.h文件和对应的.c文件、include/hw/文件夹下的.h文件和对应的.c文件等等。这些实现代码是qemu最底层的实现，如果使用gdb的话，一般要进入10层以上的函数堆栈才能跟踪到，但是通过对这些代码的学习，可以基本学习到QEMU是如何对设备进行模拟的，同时可以对QEMU的代码结构有初步的掌握。

>对于QEMU实现的某些虚拟化功能，比如热迁移，可以采用gdb调试的方法学习，学习其代码流程。但是在gdb调试之前，仍然建议粗略地看一下代码的相关流程、函数跳转，以便调试时能够清楚应该具体在哪里打断点。

>特别需要注意的是QEMU中全局变量的定义和使用，这些全局变量管理了虚拟机的全部资源包括CPU、内存等，理解这些全局变量的使用，对于理解QEMU的执行有很大的帮助。
