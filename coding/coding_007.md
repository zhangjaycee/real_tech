# 无损压缩能否突破信息熵的限制


无损压缩就是数据在压缩后的还能原样恢复到压缩前的样子。

若不考虑序列的相关性(dependencies)，认为每个元素独立同分布，则信息熵(即信息量)是一阶的，**一阶信息熵** 相对考虑信源相关性的信源熵更大。


信息熵则被定义来衡量信源所生成信息的信息量。

信息熵是熵编码的上限，并非损压缩算法的上限。

---



[1] 《数据压缩导论(第4版)》第二章

[2] https://books.google.com/books?id=Ii6rDAAAQBAJ&pg=PT46&lpg=PT46&dq=information+entropy+delta+encoding&source=bl&ots=GvI9ggE2jr&sig=ACfU3U0ptV_F8TgS0acePTDKak_QaEtApw&hl=en&sa=X&ved=2ahUKEwjTu8Pr_vbgAhUPKawKHeucACUQ6AEwD3oECAQQAQ#v=onepage&q=information%20entropy%20delta%20encoding&f=true