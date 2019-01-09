# 参数服务器

## 1. ps-lite

ps-lite 可以支持多种强度的一致性、实时弹性扩展和容错。

### 2. server端架构

整体架构如图[1]，ps-lite的server节点以类似KV的接口服务worker节点，其内部的通信是基于ZMQ-library(ZeroMQ[2])实现。ZMQ内部只要基于TCP协议通信，在[1]中作者修改成了RDMA接口，获得了性能提升。

[[distri_025_001.png]]

注意，通信模型对计算节点透明，优化通信策略不影响计算节点[2]。

### 3.replication

虽然在paper[1]中提到了replication的策略(如图的chain replica[1])，但是ps-lite 目前并未实现replication [3]。

[[distri_025_002.png]]

### 4. RDMA

[4]是一个在ps-lite的van模块中实现RDMA接口通信的一个pull request。

[5]是也是一篇实现ps-lite / MXNET 中实现RDMA的paper。




---

[1] M. Li et al., “Improving the Performance of Distributed MXNet with,” Int. J. Parallel Program., 2019.

[2] http://zeromq.org/

[3] https://github.com/dmlc/ps-lite/issues/15

[4] https://github.com/dmlc/ps-lite/pull/124

[5] M. Li et al., “Improving the Performance of Distributed MXNet with,” Int. J. Parallel Program., 2019.