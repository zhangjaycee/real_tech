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

## tar炸弹

> 参考： https://zh.wikipedia.org/wiki/Tar

> 攻击者利用绝对路径，或者“tar -cf bomb.tar *”的方式创建的tar文件，然后诱骗受害者在根目录下解压，或者使用绝对路径解压。可能使受害系统上已有的文件被覆盖掉，或者导致当前工作目录凌乱不堪，这就是所谓的“tar炸弹”。因此，要养成良好的解压习惯：
解压前用“t”查看tar的文件内容。
拒绝使用绝对路径。
新建一个临时子目录，然后在这个子目录里解压。
