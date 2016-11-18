# 关于tar

> 参考： http://www.linuxprobe.com/tar-commands.html

归档和压缩是两个步骤。

* 只归档：
```bash
tar -cvf xxx.tar path_to_file #归档
```

* 归档并压缩： 
```bash
tar -zcvf xxx.tar.gz path_to_file #gzip压缩
tar -jcvf xxx.tar.bz2 path_to_file #bzip2压缩
#参数中加p可以保留权限
```

* 释放/解压缩
```bash
tar -xvf xxx.tar[.gz/bz2] [-C dst_path] #释放
```