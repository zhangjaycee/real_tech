# 文件系统/数据库/存储设备中的日志

## 文件系统中的 logging FS 和 log-structured FS

logging filesystem(日志文件系统，又名journaling filesystem)和log-structured filesystem(日志结构文件系统)是两种东西。

我们熟悉的logging filesystem(journaling filesystem)包括ext3, ext4等。他们是为了保证数据的一致性，默认将metadata“存两次”，第一次存时作为日志存储，第二次是真正存到需要存的地方。先存一遍的原因是为了在掉电等意外发生时，保证metadata的一致性，防止文件系统发生错误(比如断电时日志没有存完，下次开机时可以直接扔掉没存完的日志，原位置的数据并没有因为只有部分被覆盖而发生错误)。

日志文件系统除了对metadata存两遍的Ordered模式外，还支持Journal模式(data和metadata都存两遍)和Writeback模式(只有metadata写两遍，不同于Journal模式的是，第二遍写完时并不保证data已经落盘)。

## 数据库中的undo log和redo log

## SSD中的log