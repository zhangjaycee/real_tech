# 存储性能测试工具

## 磁盘(文件)I/O测试工具[4]

基本的数据读写操作，基础的IO测试工具，都可以称为benchmark。比如固定一种访存模式（随机？顺序？追加？覆盖？等）都算是一种benchmark，只要具有可对比性。

* Fio [8] 
  - 被广泛应用于Linux环境下的文件/磁盘IO性能测试。

## 文件系统负载

* postmark[2][3]

  - 广泛应用的文件系统benchmark，会进行文件和目录操作(transaction)。

* filebench[1][4]

  - 比如可以用[filebench](https://github.com/filebench/filebench)的varmail模拟一个邮件服务器，而且会频繁的调用sync操作。


* File Name Search (find命令)[1]

  - find命令查找文件名时，有只读取文件系统的metadata的特点。

* bonnie++
  
  - 也是一种文件系统的benchmark

* SPECsfs2008[2]

  - 模拟NFSv3/CIFS文件服务器的文件系统benchmark。 

* FxMark [6][7]

  - 可以测试文件系统的多核扩展性。

## KV存储负载

* YCSB

  - 被广泛用于测试KV存储的性能。

* RocksDB 等KV存储引擎也会自带测试引擎，如db_bench等。

## 关系数据库负载

* 数据库TPC-C[1][2][4]

  - 模拟一个数据库操作员执行sql命令操纵数据库。所以应该是读写都有。

* 数据库TPC-H[2][3]

  - 很少有写操作，而且写操作基本都是由修改文件access时间组成的。
  - 基本是顺序读操作，并且不是IO密集型负载（计算密集型？），所以SSD并不能比HDD强很多。

## 其他负载

* dedup负载[1]

  - deduplication是计算(chunking、计算fingerprint、压缩)密集型和IO(需要进行磁盘上的查找，尤其是对于exact deduplication)密集型的[5]。

---

[1] L. Arulraj, A. C. Arpaci-Dusseau, and R. H. Arpaci-Dusseau, “Improving Virtualized Storage Performance with Sky,” Proc. 13th ACM SIGPLAN/SIGOPS Int. Conf. Virtual Exec. Environ., pp. 112–128, 2017.

[2] T. Makatos, Y. Klonatos, M. Marazakis, M. D. Flouris, and A. Bilas, “ZBD: Using transparent compression at the block level to increase storage space efficiency,” Proc. - 2010 Int. Work. Storage Netw. Archit. Parallel I/Os, SNAPI 2010, pp. 61–70, 2010.

[3] F. Chen, D. Koufaty, and X. Zhang, “Hystor: making the best use of solid state drives in high performance storage systems,” Ics ’11, pp. 22–32, 2011.

[4] Q. Chen, L. Liang, Y. Xia, and H. Chen, “Mitigating Sync Amplification for Copy-on-write Virtual Disk,” 14th USENIX Conf. File Storage Technol. (FAST 16), pp. 241–247, 2016.

[5] Ma Jingwei, et al. "Lazy exact deduplication." ACM Transactions on Storage (TOS) 13.2 (2017): 11.

[6] Min, Changwoo, et al. "Understanding manycore scalability of file systems." 2016 USENIX Annual Technical Conference (USENIX ATC 16). 2016.
 
[7] https://github.com/sslab-gatech/fxmark

[8] https://github.com/axboe/fio