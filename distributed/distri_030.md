## Redis

### 1. 编译安装

```bash
# 先从 redis.io 下载源码包并解压到 REDIS_SRC_PATH
cd REDIS_SRC_PATH
cd deps
# 编译jemalloc等依赖
make hiredis jemalloc linenoise lua
cd ..
make
```

---
[1] https://redis.op

## LevelDB


### 2. 编译安装

(CentOS 7中)

```bash
git clone --recurse-submodules https://github.com/google/leveldb.git
mkdir -p build && cd build
cmake3 -DCMAKE_BUILD_TYPE=Release .. && cmake3 --build .
```

---
[1] https://github.com/google/leveldb