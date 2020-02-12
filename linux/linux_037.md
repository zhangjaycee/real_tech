# 内核调试技巧


## printk

```cpp
printk(KERN_INFO "xxxx");
```
类似于printf，但之前有一个调试等级的宏定义：
```
KERN_EMERG <-- the most important
KERN_ALERT
KERN_CRIT
KERN_ERR
KERN_WARNING
KERN_NOTICE
KERN_INFO
KERN_DEBUG <-- the least important
```
可以用`dmesg -wH`进行查看。


## dump_stack

调用`dump_stack()`可以打印调用栈，也是用dmesg查看。
