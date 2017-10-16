# Open-channel SSD



Fast 17 中专门有一个分区(包括3篇paper)讲了相关的研究:

- LightNVM: The Linux Open-Channel SSD Subsystem

- FlashBlox: Achieving Both Performance Isolation and Uniform Lifetime for Virtualized SSDs

- DIDACache: A Deep Integration of Device and Application for Flash based Key-value Caching

其中写LightNVM的作者Bjørling正是13年SYSTOR写了blk-mq linux块层多队列(multi-queue)调度器的人，paper如下：

- Linux Block IO: Introducing Multi-queue SSD Access on Multi-core Systems

更多关于blk-mq在本wiki中也有写到：[[blk-mq 相关|linux_015]]


## 更多相关网页：

The multiqueue block layer, https://lwn.net/Articles/552904/

Support for Open-Channel SSDs (was dm-lightnvm), https://lwn.net/Articles/615341/

Taking control of SSDs with LightNVM, https://lwn.net/Articles/641247/
  