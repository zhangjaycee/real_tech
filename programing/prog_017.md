# 编译常见错误

* 找不到动态链接库

八成是路径不对，先确定库的位置，然后在`/etc/ld.so.conf.d`文件夹中加入一个文件写明这个路径。然后运行`sudo /sbin/ldconfig`使文件生效。


--- 
[1] https://www.cnblogs.com/xudong-bupt/p/3698294.html