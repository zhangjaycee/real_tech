# OSTEP Part1(Virtualization) 笔记

大部分截图来自原书，贴出书的官方主页： 《[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)》
(作者Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau)。感谢原作者这么好的书。

## 第一节 进程的抽象

#### 1.1. 策略和机制

Policy在mechanism（策略和机制）在操作系统中通常是分开设计的。比如如何切换上下文是一个low-level的mechanism，指底层的方法或者协议。当前时刻应该让哪个进程运行更好是一个high-level的policy的问题，指一些“智能”的调度。


#### 1.2. 虚拟化和OS

OS本身就可以看做是“虚拟机”(virtual machine)。系统通过在可以被接受的合理开销（时间、空间）范围内，将计算机CPU、内存、存储等资源进行虚拟化（抽象），目的是为了用户的方便使用。

**CPU虚拟化** 主要体现在将任务抽象为 **进程(process)** ，将资源按进程隔离，然后多个进程轮转使用计算资源； **内存虚拟化** 主要体现在 **虚拟地址空间(virtual address space 或 adress space)** ；而对于持久化的 **存储** ，OS让文件共享，没有那么多私有隔离，OS假定用户会用文件来共享数据。 (？？？？)

## 第二节 进程API

#### 2.1. fork和exec

exec()函数组和fork()的区别是：fork()复制当前进程为一个子进程执行，exec()会执行一个新的程序；exec()执行以后就再也不会返回。

#### 2.2. shell和stdout redirect

例如shell就是一个普通的用户程序，利用了fork和exec的组合。给出一个提示符，你输入可执行程序时，会先fork()，然后在fork出的子进程中exec()这个命令，然后调用wait()来结束。这种fork和exec的组合使用，可以在让shell在fork后运行一些其他代码：fork后的子进程可以redirect操作再exec；fork后的父进程可以执行wait操作在exec结束后再显示提示符prompt。

stdout redirect的原理很简单，stdout一般的fd都是0，在fork后的子进程中close掉stdout，然后打开要redirect到的文件，这个文件就会获得为0的fd，这时执行新命令的exec，则会把这个为0的文件看做stdout进行输出，程序清单如下图：

[[p1_001.png]]

#### 2.3. 其他

kill()可以向进程发送信号，让程序sleep, die。

## 第三节 机制：有限的直接执行(Limited Direct Excution)

为了实现多个程序在同一个机器上执行，即CPU时间被多个进程共享，需要一种称为Limited Direct Excution(LDE)的机制。若单说Direct excution，指的是程序直接在CPU上执行（类似单片机？），OS对各程序加以限制，让进程间交替执行，即LDE。

#### 3.1 用户空间和内核空间的切换

**用户程序操作受限**

OS的执行模式可以分为 **kernel mode** 和 **user mode** ，kernel mode下内核程序代码可以为所欲为，而user mode下的应用程序是受限的：比如，user mode程序无法直接进行IO请求，这种限制是必要的，因为OS不希望用户随便更改磁盘，而且OS的FS也希望用户访问文件前检查用户的访问权限。

**系统调用并陷入内核**

**系统调用(system call)** 可以说是连接用户空间和内核空间的桥梁。用户程序想执行受限的操作，需要通过OS的系统调用来 **陷入(trap)** OS内核。（这就类似于OS是个代理，特殊的操作都要由内核程序经手办理。最开始OS的系统调用可能有二十种左右，现在一般OS都有几百种系统调用。）

系统调用并陷(trap)入内核的流程可以看成是LDE执行协议，如下图，分为两段，第一段是系统启动时的向硬件的注册，第二段是正常运行：进行系统调用时，控制权将从用户程序转交内核，这需要用户程序执行trap指令，硬件首先会把当前程序的寄存器信息备份（x86下会将PC、各种标志位等寄存器push到对应进程的kernel stack中），然后根据（系统启动时注册到硬件的）系统调用trap表jump到指定的内核代码，OS内核为所欲为地执行完后，会最后执行return-from-trap指令，恢复用户程序寄存器(pop from kernel stack)，用户程序会继续运行。

[[p1_002.png]]

比如，open()等函数就属于系统调用，在open的C库中，会有进行trap的汇编指令，所以我们可以直接调用系统调用函数，而不用写汇编，因为已经有人封装好了。

#### 3.2 用户空间多个程序的切换(交替执行)

要使多个程序一起执行，需要OS进行整体的控制和调度，但是当用户程序在CPU运行时，意味着OS没有在运行，所以要在程序间复用CPU，OS需要频繁地拿回控制权并向多个进程进行分配。

早期的苹果系统和Xerox系统等采用了一种和谐 **“合作”方式** 处理这个问题，OS相信用户会调用一个成为yield的系统调用，主动交出控制权给内核。但是这样并无法保证程序不存在恶意，OS只能期望程序交出控制权或者程序执行出错（illegal operation）。

