# 机器(深度)学习系统的存储和IO性能

[1]和[2]两篇论文分别讲到了tensorflow和caffe的IO性能分析和优化。

### TensorFlow

TensorFlow中，计算被表示为计算流图，点为计算操作，边表示数据的产生或消耗。

TensorFlow的I/O主要涉及训练样本数据的读取，还有checkpoint数据的写入。读训练数据很容易理解；写checkpoint是为了方便任务中断后的重启，checkpoint定期执行，其将权重变量写到文件，每次的文件很容易达到几百MB，挺大的。一个次checkpoint由`tf.train.Saver()`发起，生成`.meta`、`.index`和`.data`三个文件。

原版TensorFlow中，数据接口称为Dataset API，其当然已经有优化I/O相关的策略，利用流水线和多线程的思想，也支持数据的预读。一个典型的情况下，每次迭代以mini-batch的方式进行训练，计算任务交由GPU执行，CPU负责用多个线程进行IO和数据处理等，再加上预取和流水线思想，计算和IO就有效重叠了起来。

具体来说，CPU的线程负责I/O、decoding和pre-processing。比如一个磁盘上的jpeg要先读取到内存、解压为tensor和resizing等处理。这条流程整个被称为input pipeline[1]。

### Caffe




---

[1] S. W. D. Chien et al., “Characterizing Deep-Learning I / O Workloads in TensorFlow,” 2018.

[2] S. Pumma, M. Si, W. Feng, and P. Balaji, “TOWARDS SCALABLE DEEP LEARNING VIA I/O ANALYSIS AND OPTIMIZATION.”