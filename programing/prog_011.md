# 用C、Python和Shell语言在终端打印文本的格式和颜色


## 例子
以打印一个蓝色斜体的”hello, world“为例：
* C
```cpp
printf("\033[3;34mhello, world\033[0m\n");
```

* python
```python
print "\033[3;34mhello, world\033[0m"
```

* Shell
```bash
echo -e '\033[Para0{;Para1...}mhello, world\033[0m'
```

## 格式

```
\033[Para0{;Para1...}mYOUR_TEXT\033[0m
```

* `\033[Para0{;Para1...}m` 表示转义开始
* `\033[0m` 作为转义结束
* `Para0(1,2...)` 参数可以为多个，比如上述例子中，3表示为斜体，34表示蓝色
* `YOUR_TEXT` 在例子中就是hello, world


## 参数

通过man console_codes命令可查看详细的参数描述，这里写一下常用的格式和颜色：

* 常用格式：

|参数代码|描述|
|---|---|
|0|重制所有格式|
|1|粗体(高亮)|
|2|暗色|
|3|斜体|
|4|下划线|
|5|闪烁|

* 常用颜色：

(前景色为30+颜色代码；背景色为40+颜色代码。)

|颜色|代码|前景|背景|
|--|--|--|--|
|黑|0|30|40|
|红|1|31|41|
|绿|2|32|42|
|黄|3|33|43|
|蓝|4|34|44|
|洋红|5|35|45|
|青|6|36|46|
|白|7|37|47|

## 参考与扩展

> [通过printf设置Linux终端输出的颜色和显示方式](http://www.cnblogs.com/clover-toeic/p/4031618.html), clover_toeic, 2014-10-17
>
> [How to: Change / Setup bash custom prompt (PS1)](https://www.cyberciti.biz/tips/howto-linux-unix-bash-shell-setup-prompt.html), June 2, 2007