最常用的方法是用 **timer中断方式** 保证OS可以拿回控制权。系统启动时会设定一个定时器，若一个进程在一定时间没有放弃控制权，timer中断也会把控制权“夺回”给OS，OS决定是继续执行当前进程还是将时间片分给其他程序。需要注意的是，在这个过程中，存在两中保存和恢复(saves/restores)寄存器的过程：首先，在timer中断时， **硬件** 会保存当前程序A的寄存器以便恢复执行；其次，如果OS决定从A切换到B，需要 **软件** (OS)将A的寄存器保存到memory中。

中断还存在很多并发的问题，比如OS会在中断代码执行时禁止中断，并会引入很多锁保证内部数据结构的并发访问，书的第二部分将详细讨论。

## 第四节 进程调度

**workload的信息**

讨论调度首先要了解workload（当前系统运行的进程集），有时条件比较宽松，比如知道任务同时来，任务长短已知等，这时SJF(short job first)这种简单调度就是最优的；但一般情况下，workload的很多信息并无法预知，所以需要更复杂的调度方法。

**调度的metrics：完成时间和响应时间**

有两个衡量调度优劣的评判标准，Turnaround time和response time，一般两者不可兼得。

#### 4.1 调度思想

两种简单的 **非抢占(non-preemptive)调度** ，任务是一个接一个执行的：

* **FIFO** 或者称为FCFS，最简单，但是可能引起convoy effect（护送效应？），即第一个任务时间很长，后边的任务需要等很长时间。

* **SJF** 改进了这种情况，让最短的任务最先执行。

但是，实际中的任务一般不是同时到达的，如果短的任务来晚了一会，长的任务已经执行了，又要等很长时间。于是有了 **抢占式(preemptive)调度**：

* **STCF** 即shortes time-to-completion first，或者叫 **PSJF** (Preempttive Shorted Job First)，**改进了SJF** 可以在预知完成时间的情况下，让可以先执行完的任务抢占执行。

但是，实际中很少知道任务什么时候将执行完一般很难知道，为了保证响应时间，有了 **时间片(time slice或scheduling quantum)** 的概念：

* **Round Robin** ,简称 **RR** ，是一种轮询调度，保证了响应时间，但是完成时间确是最差的。另外时间片的长短选择时，有一个 **trade-off** ：即进程的上下文切换需要时间，如果时间片太短，则会导致用在切换的时间太长，时间片太长，又会导致响应时间变差，这也是一个时间 **分摊(amortize)** 的问题。作者之后讨论的调度多是基于时间片的调度。

#### 4.2 进行磁盘I/O的进程的调度

一个进程进行IO请求后，很可能会阻塞，但是这个阻塞并不占用CPU，因此这是应该利用这个时间去执行其他的进程，这样可以提升CPU利用率。当IO完成时，一般会有中断发生，这时OS才把进行IO的进程改回“ready”状态。

#### 4.3 多级反馈队列调度(MLFQ)

Multi-level feedback queue主要通过"learn from history"的方法，解决完成时间(turnaround time)和响应时间(response time)的优化问题。

MLFQ有多个queue，每个queue有不同的优先级，并且可以根据任务执行的情况调整优先级：若任务在时间片结束前就放弃控制权，说明是 **交互型任务** (类似latency-sensitive任务)，放在高优先级；如果每次都用完了时间片，说明是 **CPU-bound** 的任务(类似best-effort任务)，对响应要求不高，放在低优先级。比如对于鼠标键盘等IO，时间片结束前就会放弃CPU控制权，从而保持高优先级，保证了响应时间。

但是这种优先级调整会遇到几个问题：

**饥饿问题(starvation)** 如果高优先级的任务太多，低优先级队列的任务永远饿着，解决这个问题的办法是定期的 **优先级boost** ，即定期(如1s)将任务全调到最高优先级，这样可以防止饥饿。但是这个周期S参数怎么选又是个 **trade-off** ：太长的话，低优先级队列的任务就要饿很久；太短的话，对响应要求高的任务就不能更好地工作。

**欺骗问题(game the scheduler)** 既然执行完时间片会被降级，那么执行99%的时间片再放弃CPU，会同时获得高优先级和大量的CPU时间，这种欺骗是恶意的，会导致系统性能问题。解决的方法是将各个优先级间调整的依据（时间片）改为更精确的计时，高优先级的队列要求的时间更短，向下的优先级逐级递增（**优先级越低，时间配额越大**）。这里当然还会有很多参数设定的问题。

**任务特征变化的问题** 任务不都是一成不变的，可能由CPU-bound型转为interactive型。这个问题也可以通过定期 **优先级boost** 解决。

**参数设定的问题** 队列数目、队列长度、boost周期、优先级调整时间配额等都是可变的参数，但是这个参数很难调。我们大家都知道，多数用户从不改默认参数，改的话也可能越改越差，这个问题很难解决。有些系统给出了方便调优的工具，有些利用了应用或用户的建议(advise)或提示( **hint** )，比如进程优先级 **nice** 和内存管理 **madvise** 等。

MLFQ达到了一定的fairness，BSD UNIX的衍生版本、Solaris、Windows NT及后续版本都在用它作为基本调度器。

