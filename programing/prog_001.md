# 老式C语言中函数定义的形参声明

> 参考：

> https://zhidao.baidu.com/question/397492523.html


> 老式c语言 形参类型能省，形参名不可以省。但小括号外，花括号前，要加形参类型声明：
```cpp
#include <stdio.h>
fun(a)
int a;
{
printf("a=%d",a);
}
main() 
{
int a = 123;
fun(a);
return 0;
}
```
结果输出 123