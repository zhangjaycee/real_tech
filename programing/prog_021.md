# define 和 enum


define 和 enum 有时用途类似，比如想定义API几种参数或错误类型：

```cpp
#define A 1
#define B 2
#define C 3
```
等价于
```cpp
enum Status {
A, B, C
};
```

主要区别在于：
- 程序员要主动保证define 的整数之间不重复，而enum则自动分配不同的整数。
- enum占用代码段空间，而define则在编译时替换，连gdb等debugger也无法再获知信息。

- 用16进制定义define，还可以使用与，或等位运算。。