#### 4.4 按比例(Proportion-Share)调度

比例调度(proportional-share scheduler, fair-share scheduler)保证了fairness，保证某个进程得到一定比例的CPU时间。

主要介绍了两种方法： **lottery scheduling** 和 **stride scheduling** ，前者为不同人物分配不同数量的ticket，然后随机选一个数，根据概率决定下一次哪个进程执行；后者根据步长，将每个任务的“计步器”初始化为0，CPU配额大的任务步长小，每次步数最少的程序执行。

stride scheduling更精确，因为没有随机数的应用；lottery scheduling更灵活，因为中途可以很方便地加入新的任务而不用新的初始化。

而且，lottery scheduling有很多有趣的玩法，ticket可以看成一种通货( **ticket currency** )，这种ticket通货在进程间进行转增( **ticket transfer** )、可能发生“通胀( **ticket inflation** )”的ticket增发等。ticket转赠即一个进程可以将自己的ticket划给其他进程，这样CPU比例就发生了变化；如果进程间 **相互信任** ，还可以允许某个进程暂时凭空增加（借贷）和减少（放贷）ticket数目，这可能引起问题，但的确很灵活。这种讨论还可以参见[1]。

ticket assignment problem是指应该怎么指定给每个进程发多少tickets的问题，这个问题是开放性的。

---

[1] Lottery Scheduling, https://cs.nyu.edu/rgrimm/teaching/sp07-os/lottery.pdf


## 多核

详细在书的第二部分讲。

*BFS[1]

## 第五节 地址空间

#### 5.1 内存虚拟化

多进程OS的资源共享策略

本书上半部分讲了CPU的共享策略：通过进程(process)这个抽象，OS将时间片分给进程。

对于内存资源的共享：为了让昂贵的计算机能够支持多个程序同时运行，如果在切换某个进程时将内存数据从磁盘换入（进程共享磁盘，内存和寄存器都不共享），由于磁盘IO太慢，不现实。所以现在的系统，都是将相对较快的寄存器换入换出 ，所有进程数据共享内存资源（ **寄存器不共享，内存共享** ）。为了实现这种想法，并更好地管理内存， **地址空间(Address Space)** 的抽象被引入（如下图），相对为每个程序固定分配一定大小的内存空间更灵活，用地址空间进行管理更加灵活。

[[p1_003.png]]

地址空间在 **结构** 上主要分为Code、Heap和Stack，Code部分用来存程序运行的代码，Heap是用户程序动态分配内存(malloc/free)所使用空间，Stack是变量使用的空间。除非程序递归很多，一般Stack都是够用的；如果程序视图访问非法地址，可能出现Segmentation fault的错误。

每个进程都会有一个自己地址空间，且每个进程都认为自己的地址空间是从0开始的，并且地址空间的地址也不必和物理地址相等，甚至地址空间的总大小可以大于物理内存大小，这就体现了一种 **内存虚拟化** 的概念，OS的内存管理系统也可以称为 **虚拟内存系统(virtual memory system, VM)** 。因此，我们编写的程序中，所有我们可以得到的地址也都是虚拟地址，并非物理地址。

VM系统设计的三个目标：**透明(transparency)、高效(efficency)** 和 **保护(protection)** 。其中保护即隔离(isolation)，进程间的地址空间需要隔离，进程和OS间也需要隔离，（甚至在有些微内核操作系统中，OS的一部分和OS的另一部分也进行了隔离），这样可以保证安全性。

#### 5.2. memory API

对于用户程序，Stack中的变量是自动管理的，比如用int声明一个整数变量，而Heap中的内存是由程序（程序员）负责的，什么时候malloc/free都要程序员进行考虑，所以要格外小心一些常见的malloc错误，比如忘记分配内存、分配的不够导致buffer overflow、忘记初始化所分配内存内容、忘记free等。 **purify** 和 **valgrind** 这两个工具可以协助检测内存分配的问题。

#### 5.3. malloc、free和mmap的关系**

要注意 **malloc/free并不是系统调用** ，它们是基于brk和sbrk等系统调用的库函数，但我们使用时不应该直接使用brk等，而应该坚持使用malloc/free函数。

传入某些参数后， **mmap** 函数也可以从OS申请内存，OS会在你的程序中创建匿名(anonymous)内存区域（一个和swap space相关的区域，而不是某个文件），这个区域可以像Heap一样进行管理。

需要注意的是，mmap是系统调用，mmap也是malloc函数分配给用户程序内存时所基于的系统调用之一。在嵌入式领域,mmap可以将外设寄存器的地址（物理地址），映射到用户内存空间。实现在用户态下操作寄存器，进而实现用户态下驱动程序的作用。[2]

#### 5.4 地址转换机制

由于地址空间的地址是虚拟地址，需要进行虚拟和物理地址间的转换，硬件的介入(interposition)可以加速这种转换。（“介入”不只在硬件，软件层次中也经常用到，以透明的方法两个层次的中间加入功能或改进性能）

