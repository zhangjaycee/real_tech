# GDB调试

## 安装GDB

`sudo apt install gdb`

## 编译被调试源码

### C语言
对于一般的c语言程序在gcc编译的时候应该加上`-g`，e.g.
```bash
#编译
gcc -g hello.c -o hello_bin
```
### 对于Qemu
configure的时候，参数后边加上`--enable-debug`, e.g.
```bash
./configure --enable-kvm --target-list=x86_64-softmmu --ebable-debug
```

## 调试

### 基本命令

```bash
#打开gdb
> gdb
#打开要调试的文件
(gdb) file hello_bin
#列出源代码
(gdb) list
#添加断点到hello.c的第10行
(gdb) break hello.c:10
#查看当前所设置的断点
(gdb) info break #或者直接(gdb)i b
#删除某个断点 delete(clear) + 断点标号，标号可以用(gdb) i b查看，不加标号为全部删除
(gdb) delete 5
(gdb) clear
#暂停(开启)使用某个(全部)断点
(gdb) disable 5
(gdb) disable
(gdb) enable 5
(gdb) enable
#执行程序，格式是r[un] + 参数列表
(gdb) run arg1 arg2 ...
#程序到断点中断时，查看函数调用栈
(gdb) backtrace #或者直接(gdb) bt
(gdb) thread apply all bt #所有线程的bt, 更适合多线程程序
#断点中断后让程序继续跑
(gdb) continue
#终止程序
(gdb) kill
```

### 保存断点设置到文件

```bash
#保存断点到某个文件
save breakpoints <filename>
#执行某个文件到命令，如果正好是上边保存到断点文件，就是恢复断点啦
source <filename>
```

### 保存调试输出到文件

```bash
#设置输出的文件
(gdb) set logging file <filename> 
#开启log写入文件
(gdb) set logging on
#这时调试, 所有信息会保存在文件内, e.g.:
(gdb) bt
#暂停log写入文件
(gdb) set logging off
```