# Cscope基本使用

## 建立cscope使用的索引文件
在你需要浏览源码的根目录下（如你想用cscope看linux源码)使用下面命令：
```bash
cscope -Rbq
```
```
R 表示把所有子目录里的文件也建立索引
b 表示cscope不启动自带的用户界面，而仅仅建立符号数据库
q生成cscope.in.out和cscope.po.out文件，加快cscope的索引速度
k在生成索引文件时，不搜索/usr/include目录
```
## Vim中使用cscope
在源码根目录下打开任意.c文件，使用如下命令：
```
Ctrl+]将跳到光标所在变量或函数的定义处 Ctrl+T返回
：cs find s ---- 查找C语言符号，即查找函数名、宏、枚举值等出现的地方
：cs find g ---- 查找函数、宏、枚举等定义的位置，类似ctags所提供的功能
：cs find d ---- 查找本函数调用的函数
：cs find c ---- 查找调用本函数的函数
：cs find t: ---- 查找指定的字符串
：cs find e ---- 查找egrep模式，相当于egrep功能，但查找速度快多了
：cs find f ---- 查找并打开文件，类似vim的find功能
：cs find i ---- 查找包含本文件的文
```

> 参考：

> http://cscope.sourceforge.net/

> http://laokaddk.blog.51cto.com/368606/1242365