**1. 软件实现：** 在硬件加速出现之前是 **software-based static relocatin** ，方法是OS有一段称为loader程序负责转换地址。但这样缺点是进程间没有保护，而且一旦地址空间被放置，以后很难进行重新放置。

**2. 硬件实现(base and bound)：** 50年代进行"hardware-based dynamic relocation"的思路是通过 **base and bound** 硬件寄存器进行辅助，物理地址一般就是base地址加上虚拟地址，bound寄存器用于存储地址空间对应区域的大小或者结束地址，用于检测转换后的地址是否合法。辅助内存管理的硬件称为 **MMU(memory management unit)** ，base和bound寄存器就属于MMU。

为了实现base and bound，OS需要在进程 **创建、结束或切换** 时进行对应的操作。创建进程时时需要找到空闲足够的物理地址空间(最简单的，OS可以用 **free-list** 实现)；结束进程时，需要进行内存的回收；进程切换时，需要保存和恢复(save and restore)base和bound寄存器的内容，将要切换出的进程寄存器会保存到对应的PCB(process control block)中。这种硬件实现还可以方便地址空间的随时移动，一个没有正在运行的程序，只需要将地址空间拷贝到新的地方，然后更新PCB中base寄存器的内容即可。

## 第六节 segmentation(分段)管理

#### 6.1 地址空间分段

上述的地址空间这个抽象，是内存虚拟化最基础的思路。但是这种最基本的结构有个显著的缺陷：**internal fragmentation（内部碎片）** ，即某个地址空间中如果stack和heap之间有很多空间没有使用，一旦分配，也不能给别的进程使用，这便造成了空间的浪费。

于是，60年代，人们引入了 **分段segamentation** 的思路，即将地址空间分成code、heap和stack三个逻辑段，每个段分别有一对对应的base和bound。（我们常见的segamentation fault错误，就是源于访问了非法的内存空间地址）有了段，我们可以在物理上将三个段分开放置，解决了内部碎片问题。

#### 6.2 分段地址转换

引入分段后，虚拟地址可以看成两部分组成（如图）：段地址(segment)和偏移量(offset)。这样如果一个地址空间分了3个段，就相当于原来的地址分了前两位出来表示段，offset的作用和原来的地址作用类似。

[[p1_004.png]]

#### 6.3 外部碎片问题和空闲空间管理

引入分段，虽然解决了内部碎片问题，但是会导致 **外部碎片** 问题（空闲空间都不连续）。为解决外部碎片问题，可以定期进行段移动整理碎片(compaction)，但是这样性能开销很大；或者用free-list采用best-fit、worst-fit、first-fit等短发进行空闲空间的管理。

其实不管是上述讨论的OS的内存的分段管理，还是malloc/free这种进程heap的内存管理，都可能导致外部碎片（相对内部碎片，我们更担心的外部碎片），需要进行 **free space management** 。本书以malloc/free内存分配库为例进行了讲解：（详见课本）

**1. low-level机制：** 最简单的，free-list通过malloc时的 **分割(splitting)** 和free时的 **合并(coalescing)** 进行管理，但是在内存分配库中，无法用malloc进行free-list节点的空间的分配，这时，需要用mmap申请内存，并将free-list的结构嵌入到整个所申请的内存中。

**2. 基本策略：** 策略有best fit、worst fit、first fit、next fit等。其他的策略还有segregate list、伙伴算法等，伙伴系统可以避免外部碎片，但是由于所分配只能是2的倍数，无法避免内部碎片。后来有些系统考虑到list搜索效率低带来低scaling的问题，引入了平衡树等结构来构建空闲内存管理。

## 第七节 paging(分页)

分段带来的碎片问题很让人头疼，所以在很早的60年代，人们也提出了分页(paging)的思路，将内存分成固定大小的页，这比分段更灵活和简单。

#### 7.1 地址转换

分页也是在虚拟地址空间上进行的，为了进行地址转换，基本思路是每个进程会配有一个 **page table** ，存有虚拟页号VPN(virtual page number)到物理页框PFN(physical frame number)的映射。

地址的格式和分段类似，也是有若干位被分出来作为VPN，进行转换时，类似分段借助base寄存器，分页则借助于page table，offset为页内地址，不用转换，如下图：

[[p1_005.png]]

page table 由 page-table entry(PTE)组成，一个x86的PTE如下：

[[p1_006.png]]


#### 7.2 TLB(translation lookaside buffer)硬件加速

#### 7.3 高级页表(Advanced Page Tables)

## 第八节 交换空间

#### 8.1 机制

#### 8.2 策略

## 第九节 实例：VAX/VMS内存管理系统

---

[1] http://ck.kolivas.org/patches/bfs/bfs-faq.txt

[2] linux mmap匿名映射的作用是什么？ https://www.zhihu.com/question/57653599


# OSTEP Part3(Persistence) 笔记

大部分截图来自原书，贴出书的官方主页： 《[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)》
(作者Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau)。感谢原作者这么好的书。

## 第一节 I/O Device

#### 1.1 IO 总线

