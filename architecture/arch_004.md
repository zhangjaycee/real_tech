## FPGA 架构

FPGA 即 Field Programmable Gate Arrays，现场可编程门阵列。如果逻辑代数为数字世界的理论指导，那么逻辑门电路就是盖起座座数字大厦的基本块块砖瓦，无论基本的数字电路还是现代的集成电路，无不构建在逻辑门之上，把逻辑门和时钟组合起来，人们搭建起了加法器、选择器、锁存器、触发器，进而的运算单元、可控制单元、RAM。按照聪明的工程师设计好的电路图纸再将这些基本的数字电路原件组合起来，再设计成可以印刷的集成电路形式，就可以构成各种专用的集成电路(ASIC)或者通用计算机处理器(CPU)等。FPGA相对ASIC来说更灵活。ASIC相对来说量产后会更廉价、节能，性能也更好。

专用集成电路只在意输入和输出，中间的一切算法会被固化到硬件设计中；而通用CPU则同时接收数据流和指令流，按照软件工程师的程序指令序列执行一些列计算任务(虽有人将CPU也归为ASIC，但是我觉得这是在硬件角度上来说的，从计算任务的可编程性角度CPU实际上是最灵活通用的)。FPGA则介于ASIC和CPU之间，它并非将逻辑门组成的原件之间的连接形式固化，也非做成最有利通用计算的形式动态地接收软件指令来调动片上已有的计算单元，而是可以通过重复硬件编程来改变它逻辑门所组成的基本功能单元和调整这些单元之间的连接关系。

### 1. 硬件架构介绍

#### 1.1 Overview

如下图所示，逻辑上，FPGA主要由可编程的逻辑块(programmable logic block, 主要是图中CLB) 和 可编程互联网络 (programmable interconnect network / routing interconnect, 主要是图中SB, CB和一些路由通道组成)。

```
+-----------+
|           |
|    LUT    +-+
|           | |    +--------+    +-----------+
+-----------+ |    |        |    |           |
              +---->   BLE  +---->    CLB    +----+
+-----------+ |    |        |    |           |    |
|           | |    +--------+    +-----------+    |
| Flip-Flop +-+                                   |
|           |          +---------------------+    |
+-----------+          |                     |    |
                       |    Switch Box (SB)  +----+
                       |                     |    |
                       +---------------------+    |
                                                  +---> FPGA
                       +---------------------+    |
                       |                     |    |
                       |    Connection Box   +----+
                       |        (CB)         |    |
                       +---------------------+    |
                                                  |
                       +---------------------+    |
                       |                     |    |
                       |    I/O Block        |    |
                       |                     +----+
                       +---------------------+
```

空间布局上，可以简单理解为下图[1]：

![fig3]

* 按编程技术分类FPGA

FPGA的基础，即可配置性依赖于存储这些硬件门配置的介质，这种区别也成为FPGA的编程技术，按照这种硬件编程技术分类，FPGA分为三类：**基于SRAM的FPGA**、**基于flash的FPGA**和**基于反熔丝(antifuse)的FPGA**[1]。

**基于SRAM的FPGA**是断电易失的，所以需要在开机(startup)时通过JTAG编程，或者通过内置/外置的非易失存储进行编程。

**基于flash的FPGA**的逻辑门本身就是非易失的。**antifuse FPGA**只能编程一次，不可逆。

#### 1.2 组成单元

* **Look-Up Table (SRAM based)**

k-bound LUT或称为LUT-k指的是有k个输入、2^k个配置bits的布尔函数逻辑。如下图[1]所示的basic logic element(BLE)由1个LUT-4和一个D型触发器(Flip-Flop)构成，其中多个LUT-4有16个SRAM构成的配置位，通过这些配置为配置这些选择器可以构成任意一个4输入逻辑单元。

![fig2]

这个例子中，配置数据存在SRAM中，基于这种BLE的FPGA可以称为基于SRAM(或说static memory)的FPGA。

* **Switch Box (SRAM based)**

如下图[1]Switch Box中，分为双向(a)和单向(b)，一般后者更常用。这些switch都是基于pass transistor[3]的，每个pass transistor可以独立地进行开关配置。

