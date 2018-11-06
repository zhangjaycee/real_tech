# Linux 内核架构


- 进程管理：

struct task_struct 为一个进程(或线程)的核心数据结构，调度也是以task_struct 为单位。

- 内存管理：

其指向的struct mm_struct结构管理这个进程的地址空间。

- IO管理：
  
数据存储于文件中，其他外设也被抽象为文件，由于一切皆文件，由VFS统一管理。