**一般情况下，** IO设备的性能较差(慢)，所以用Peripheral IO Bus，为什么不用像显卡一样用的PCI呢？因为1)越快的总线越短，这样空间不够插；2)越快的总线制作成本越高，如果存储设备照总线的性能差的远，没必要用高性能总线。

[[p3_001.png]]

这张图为总线的层次结构，memory bus是最快的也是最近的，IO Bus比较远，也是最慢的，中间有用于显卡的PCI等总线。

#### 1.2 典型设备的组成部分

[[p3_002.png]]

一个典型的外围设备如图所示，包括两部分： **接口** 和 **内部结构** 。

**接口：** 类似软件接口的功能，硬件接口是留给OS和设备交互的。
**内部结构：** 比如㓟CPU、MEM等基本组件，还有称为固件(firmware)的软件来实现内部功能。

#### 1.3 PIO中的两种模式(Polling和Interrupt)

一种典型的协议是 **Polling** (轮询)，步骤有4: 

* 循环等待STATUS寄存器直到设备状态为不busy
* 写数据到DATA寄存器
* 写命令到COMMAND寄存器
* 循环等待STATUS直到设备为不busy

Polling显著的缺点就是太浪费CPU时间，这是因为IO相对于CPU是很慢的，大量的CPU时间被用在了等待上。

**Interrupt** (中断)方法可以解决这个问题，用Interrupt方法进行IO时，当设备完成操作时，会raise一个硬件interrupt。但是这样的话，如果设备很快(不如现在的NVMe SSD设备)，Interrupt由于需要进程上下文的切换、以及中断的控制等原因，会拖慢IO的速度。所以两种方法各有利弊：

|Polling | Interrupt |
|--------|--------|
| 浪费CPU时间 | 节省CPU时间 |
| 更小的I/O延迟 | 进程切换及中断处理导致高延迟 |

在IO请求压力时大时小不好确定的系统中，更好的方案可能是采用hybrid(混合)的 **两段协议** ，先poll一会儿，还没完成的话改用interrupt方式。还有一种方式是 **中断合并** ，当一个请求完成，等一等，说不定又有新的请求完成了，这样就见小了中断数，减小了中断带来的性能损失，但是这样做的缺点也是显而易见的--用延迟代价换来了高吞吐。

#### 1.4 设备交互：PIO和MMIO

以上的Interrupt和Polling都属于Programmed I/O(PIO)的方式，这种方式是CPU通过指令和设备进行的交互。

还有一种称为Memory-mapped I/O(MMIO)，这种方法中，设备寄存器被映射到内存地址空间，OS读写这个映射地址，硬件会自动将存取数据路由到设备而不是主存中。

#### 1.5 PIO中传输任务的卸载(Direct Memory Access, DMA)

若不使用DMA，虽然可以用中断来讲等待设备IO完成的时间用在其他进程上，但是IO请求中还包括CPU从内存到设备以字长为单位一点一点搬运数据（数据传输）的过程，如图：

[[p3_003.png]]

有了DMA这种专用设备帮CPU搬运，流水线就可以入下图一样：

[[p3_004.png]]

当DMA完成任务，DMA控制器会raise一个中断，这样OS就知道传输完成了。

#### 1。6 设备驱动和I/O栈

I/O栈各层的抽象(如块设备驱动、文件系统等)当然有好处，其把不同的设备封装成统一的结构，但也有坏处。

其实不是从上层应用到底层驱动会出现信息丢失的问题(我曾经调研过上层到下层会有语义鸿沟的问题)，底层的设备由于统一的抽象也会“丧失个性”，比如SCSI支持多种IO错误信息，但是ATA/IDE却不支持，因此Linux设计成上层文件系统只能接到更"EIO"错误(generic IO errer)。

驱动占Linux源码的70%，很多驱动都是“业余”开发的，因此很多系统崩溃也是由于驱动bug造成的。

## 第三节 RAID

书中有个对比表总结的不错：

[[p3_005.png]]]

## 第四节 文件和目录

文件(file)和目录(directory)是OS虚拟化中存储部分的两个重要的抽象概念。

本节主要解释一些基本的文件操作和对应的系统调用。比如：

| 常用操作 | 系统调用 |
|--------|--------|
|  cat命令   | open() / read() / write()  |
| 数据同步  |   fsync()     |
|   mv命令重命名   |   rename()     |
|  ls的-l参数、stat命令    |   stat() / fstat()      |
|    rm命令    |    unlink()    |
|     mkdir命令    |   mkdir()     |
|文件夹操作函数|opendir() / closedir() / readdir()|
|rmdir命令|rmdir()|

这节还讲了硬链接和软连接、创建和挂载文件系统的内容，略了。。


## 第五节 文件系统的实现

本节主要讲，要实现一个文件系统的基本功能上应该怎么实现。

#### 5.1 文件系统的根本

对于文件系统，我们头脑中应该有一种模型：文件系统(Filesystem, FS)由接入部分和基本数据结构部分组成。前者指的是read()、write()等这样的接口；后者关系到FS内部怎么组织存储用户数据和元数据。设计时，不同的文件系统一般都有相同的接口，不同FS的主要区别是内部的 **数据结构** 。

