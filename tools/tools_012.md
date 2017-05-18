# htop

htop 较 top 更为“可视化”，在测试初始阶段做一些需要实时肉眼观察的时候挺好用的。

安装：
```
wget http://sourceforge.net/projects/htop/files/latest/download
tar -zxf download
cd htop-1.0.2
./configure
make
make install
```


运行后，和top直观上很大的功能差别是它默认会显示进程中的线程(userland thread)，导致界面上可能出现大量重复的名字，可以按F2在dispay设置中将其关闭。



> http://www.jianshu.com/p/eefc858b61ba
>
> https://sourceforge.net/projects/htop/