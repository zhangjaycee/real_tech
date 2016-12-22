# what's the differences between glib & libc & glibc & uclibc & eglibc 

其中，glib最为特殊，可以说和其它几种不是一类东西。

* __glib:__ 原属于GTK+的一部分，现在独立出来，gnome就是在它的基础上开发。它是实现C常用数据结构的一个库，就好比链表、树等常用数据结构里面都有实现，好比“轮子”。

* __(.?)libc:__ libc是指构建Linux操作系统的基石，是标准C库，但是是不同的实现，用的系统也不同，比如glibc是GNU libc, 用于linux系统; eglibc是Embbeded glibc,主要用于嵌入式系统; uclibc是用于嵌入式系统的轻量版libc,体积较小。


> http://www.linux-m68k.org/faq/glibcinfo.html

> http://bbs.chinaunix.net/thread-3762882-1-1.html