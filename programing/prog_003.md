# Python语法注意点

* 由于python返回类型不固定，所以检查返回值时慎用`not`，它分不清0和None

比如，定义了一个检查栈最小值的函数，当栈为空时返回None，在有值时返回最小值。这是不能用 not 检查是不是空值，因为也可能返回的最小值正好是0，这样 not 0 和not None 都为真，应该用 == None 来确定返回是不是None。
(→[leetcode 155. Min Stack](https://leetcode.com/problems/min-stack/))


# Python 交互式终端中运行.py文件
```python
>>> execfile('xxx.py')
```