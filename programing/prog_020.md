# 动态库和静态库

### 如何编译一个静态库：

比如有test.c和test.h文件：
```
# 这句生成test.o
gcc -shared -fPIC -DPIC -c test.c
# 这句生成libtest.so 动态库
ld -shared test.o -o libtest.so
```

---
[1] https://blog.csdn.net/linfengfeiye/article/details/6946407