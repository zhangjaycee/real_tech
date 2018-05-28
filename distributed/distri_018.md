# polling and interrupt based I/O

We only focus on block device polling here, rather than networking.


1. poll / epoll / select are all userspace polling.

2. In kernel, polling is only supported in NVMe driver or block layer's blk-mq ...

 