#### 5.2 整体结构

文件系统内的数据可以分为用户数据(data)和元数据(metadata)，元数据可以简单的理解为数据的数据。上节所讲的文件系统的两种重要抽象（文件和目录），都需要存储data和metadata。

**data：**
  * 文件的data自然是用户数据，我们不需要关注用户数据的具体内容；目录的data应该存储文件名和对应文件的metadata。

**metadata：**

  * **inode** 文件的metadata是inode(曾经是index node的缩写)或者类似inode但不叫inode的东西；目录的metadata也是inode。inode以某种结构存储有对应文件或目录的数据块地址。
  * **bitmap**(或free list) 是与整个文件系统空闲空间相关的metadata，FS需要分配新空间时，会从这里查询哪里有空闲位置。分为data的bitmap和inode的bitmap。这里的bitmap也可以换为使用free list其他的数据结构。可以说，bitmap是metadata(文件和目录的inode)的metadata和data(文件和目录的data)的metadata，不过也还是metadata。。。
  * **superblock** 记录有文件系统最大inode数、inode块和数据块从哪个地址开始等信息，是整个文件系统的metadata。

#### 5.3 Inode

**组成：** 每个inode都有一个inumber，由于inode是顺序排列的，给定inode table开始块的地址、inode的大小和inumber就可以知道这个inode在哪个块了。inode中包含的信息包括：type（一般文件还是目录）、size（文件大小）、各种时间信息、指向数据块的地址“指针”（索引）等。

**数据块地址索引：** 其中的地址“指针”可以分为两类，最简单的直接指向相关的data块，称为direct pointer；另一种更常应用的交indirect pointer。

为什么要用indirect呢？因为一个inode的空间是有限的，如果文件数据太大，inode中留给存储块地址的空间装不下。于是就有了间接的两层索引、三层索引这种结构。例如，三级索引中，总共inode有n个地址空间有a个直接索引，b个二级间接索引，c个三级间接索引，那么有`n=a+b+c`；如果设一个数据块可以存m个索引，块的大小为4KB，支持文件的最大大小为`4KB * (a + b * m + c * m * m)`。

显然，这个多级索引结构是个非平衡树，也是不对称的，看了让人挺难受（强迫症），为什么这样设计呢？这是出于多数文件都很小的事实。

**FAT的链式存储：** FAT等FS没有inode，而是只存储第一个数据块的地址（类似链表头），然后下一个块的地址可以去前一个块找。这只是道理上的，如果真的这么做，随机访问肯定超级慢，所以还内存中存在一种存有连接信息的表，（可以看成key-value形式，用块的地址作为key，用下一个块作为value），这样就可以在内存中完成“链表的遍历”，加速了这种思路。这种结构的缺陷之一是无法创建硬链接。

书的作者给出了几种事实对设计FS很有借鉴意义：

| 事实 | 数据 |
|--------|--------|
|  多数文件都很小 |  多数都在2KB左右      |
|   平均大小会大一些     |  200KB左右      |
|   大多数数据都在大文件中     | 少数的大文件占据了大部分的空间     |
|   文件系统有很多文件  |  平均接近100k个     |
|   文件系统一般都是没满的 |  即使磁盘空间在变大，还是有50%空间空闲      |
|  目录一般都很小      |   平均小于20个项     |

#### 5.4 目录的组织

在作者的例子中，目录和文件是类似的，都有inode，只不过目录的data中有文件名和文件inode地址的映射，这是一种类似线性链表的结构，所以目录如果深的话查找开销会比较大。

目录的组织是对数据结构的一种设计和选择，当然也可以有不同的选择，比如XFS就采用了B-tree作为目录的存储组织结构（这样在创建文件时也很容易确定是不是重名）。

#### 5.5 空闲空间的管理

和目录的组织一样，作者的例子用了bitmap，但还可以用free list链表形式或者B-tree(XFS)等很多形式进行管理，这将导致性能和空间的trade-off。

当使用空闲空间时，尽量将连续的空间分配给需要的文件，这样的启发式方法会增加文件读写的速度（请求次数更少、一次顺序读写更多）。

#### 5.6 read()和write()的过程

作者的例子中，一次读或写请求会导致多次IO。尤其对于写时不存在的文件进行creat操作时，需要更多的IO，因为要逐级更改上层目录data和inode等。读和创建文件的操作如下两图：

[[p3_006.png]]

[[p3_007.png]]

#### 5.7 缓存和缓冲区(caching and buffering)

现代系统一般将virtual memory pages和文件系统pages合并成统一的page cache(unified page cache)，这样内存可以被更灵活的在虚拟内存和文件系统间分配（？）。

write buffering是有好处的，等一等再往下存，可以batch一些请求或者减少请求（如创建后马上删除），现在的文件系统一般都会等5s或30s之类的。这样做是有trade-off的：增加了延迟，增加了系统crash时数据丢失的可能。DBMS等系统决不允许这样导致数据丢失，因此可以勤用fsync()同步、用direct I/O绕过缓存或用raw disk接口绕过文件系统。但是一般这种trade-off在作者看来是可以接受。


