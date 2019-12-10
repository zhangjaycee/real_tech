# Flash相关 (NOR, NAND, Flash-based FPGA...)


## Flash用于数据存储

Flash 属于 Non-volatile Memory，可用于存储[1]。
![](https://www.embedded.com/wp-content/uploads/contenteetimes-images-design-embedded-2018-fl-1-f1.jpg)

NOR和NAND型flash对比如下[1]。

![](https://www.embedded.com/wp-content/uploads/contenteetimes-images-design-embedded-2018-fl-1-t1.jpg)

可以看出，NOR数据密度更小，随机性能更好，顺序读/写/擦的性能更差。NOR可以直接访问，所以代码可以直接存储/执行代码，NAND上的代码只能load到可以随机访问的memory上才可以执行。而且NOR的可靠性(data retention)要好一些。

所以NOR更适合可用于代码直接执行、更快随机读需求的场景。而NAND适合大规模应用数据存储和擦/写需求较多的场景。

## Flash-based FPGA

FPGA的逻辑门可以基于SRAM, antifuse或者是NAND flash，其中基于NAND的FPAG属于nonvolatile FPGA，因为断电非易失[2]。

---
[1] https://www.embedded.com/flash-101-nand-flash-vs-nor-flash/

[2] https://github.com/zhangjaycee/real_tech/wiki/arch_004

