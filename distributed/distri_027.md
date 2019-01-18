# 机器(深度)学习系统的存储IO性能

[1]和[2]两篇论文分别讲到了tensorflow和caffe的IO性能分析和优化。

### TensorFlow

TensorFlow中，计算被表示为计算流图，点为计算操作，边表示数据的产生或消耗。

TensorFlow的I/O主要涉及训练样本数据的读取，还有checkpoint数据的写入。读训练数据很容易理解；写checkpoint是为了方便任务中断后的重启，checkpoint定期执行，其将权重变量写到文件，每次的文件很容易达到几百MB，挺大的。一个次checkpoint由`tf.train.Saver()`发起，生成`.meta`、`.index`和`.data`三个文件。

原版TensorFlow中，数据接口称为Dataset API，其当然已经有优化I/O相关的策略，利用流水线和多线程的思想，也支持数据的预读。一个典型的情况下，每次迭代以mini-batch的方式进行训练，计算任务交由GPU执行，CPU负责用多个线程进行IO和数据处理等，再加上预取和流水线思想，计算和IO就有效重叠了起来。

具体来说，CPU的线程负责I/O、decoding和pre-processing。比如一个磁盘上的jpeg要先读取到内存、解压为tensor和resizing等处理。这条流程整个被称为input pipeline[1]。

### Caffe和LMDB

[2]中主要讨论了caffe的IO接口LMDB。

LMDB (lightning memory-mapped database)，它是以B+树的形式存储的，并且使用时用mmap映射到内存，也不只用于caffe，TensorFlow等也会用它。[2]中主要提出了一种基于MPI-shared memory的共享映射区，减少IO完成中断在多进程IO情况下导致的不必要进程切换开销。

在[2]的相关工作中，还提到了很多其他的IO框架。比如，MPI-IO是比较低层次，为非结构化数据提供了并行IO接口；HDF5和NetCDF是比较高层次的，它们吧数据抽象为文件格式，并提供了丰富功能的IO接口。一些工作结合高层次的HDF5、NetCDF和低层次的MPI-IO，因此同时提供了并行IO和丰富的编程接口。作者提到这些IO框架逗比mmap高效，但是用起来不如mmap方便。长期来看用这些IO框架代替mmap是值得的，但是很多数据集就要从LMDB文件格式迁移到其他格式。


---

[1] S. W. D. Chien et al., “Characterizing Deep-Learning I / O Workloads in TensorFlow,” 2018.

[2] S. Pumma, M. Si, W. Feng, and P. Balaji, “TOWARDS SCALABLE DEEP LEARNING VIA I/O ANALYSIS AND OPTIMIZATION.”