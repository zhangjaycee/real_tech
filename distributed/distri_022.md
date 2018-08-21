# 外存数据结构

(《basic external memory data-structure(Rasmus Pagh)》的笔记)

外存的“宏观结构”与内存的“微观结构”很类似。比如对于stack，内存中push和pop的单位是一个元素，而外存是一个block。(其实考虑CPU到memory的原子读写粒度和cacheline单元，内存也不是以元素为粒度)

1. stack和queue

平均每次插入或者删除需要1/B次I/O。(B：每个block可以装的元素数)

2. linked list

假定元素是有序的，可以保持每个块都不是满的，适时进行merge和split操作，方便插入操作。

3. dictionary

是一种抽象，类似现在的key-value接口。也是很多其他数据结构的基础。可以用树或者哈希实现。

4. B-tree

B-tree是二叉搜索树(binary searching tree)的变种，区别在于二叉树每个节点分2叉，而B树每个几点分N叉(N是一个磁盘block可以装下的元素数)，B+树则在非叶节点只存指针，N为一个磁盘block可以装下的指针数。

5. hashing

介绍了线性探测(开发寻址法的一种)、溢出链、完备哈希、可扩展哈希线性可扩展哈希、并行哈希等方法。
