# Linux下如何杀掉一个进程

> 参考《linux下杀死进程的10种方法》：

> http://mrcelite.blog.51cto.com/2977858/1350392


### 常用的两种：
1. 
killall -9 *prog_name*

1. 
ps -ef|grep *prog_name* ;
kill -9 *pid*