## 第六节 局部性和FFS(Fast File System)

本节主要讲了FFS，一种84年提出的Unix文件系统，ext2和ext3的前辈。

在FFS之前，磁盘的性能很差，主要是因为人们没有考虑底层磁盘的特性，把磁盘当成了一个随机存储设备。例如，相对更古老Unix FS中的碎片没有被适当的处理，越来越碎，性能越来越差；而且块太小只有一个扇区的大小，这会导致开销增大（传输一次的量太小了）。

#### 措施1：分组存储

将整个文件系统分成Cylinder Group，每个Group都类似一个文件系统，甚至有冗余的Superblock。ext2和ext3中把这种结构称为block group。

这样存储就可以实现一些策略，这些“启发式”的策略并不是通过详细的论证得到，都是基于经验的，也是很管用的：1）将相关的文件（如同一个文件夹中的文件）放到一个组中（空间局部性，虽然FFS考虑了空间局部性，但没有考虑时间局部性，比如编译文件夹和源码文件夹在相距很远的两个目录里，就可能导致反复的查询）；2）创建文件时平均让各个组的空余inode数平衡等。


#### 措施2：大文件的分组存储

大的文件如果大到占了一个组的大部分，就开始破坏组内的局部性了，因为很少有地方可以存相关的文件了。因此可以根据预先设定，一个组内一个文件最多存多少块，如果多于这个数，就把一个文件分在多个组中存。

这样固然会降低存储效率，但是降低的应该不多，因为即使分块了，大文件的每个块依然较大，一次还是可以传输较多的数据，这样，传输所占的时间还是远大于请求所占的时间。这也是可以用数学公式计算一下比例的（摊还分析），作者在书中进行了推导，要达到50%的带宽，一个块400K即可，要达到99%的带宽，一个块需要40MB。（当然这只是针对磁盘，现在的高性能设备就不一定了！）

作者还讨论了HDD中顺序请求也可能让磁头旋转可能过头的问题。解决方法如图，具体解释，略。。。

[[p3_008.png]]


## 第七节 FSCK和Journaling


#### 7.1 Crash Consistency

FS的数据结构和其他内存中的数据结构不同，必须持久化存储。但是由于一次写请求是必定引起多次的磁盘IO（比如，要更新一个文件，需要更新或添加数据块、更新inode信息、可能更新bitmap块等。），若在一次写请求的多次IO之间系统崩溃了（可能由于断电等原因），那么文件系统结构就可能出现不一致。作者将这个问题成为crash consistency问题，并假设一次写请求分解成了3次基本IO操作（更新数据块、更新inode块、更新bitmap块），总结了几种情况，总结如下表(F for finished, N for not finished)：

| 数据块 | inode块 |bitmap块|一致性|备注|
|--------|--------|-------|----|---|
|N|N|N|一致|相当于什么也没干，FS一致，虽然写没有成功|
|N|N|F|不一致（bitmap和实际占用空间）|若bitmap记录了分配了新空间，可能导致“空间泄露”（道理类似内存泄漏），|
|N|F|N|不一致（inode指针和实际存储位置）|这时inode指向了并未更新的数据块，后续的读操作会返回一堆“垃圾”数据|
|N|F|F|不一致|同上，可能读到“垃圾”数据|
|  F  |    N    |    N |一致|虽然写请求没有成功，但因为bitmap和inode都没变，写入数据块只是相当于白写了，没有引起不一致|
|F|N|F|不一致|由于inode没有更新，可能读不到更新的数据块|
|F|F|N|不一致（bitmap空闲空间和实际所用空间）|未更新的bitmap可能导致再次申请时覆盖有效数据|
|F|F|F|一致|请求正常完成了|

FSCK和Journaling是保证crash consistency的两种最基本、最广泛的方法。FSCK即File System ChKer, Journaling又可以叫logging，都是保证crash consistency的方法。这些保证只是说保证系统不发生错误，无法保证写请求的成功。（类似DBMS的事务，consistency就是一次事务要么完了，要么没发生过，不能发生一半）

#### 7.2 FSCK

思路很简单，在每次FS挂载时，进行FSCK检查，进行必要的修复。 **缺点是很慢，因为每次都要全局进行检查。** 检查方法如下：

**Superblock** 检查超级块有没有异常，如果有异常，会启用备用超级块。

**Bitmap** 逐一检查inode和indirect块，生成一个记录分配情况的新bitmap，这样就不会有数据块和inode块与bitmap记录的不一致的问题。

**Inode** 检查有没有异常，比如标志位是不是有效，检查Inode的link count是不是正确，如果inode没有被任何目录指向，会放到lost+found文件夹；如果指向的块没有在有效范围，可能inode会被清除以保证一致性。

**Data block** 如果两个inode指向同一个块，会复制一份让两个inode各自拥有一份数据块；directory数据块会检查前两个是不是.和..目录，并且要保证每个inode没有在同一个目录被link两次。

#### 7.3 Journaling