![fig4]

* **基于NAND Flash 的 FPGA 组件**

同样也有人提出基于NAND flash的FPGA，基于NAND flash相对基于SRAM，除了LUT、SB的配置形式需要重新设计外，NAND flash还具有NVM都有的非易失特点，可以减少外置flash存储的使用，在上电后不用重新配置。

但是当今的主流FPGA技术还是SRAM，因为它和一般的CMOS集成电路技术分享技术，可以得到集成度、速度和功耗上的不断提升。

一般的，要用Flash替代SRAM作为配置位，需要将SRAM cell替换为FMC(flash memory cell)，如下图以2-LUT为例[2]，每个FMC都由2个flash晶体管Fp和Fq组成。当然论文[2]的作者也提出了针对NAND Flash的更高效替代方法。

![fig5]

#### 1.3 IP核

FPGA的IP核(core)可以看做是软件中的各种库，避免了编程或设计人员重复造轮子。现代FPGA的可编程门阵列只占50%，其他大部分被硬IP核占据。

硬IP核是系统设计中一些常用的模块，直接以模块形式集成到FPGA的，比如memory block、calculating circuits，transceiver和protocol controller等，有些甚至加入了CPU、DSP等[6]。





### 2. 软件流程

软件流程也叫CAD(计算机辅助)流程，负责将人实现的上层应用逻辑映射到FPGA可编程硬件逻辑上，这个映射对最终的性能影响很大，所以这也是人们研究的一个重点。

这个过程将人写的硬件描述语言HDL转成可以最终编程到FPGA的比特流。这个过程大概分为5步： synthesis(综合)、technology mapping, mapping, placement, routing。CAD 工具最后生成的就是bit流。软件流程的框图[1]如下：

![fig1]

* **Logic Synthesis 逻辑综合** 将VHDL/verilog这类硬件描述编程语言转成布尔门、flip-flops。

* **Technology Mapping** 将上一步的逻辑门转成k-bound的LUT (lookup-table)。

* **Clustering/Packing** 将多个LB(即k-bound LUT + flip-flop对，或称BLE) 组成logic block clusters。主要有三种方法，各有利弊：

  top-down：k路分割问题的基本的cost function 是 net cut，即partition间的边数。

  depth-optimal：用逻辑的重复换取更快的运行

  bottom-up： FPGA CAD中用的比较多，因为运行快

* **Placement** 主要决定logic block 的放到FPGA哪个logic block 位置，以最小的wiring 为主(wire length-driven placement)。或者平衡wiring 的密度(routability-driven placement)；或者找到最快的电路速度(timing-driven placement)。常用partitioning或者模拟退火的方法
* **Routing** 阶段将网络关联到物理的routing网络，当前state-of-the-art 算法是pathfinder。

在这些阶段之后，还有时序分析阶段和bitstream生成阶段，最后的bitstream会真正的用于编程到SRAM存储位来配置逻辑门。



## 3. Host FPGA管理系统的发展

[4] 提出了一种"FPGA操作系统"， [5] 是对FPGA虚拟化的综述。

...

---

[1] U. Farooq, Z. Marrakchi, and H. Mehrez, *Tree-based heterogeneous FPGA architectures: Application specific exploration and optimization*, vol. 9781461435. 2012.

[2] M. Abusultan and S. P. Khatri, “Exploring static and dynamic flash-based FPGA design topologies,” *Proc. 34th IEEE Int. Conf. Comput. Des. ICCD 2016*, pp. 416–419, 2016.

[3] https://en.wikipedia.org/wiki/Pass_transistor_logic 

[4]  Jiansong. Zhang *et al.*, “The feniks FPGA operating system for cloud computing,” *Proc. 8th Asia-Pacific Work. Syst. APSys 2017*, 2017.

[5] A. Vaishnav, K. D. Pham, and D. Koch, “A survey on FPGA virtualization,” *Proc. - 2018 Int. Conf. Field-Programmable Log. Appl. FPL 2018*, pp. 131–138, 2018.

[6] FPGAs For Dummies, https://plan.seek.intel.com/PSG_WW_NC_LPCD_FR_2018_FPGAforDummiesbook