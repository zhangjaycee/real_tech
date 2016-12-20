# C语言中结构体struct初始化和赋值的几种方式

> http://stackoverflow.com/questions/330793/how-to-initialize-a-struct-in-accordance-with-c-programming-language-standards

在内核中`fs/ext3/indoe.c`中，一个struct初始化格式个这样的：
~~~cpp
static const struct address_space_operations ext3_writeback_aops = {
         .readpage               = ext3_readpage,
         .readpages              = ext3_readpages,
         .writepage              = ext3_writeback_writepage,
         .write_begin            = ext3_write_begin,
         .write_end              = ext3_writeback_write_end,
         .bmap                   = ext3_bmap,
         .invalidatepage         = ext3_invalidatepage,
         .releasepage            = ext3_releasepage,
         .direct_IO              = ext3_direct_IO,
         .migratepage            = buffer_migrate_page,
         .is_partially_uptodate  = block_is_partially_uptodate,
         .error_remove_page      = generic_error_remove_page,
};
~~~
我以前没见过这种形式，于是查了一下，原来这是属于C99的“新”特性。

## 初始化

对于最初(C89)一般形式的struct初始化，需要在大括号中按照成员顺序初始化，和初始化数组很类似；而C99支持乱序初始化，只要给出初始化的变量名，并且在前面加点，后边加等号即可。下面举例和c语言中一般形式的初始化结构体对比：
~~~cpp
/* 结构体定义 */
struct People {
    char * name;
    int age;
    int sex;
};

/* 形式1(C89，需要成员顺序初始化) */
struct People zjc= {"jayceezhang", 22, 1};

/* 形式2(C99) */
struct People zjc2= {
    .age = 22, 
    .name = "jayceezhang",
    .sex = 1
};


~~~


## 赋值

对于赋值，C99支持的方式更多样灵活，举例：
~~~cpp
/* 形式1(C89): 很好理解，就是分别赋值 */
zjc.name = "zhangjc";
zjc.age = 22;

/*
 * 形式2(C99): 可以理解为创建了一个临时struct People变量赋给了zjc,和初始化一
 * 个道理一样，可以顺序或者点名赋值，但是注意如果没被赋值变量会被覆盖成不明确的值，
 * 而不会保留原有的值，具体覆盖成什么值应该取决于编译器实现（比如gcc可能是0），所
 * 以个人感觉方式的赋值个人感觉更像是“重新初始化”而已。
 */

zjc = (struct People){"zhangjc", 22, 1};
zjc = (struct People){.age = 23, .name = "jcccc", .sex = 1};
~~~