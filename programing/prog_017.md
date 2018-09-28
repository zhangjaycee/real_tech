# Linux环境编译常见问题

* 找不到动态链接库

八成是路径不对，先确定库的位置，然后在`/etc/ld.so.conf.d`文件夹中加入一个文件写明这个路径。然后运行`sudo /sbin/ldconfig`使文件生效。

* 系统是中文的，GCC输出信息是中文不方便google怎么办？
```bash
export LANG=en_US
```

* gcc的默认搜索路径？(PATH)

gcc可以通过`-I`、`-L`等指定路径，也有默认的搜索路径，怎么知道呢：[2]
```bash
#For C:
gcc -xc -E -v -
#For C++:
gcc -xc++ -E -v -
```


--- 
[1] https://www.cnblogs.com/xudong-bupt/p/3698294.html

[2] https://stackoverflow.com/questions/4980819/what-are-the-gcc-default-include-directories
