# C语言结构体的内存布局

### 1. struct成员的内存对齐

两个原则：

- 首先，struct成员是一个个放进去的，放进某个成员时，它的其实偏移应该是它自身大小的整数倍。若这个成员也是个struct，这个大小按它成员中的最大成员来计算。

- 其次，当成员被一个个放完后，struct末尾可能需要进行填充，填充到最大成员类型大小的整数倍。

### 2. 紧凑struct布局

两种方式[1]：

- 一种采用 `#pragma pack(N)` (N为对齐单位) `#pragma pack(pop)` 这对宏分别放在结构体定义的前后。

- 一种直接用`__attribute__((packed));`作为结构体定义的结尾，其效果相当于上一中N=1。

### 3. struct的位段(bit-field)

位段的定义格式为[2]:
```
type  [var]: digits
```
其中type只能为int，unsigned int，signed int三种类型。

一种紧凑的存储形式。。。待续。。。[3]

### 4. union

union和struct不同，struct中所有的变量都会一一排开，而union中所有成员都是从0偏移量开始的，所以一般同一时间只能使用一个，也只有那一个是有意义的。







[1] https://blog.csdn.net/zhangxiong2532/article/details/50826917

[2] https://www.cnblogs.com/bigrabbit/archive/2012/09/20/2695543.html

[3] https://en.wikipedia.org/wiki/Bit_field
