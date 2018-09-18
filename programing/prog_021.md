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

主要区别在于，你要主动保证define 的整数之间不重复，而Status则自动分配不同的整数。

用16进制定义define，还可以使用与，或等位运算。。
