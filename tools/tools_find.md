# Linux下的find工具


* 查找某个目录[dir]下所有文件的某些内容[content]

```bash
find [dir] -type f|xargs grep [content]
```

* 查找某（几）后缀的文件


```bash
find [dir] -name "*.c" [-o -name "*.py"] [-o -name "*.h"] ...
```
这里的-o参数还可以写成-or， 就是或的意思。
