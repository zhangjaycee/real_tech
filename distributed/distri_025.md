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


### 5. 一些源码

#### key-value Push

在` tests/test_kv_app.cc`，中，Worker函数会调用`KVWorker<float> kv(0, 0);`创建一个KVWorker对象kv。

然后会用`kv.Push()`,`kv.Pull()`,`kv.Wait()`等API。


#### Worker

KVWorker类在`ps/kv_app.h`中实现。其中以Push函数为例，有如下调用关系：

```
KVWorker::Push()  --> KVWorker::ZPush()  -->  KVWorker::Send()
```



到了`KVWorker::Send()`中，比较关键，它在最后会调用van类(默认ZMQ?)的接口。具体函数摘抄如下：

```cpp
template <typename Val>
void KVWorker<Val>::Send(int timestamp, bool push, int cmd, const KVPairs<Val>& kvs) {
  // slice the message 切分数据
  SlicedKVs sliced;
  // 默认的slicer_函数是DefaultSlicer
  slicer_(kvs, Postoffice::Get()->GetServerKeyRanges(), &sliced);

  // need to add response first, since it will not always trigger the callback
  int skipped = 0;
  for (size_t i = 0; i < sliced.size(); ++i) {
    if (!sliced[i].first) ++skipped;
  }
  obj_->AddResponse(timestamp, skipped);
  if ((size_t)skipped == sliced.size()) {
    RunCallback(timestamp);
  }

  for (size_t i = 0; i < sliced.size(); ++i) {
    const auto& s = sliced[i];
    if (!s.first) continue;
    Message msg;
    msg.meta.app_id = obj_->app_id();
    msg.meta.customer_id = obj_->customer_id();
    msg.meta.request     = true;
    msg.meta.push        = push;
    msg.meta.head        = cmd;
    msg.meta.timestamp   = timestamp;
    msg.meta.recver      = Postoffice::Get()->ServerRankToID(i);
    const auto& kvs = s.second;
    if (kvs.keys.size()) {
      msg.AddData(kvs.keys);
      msg.AddData(kvs.vals);
      if (kvs.lens.size()) {
        msg.AddData(kvs.lens);
      }
    }
    // 发送
    Postoffice::Get()->van()->Send(msg);
  }
}
```



`Van::Send()`会调用`Van::SendMsg()`，`src/zmq_van.h`实现了一种van，其利用了ZeroMQ实现。

#### Server

test_kv_app.cc 中的StartServer()会创建一个`KVServer`对象，在`class KVServer`构造时，它构造时会new一个`class Customer`，`Customer`在构造时又会开一个Recieving **线程** ，这个Receiving函数就在`src/customer.cc`中：

```cpp
void Customer::Receiving() {
  while (true) {
    Message recv;
    recv_queue_.WaitAndPop(&recv);
    if (!recv.meta.control.empty() &&
        recv.meta.control.cmd == Control::TERMINATE) {
      break;
    }
    recv_handle_(recv);
    if (!recv.meta.request) {
      std::lock_guard<std::mutex> lk(tracker_mu_);
      tracker_[recv.meta.timestamp].second++;
      tracker_cond_.notify_all();
    }
  }
}
```

对于server，KV数据最终会由`server->set_request_handle()`所设置的函数处理，在ps-lite中，给出了一个`struct KVServerDefaultHandle`类，它重载了函数调用：

```cpp
/**
 * \brief an example handle adding pushed kv into store
 */
template <typename Val>
struct KVServerDefaultHandle {
  void operator()(
      const KVMeta& req_meta, const KVPairs<Val>& req_data, KVServer<Val>* server) {
    size_t n = req_data.keys.size();
    KVPairs<Val> res;
    if (req_meta.push) {
      CHECK_EQ(n, req_data.vals.size());
    } else {
      res.keys = req_data.keys; res.vals.resize(n);
    }
    for (size_t i = 0; i < n; ++i) {
      Key key = req_data.keys[i];
      if (req_meta.push) {
        store[key] += req_data.vals[i];
      } else {
        res.vals[i] = store[key];
      }
    }
    server->Response(req_meta, res);
  }
  std::unordered_map<Key, Val> store; // 注意这里store定义为一个unordered_map
};
```

---

[1] M. Li et al., “Improving the Performance of Distributed MXNet with,” Int. J. Parallel Program., 2019.

[2] http://zeromq.org/

[3] https://github.com/dmlc/ps-lite/issues/15

[4] https://github.com/dmlc/ps-lite/pull/124

[5] M. Li et al., “Improving the Performance of Distributed MXNet with,” Int. J. Parallel Program., 2019.

[6] https://www.zybuluo.com/Dounm/note/529299