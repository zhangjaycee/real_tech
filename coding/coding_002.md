# 密码哈希 Cryptographic hash function

校验和与密码学hash函数的应用的场合不同，复杂度也不同，校验多用于通信数据传输，所以速度一定要快，而安全hash多用于加密等安全领域，计算速度甚至是慢也无所谓。

e.g. 校验(checksum)比如CRC等，hash比如MD5、SHA等。

### 性能

[1][2] 中给出了CPU的测试。[3]中给出了GPU的测试。

---


[1] https://www.cryptopp.com/benchmarks.html

[2] http://bench.cr.yp.to/results-hash.html

[3] Speed Hashing, https://blog.codinghorror.com/speed-hashing/