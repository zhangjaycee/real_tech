# Linux下的find工具


### 按内容查找

* 查找某个目录[dir]下所有文件的某些内容[content]

```bash
find [dir] -type f|xargs grep [content]
```

### 按文件名查找

```bash
find [dir] -name [pattern]
```
例如：

* 查找某（几）后缀的文件

```bash
find [dir] -name "*.c" [-o -name "*.py"] [-o -name "*.h"] ...
```
这里的-o参数还可以写成-or， 就是或的意思。

* 查找名字包含某字符串的文件
```bash
find [dir] -name "*foobar*"
```