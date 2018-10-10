# 指令集并行 (分支预测, 乱序执行...)

处理器有个指令窗口，同一个窗口中存在乱序执行，但是每次离开的执行(被称为commit或者retire)的只能是最早进入窗口的指令，所以类似一个滑动窗口。


以下图来自[1]中，介绍了一种典型的Intel x86架构的pipeline执行流程。分为front-end部分和back-end部分。

[[arch_001_p1.png]]


- frontend负责fetching和traslating，即从L1i cahce取指令，翻译(decode)成micro-operations(uops)并插入到micro-op队列中。

- backend负责schdule, execute和commit (retire)指令。图中也可以看到load和store模块会和L1d cache交互。

- frontend和backend都会和L2 cache进行交互，可见L2 cache是部分指令/数据cache的。


---

[1] G. Ayers, J. H. Ahn, C. Kozyrakis, and P. Ranganathan, “Memory Hierarchy for Web Search,” 2018 IEEE Int. Symp. High Perform. Comput. Archit., pp. 643–656, 2018.