借鉴了DBMS的write-ahead logging的方法来改进FS的一致性，将恢复时间由O(size-of-disk-volumn)降低到O(size-of-the-log)，ext3、ext4、XFS、JFS、NTFS等FS都用了这种方法。

可以分为两种：metadata journaling和full mode journaling。后者在更新磁盘区域时，会提前将所有新数据写到journal区域；而前者在FS journal区域只存储inode、bitmap等metadata，不存user data，因为节省bandwidth，更为常用。

##### 7.3.1 full mode journaling 

**大概需要三步：**

1. Journal write: 在journal区域以一个TxB(Transaction Begin)标志开始讲需要journal的data、metadata写入。
2. Journal commit: 在日志写好后写一个TxE(Transaction End)标志表示日志写结束了。
3. Checkpoint: Checkpoint过程就是真正更新磁盘的过程。
4. Free: 过一段时间后，需要更新journal的superblock，mark这次事务为free

如下图：

[[p3_009.png]]

**两个问题：**

1. 其中为了将a)和b)两次IO合成一次减少性能开销，可以在TxB和TxE中都写一下日志的校验和(checksum)，这样恢复的时候就可以根据TxB的checksum和已经存储的检验日志的完整性了，这个方法是被作者的团队提出的，现在被用于 **ext4** 中。
2. journal的区域是一定的，不能无限增长，所以采用了类似环形链表的数据结构存储log，只需要存储开始块和结束块的指针就可以了。

##### 7.3.2. metadata journaling 


**User Data 和 Journal的提交顺序：**

metadata journaling中，根据user data写盘的顺序，又可以分为ordered journaling和non-ordered journaling，前者保证先写user data到磁盘，再写metadata到日志，最后写metadata到磁盘；后者的区别不保证user data和metadata的顺序性，实际这不会造成什么问题。所以NTFS、XFS等FS都采用了non-ordered metadata journaling的方式保证一致性。

**大概分为五步**

1. Data write
2. Journal metadata write
3. Journal commit
4. Checkpoint metadata
5. Free

这里，只是将journal的内容减少了user data。在ordered mode中，data要先写完再开始下一步；在non-ordered mode中，data write和其他步顺序无关，异步进行。如图，complete顺序和具体运行有关：

[[p3_010.png]]

#### 7.4 其他方法

除了1)fsck、2)journaling，还可以用其他的方法保证一致性。比如3)Soft Update[1][2]，4)copy-on-write(COW)被用于ZFS，5)backpointer-based consistency(BBC)，等等。

---

[1] M. Dong and H. Chen, “Soft Updates Made Simple and Fast on Non-volatile Memory,” Atc, 2017.

[2] M. McKusick and G. Ganger, “Soft updates: a technique for eliminating most synchronous writes in the fast filesystem,” ATEC ’99 Proc. Annu. Conf. USENIX Annu. Tech. Conf., 1999.


## 第八节 LFS(log-structured filesystem)

What does “level of indirection” mean in David Wheeler's aphorism?
, https://stackoverflow.com/questions/18003544/what-does-level-of-indirection-mean-in-david-wheelers-aphorism

## 第九节 数据完整性和数据保护

## 第十~十二节 分布式系统简介、NFS和AFS

介绍了分布式系统很复杂，系统各部分的错误是无法消除的，需要使用各种手段保证系统正常运行。

分布式系统的问题包括性能、安全、通信等问题，本节主要谈通信问题。首先，通信本身就是不可靠的，在网络传输中，丢包不可避免。TCP能保证传输可靠性，但性能牺牲太大，UDP只提供了简单的checksum机制，需要分布式系统自己保证传输的可靠。比如，作者较详细地介绍了RPC(详见原文)，其一般为了保证性能，用UDP而不用TCP。

作者在下两节分别介绍了NFS和AFS两种分布式文件系统。

#### 10.1 Sun's Network File System(NFS)协议

NFS由SUN公司开发，并没有被实现为一种特定的系统，而是指定了一种开方的协议（open protocol）。现在最新为v4版，作者重点介绍NFSv2。

首先，NFSv2被实现为一种无状态协议(stateless protocol)，即每个客户端的单个操作都包含着完成请求所需的所有信息。其次，它应该兼容POSIX，来方便用户和应用使用。

NFSv2的关键概念是 **file handle** 。它包括3部分：volume identifier、inode number和generation number。volume ID用于指定请求的是哪个server，inode number指明了是哪个文件，而generation number用于重复使用一个inode number使对请求进行区分。协议如图：

[[p3_011.png]]


#### 10.2 The Andrew File System(AFS)协议

AFS用的不多了，其特色思路已经被最新的NFSv4引入，人们大多用NFS和CIFS等代替它。作者重点是讲其思路。AFS最初由CMU开发，版本1(ITC)和版本2之间有较大变革。

与NFS不同，AFS是以文件为单位进行下载和更新的，而NFS是以块为单位的。

AFSv1的协议如下：


[[p3_012.png]]


#### 10.3 NFS和AFS

两者性能对比表如下：

[[p3_013.png]]