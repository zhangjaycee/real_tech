## 大数据系统和分布式存储


### 1. Spark

##### 1.1 数据形式

Spark 的数据API进化：
```
RDD(2011) --> DataFrame(2013) --> DataSet(2015)
```

Resilient Distributed Datasets (RDD)是Spark最原始支持的数据形式。

DataFrame 是一种结构化(支持SQL)数据抽象。

DataSet是最新的，是一种”compile time type-safe“的DataFrame。

##### 1.2 存储形式

Spark支持CSV、parquet等文件格式，可以从这些文件中创建DataFrame等数据形式。
