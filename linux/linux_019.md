# linux 内核中的通用数据结构/设计模式

### Radix Tree

Radix Tree（基数树），是一中查找树，可以存K-V对。

[1] Data Structures in the Linux Kernel-Radix Tree, https://0xax.gitbooks.io/linux-insides/content/DataStructures/radix-tree.html

[2] https://stackoverflow.com/questions/3537027/which-is-faster-a-radix-tree-or-a-b-tree


### container_of 函数

已知一个字段的地址及名字、所属struct的名字，返回对应struct对象的地址指针。
```
container_of(已知的某字段的地址, 字段所属的数据结构类型名, 已知地址的字段的字段名)
```

> **Embedded Anchor**: A good way to include generic objects in a data structure is to embed an anchor in them and build the data structure around the anchors. The object can be found from the anchor using container_of().

[1] Linux kernel design patterns - part 2, https://lwn.net/Articles/336255/

### Link List

内核中实现了链表结构。


## for each宏定义

这种遍历链表的宏定义很常见，会用指定的语句代替for(;;)，可以简化C代码。

内核中`include/linux/list.h`文件中有很多种for each的实现，例如：

```cpp
/**
 * list_for_each    -   iterate over a list
 * @pos:    the &struct list_head to use as a loop cursor.
 * @head:   the head for your list.
 */
#define list_for_each(pos, head) \
    for (pos = (head)->next; pos != (head); pos = pos->next)
```
输入一个循环链表的头指针（表头为空节点），遍历一圈。

再比如QEMU中实现的队列，在`QEMU_SRC/include/qemu/queue.h`文件中：

```cpp
#define QLIST_FOREACH(var, head, field)                                 \
        for ((var) = ((head)->lh_first);                                \
                (var);                                                  \
                (var) = ((var)->field.le_next))
```

