# LZ4压缩算法


## 关于LZ4的存储形式[1][2]

LZ4的压缩数据块或者压缩数据帧的组织(存储)格式是与压缩/解压算法的具体实现无关的，压缩/解压算法都应该遵循这种格式存储压缩数据。

---

[1] http://fastcompression.blogspot.com/2011/05/lz4-explained.html

[2] http://fastcompression.blogspot.com/2013/04/lz4-streaming-format-final.html

## LZ4的系统

**MySQL InnoDB transparent page compression:** https://dev.mysql.com/doc/refman/5.7/en/innodb-page-compression.html

**EROFS** 

 H. C. Xiang Gao, Mingkai Dong, Xie Miao, Wei Du, Chao Yu, “EROFS : A Compression-friendly Readonly File System for Resource-scarce Devices,” Proc. 2019 USENIX Annu. Tech. Conf., 2019.