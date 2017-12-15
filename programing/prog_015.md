# C程序不都是从main开始的(gcc attribute的构造和析构函数)

这是GCC的一个特性，gcc可以使用attribute关键字，格式如下：
```cpp
__attribute__((attribute_name))
```
其中attribute_name中有两类`constructor`和`destructor`类似C++中类的构造和析构的概念，只不过是相对main()函数来说的。简单说，`__attribute__((constructor))`定义的函数在main前执行，`__attribute__((destructor))`定义的函数在main后执行。


## QEMU中的应用

QEMU中有很多"module"的初始化使用了`__attribute__((constructor))`这个特性，来在main前完成init过程。具体如下：

```cpp
// QEMU_2.10_SRC/include/qemu/module.h中：

#define module_init(function, type)                                         \
static void __attribute__((constructor)) do_qemu_init_ ## function(void)    \
{                                                                           \
    register_module_init(function, type);                                   \
}
#endif

typedef enum {
    MODULE_INIT_BLOCK,
    MODULE_INIT_OPTS,
    MODULE_INIT_QOM,
    MODULE_INIT_TRACE,
    MODULE_INIT_MAX
} module_init_type;
// 比如这里block_init函数被用在QEMU_SRC/block/*的qcow2等Format Driver中广泛应用，
// 其实就是间接调用了被__attribute__((constructor))调用的register_module_init()
#define block_init(function) module_init(function, MODULE_INIT_BLOCK)
#define opts_init(function) module_init(function, MODULE_INIT_OPTS)
#define type_init(function) module_init(function, MODULE_INIT_QOM)
#define trace_init(function) module_init(function, MODULE_INIT_TRACE)
```

* 以qcow2为例

```cpp
// qcow2 的init流程

block_init(bdrv_qcow2_init)                                                 ------------------------ qcow2.c
----+----- -----+---------
    |            |
    |            v
    |        bdrv_register(&bdrv_qcow2)
    v
#define block_init(function) module_init(function, MODULE_INIT_BLOCK)        ---------- include/qemu/module.h
                            ----+-------
                                |
                                v
                            register_module_init(function, type)
                                |
                                v
                            l = find_type(type)  -->  QTAILQ_INSERT_TAIL(l, e, node);   ------- util/module.c
```


[1] \_\_ATTRIBUTE\_\_ 你知多少？, http://www.cnblogs.com/astwish/articles/3460618.html

[2] QEMU在main函数前对模块的初始化过程, http://blog.csdn.net/u011364612/article/details/53581501