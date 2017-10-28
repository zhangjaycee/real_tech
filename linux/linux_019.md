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