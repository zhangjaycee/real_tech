## qemu-img 文档翻译



(翻译自qemu 3.0的文档)



```
qemu-img [standard options] command [command options]
```

qemu-img 允许你离线地创建、转换或者修改镜像文件。它可以处理所有QEMU支持的镜像格式。

**注意：** 千万不要用 qemu-img 修改虚拟机(或者其他程序)正使用着的镜像，因为那可能会破坏镜像；对应的，如果读正在修改的镜像，也可能会有不一致的状态产生。

### 1. Standard options：

- ‘-h, --help’

  显示帮助信息。

- ‘-V, --version’

  显示版本信息。

- ‘-T, --trace [[enable=]pattern][,events=file][,file=file]’

  Specify tracing options.

  指定tracing选项：

  - ‘[enable=]pattern’

    以parttern来指定启动的events。这个选项仅在编译了simple、log或ftrace等3个tracing后端时才能用。要启用多个events或者patterns，用多个`-trace`即可，用`-trace help`可以打印列出trace points名称。

  

  - ‘events=file’

    Immediately enable events listed in file. The file must contain one event name (as listed in the ‘`trace-events-all`’ file) per line; globbing patterns are accepted too. This option is only available if QEMU has been compiled with the simple, log or ftrace tracing backend.

    马上开启file中列出了的events名称，file中每行为一项event名称或者patterns (存在于`trace-events-all`文件中的)。同样，这个选项仅在编译了simple、log或ftrace等3个tracing后端时才能用。

  

  - ‘file=file’

    Log output traces to file. This option is only available if QEMU has been compiled with the simple tracing backend.

    将traces的输出打印到log文件中。同样，这个选项仅在编译了simple、log或ftrace等3个tracing后端时才能用。

  

### 2. Command:

以下是被支持的命令：

```
amend [--object objectdef] [--image-opts] [-p] [-q] [-f fmt] [-t cache] -o options filename
bench [-c count] [-d depth] [-f fmt] [--flush-interval=flush_interval] [-n] [--no-drain] [-o offset] [--pattern=pattern] [-q] [-s buffer_size] [-S step_size] [-t cache] [-w] [-U] filename
check [--object objectdef] [--image-opts] [-q] [-f fmt] [--output=ofmt] [-r [leaks | all]] [-T src_cache] [-U] filename
commit [--object objectdef] [--image-opts] [-q] [-f fmt] [-t cache] [-b base] [-d] [-p] filename
compare [--object objectdef] [--image-opts] [-f fmt] [-F fmt] [-T src_cache] [-p] [-q] [-s] [-U] filename1 filename2
convert [--object objectdef] [--image-opts] [--target-image-opts] [-U] [-c] [-p] [-q] [-n] [-f fmt] [-t cache] [-T src_cache] [-O output_fmt] [-B backing_file] [-o options] [-l snapshot_param] [-S sparse_size] [-m num_coroutines] [-W] filename [filename2 [...]] output_filename
create [--object objectdef] [-q] [-f fmt] [-b backing_file] [-F backing_fmt] [-u] [-o options] filename [size]
dd [--image-opts] [-U] [-f fmt] [-O output_fmt] [bs=block_size] [count=blocks] [skip=blocks] if=input of=output
info [--object objectdef] [--image-opts] [-f fmt] [--output=ofmt] [--backing-chain] [-U] filename
map [--object objectdef] [--image-opts] [-f fmt] [--output=ofmt] [-U] filename
measure [--output=ofmt] [-O output_fmt] [-o options] [--size N | [--object objectdef] [--image-opts] [-f fmt] [-l snapshot_param] filename]
snapshot [--object objectdef] [--image-opts] [-U] [-q] [-l | -a snapshot | -c snapshot | -d snapshot] filename
rebase [--object objectdef] [--image-opts] [-U] [-q] [-f fmt] [-t cache] [-T src_cache] [-p] [-u] -b backing_file [-F backing_fmt] filename
resize [--object objectdef] [--image-opts] [-f fmt] [--preallocation=prealloc] [-q] [--shrink] filename [+ | -]size

```



 #### 2.1 Command的参数

以下为Command的参数的一般含义：

。。。



#### 2.2 Command的具体描述

* amend

* ```
  amend [--object objectdef] [--image-opts] [-p] [-p] [-f fmt] [-t cache] -o options filename
  ```

  Amends the image format specific options for the image file filename. Not all file formats support this operation.

  修改某些格式的特定参数，并非所有格式都支持。

* bench

  ```
  bench [-c count] [-d depth] [-f fmt] [--flush-interval=flush_interval] [-n] [--no-drain] [-o offset] [--pattern=pattern] [-q] [-s buffer_size] [-S step_size] [-t cache] [-w] [-U] filename
  ```

  在镜像上跑一个简单的顺序I/O基准测试，如果指定了`-w`，则进行写测试，如果没有`-w`，则进行读测试。

  一共将进行`count`个I/O请求，每个大小是`buffer_size`，并行IO的队列深度是`depth`。第一个请求将从`offset`这个偏移量开始，每次请求的位置会增加`step_size`(如果`step_size`没有指定，那么将用`buffer_size`的值代替)、

  If flush_interval is specified for a write test, the request queue is drained and a flush is issued before new writes are made whenever the number of remaining requests is a multiple of flush_interval. If additionally `--no-drain` is specified, a flush is issued without draining the request queue first.

  如果`flush_interval`在一个写测试中被指定，那么每次queue中剩余的请求数为`flush_interval`的整数倍时，都会暂停新情求，将现存请求flush掉。如果指定了额外的`--no-drain`参数，则在flush后不等待所有请求flush完成。

  如果`-n`被指定，那么native AIO后端将优先被使用(如果支持的话)，并且在Linux中，只有`-t none`和`-t directsync`被同时指定时，`-n`参数才有效。

  

* check

  ```
  check [--object objectdef] [--image-opts] [-q] [-f fmt] [--output=ofmt] [-r [leaks | all]] [-T src_cache] [-U] filename
  ```

  对镜像进行一次consistency检查，结果将被用ofmt(human或者json)格式被输出。

  如果指定了`-r`，那么`qemu-img`会尝试修复所有不一致的地方：`-r leaks`只修复cluster的leak；`-r`将会修复所有错误，但却有很大错误修复或者隐藏已经发生的错误的风险。

​	只有qcow2、qed和vdi支持consistency检查。

​	当image没有任何不一致时，check以0退出码退出，其他退出码表示其他不一致或者错误的情况发生：

|  0   | 没有不一致                                      |
| :--: | :---------------------------------------------- |
|  1   | 由于内部错误而未检查完                          |
|  2   | 检查完了，镜像出错了                            |
|  3   | 检查完了，镜像的cluster有leak现象，但是并未出错 |
|  63  | 镜像格式不支持检查一致性                        |

​	如果`-r`被指定，退出码表示修复劶镜像的状态，就是说，被正确修复的不一致镜像也会返回0。

* commit

  ```
  commit [--object objectdef] [--image-opts] [-q] [-f fmt] [-t cache] [-b base] [-d] [-p] filename
  ```

  commit文件中记录的更改到基础镜像(base image)或者后端文件(backing file)中，如果backing file比			snapshot小，那么backing file会被增加到和snapshot一样大；如果snapshot 比backing file 小，backing file也	并不会被截短。如果你想backing file和比较小的snapshot匹配，当commit成功后你可以安全地手动将其截短。		

  commit成功后上层的top image镜像将被清理，如果你commit后再也不想用它了，可以指定`-d`跳过清空文件的过程。

  如果给定的镜像文件的baking chain大于一层，那么到底commit到哪个backing file可以用`-b base`来指定(必须是backing chain中的一个)。如果`base`未被指定，top image的直接(相邻？)backing file将会被默认指定。注意，commit后，base和top image之间的所有文件将是无效的，读它们也只会读到垃圾数据，所以`-b`也就意味着`-d`(这样top image就会保持有效了)。

* compare

  ```
  compare [--object objectdef] [--image-opts] [-f fmt] [-F fmt] [-T src_cache] [-p] [-q] [-s] [-U] filename1 filename2
  ```

  检查两个镜像文件是否内容相同，支持比较两个不同格式、不同设置的镜像文件。

  默认情况下，若一个镜像比另一个大，但是大的部分都是未分配或者都是零，那么这两个镜像也是被认为相同的。另外，若一个扇区在某个镜像未被分配，并且另一个镜像的对应扇区全是零，那么两者也是相同的。用`-s`开启Strict模式，则在镜像大小不同则镜像不同，

  默认情况下，compare命令会打印出结果信息，告诉我们两个镜像相同或者发生不同的第一个位置，如果用Strict模式，还会报告出相差的大小。

  若两者相同，compare会以0退出，不同会以1退出，还有其他错误码：

  |  0   | 镜像相同         |
  | :--: | :--------------- |
  |  1   | 镜像不同         |
  |  2   | 打开镜像出错     |
  |  3   | 检查扇区分配出错 |
  |  63  | 读数据出错       |

* convert

  ```
  convert [--object objectdef] [--image-opts] [--target-image-opts] [-U] [-C] [-c] [-p] [-q] [-n] [-f fmt] [-t cache] [-T src_cache] [-O output_fmt] [-B backing_file] [-o options] [-l snapshot_param] [-S sparse_size] [-m num_coroutines] [-W] filename [filename2 [...]] output_filename
  ```

  将镜像(*filename*)或者快照(*snapshot_param*)转换为*output_fmt*格式的*output_filename*文件。还可以加`-c`开启压缩选项，或者用加密等某些镜像特别支持的功能(-o option)。

  只有qcow和qcow2支持压缩。压缩是只读的，即如果被压缩的sector被覆盖写时，会转为未压缩的形式。

  镜像的转换还可以用于缩小qcow等增长型镜像的文件大小，空扇区会被检测出来并被除去。(可以参考https://pve.proxmox.com/wiki/Shrink_Qcow2_Disk_Files)

  *sparse_size* 指示转换时创建一个“sparse image”最小的连贯的字节数(默认为4K)。如果*sparse_size* 值为0，那么将不会检测源文件的未分配和全零的扇区，目标文件的对应空间也会被全部分配。

  你可以使用 `-B` *backing_file* 选项来强制输出镜像(*output_filename*)被创建为 *backing_file* 的写前拷贝(copy on write)镜像，这个 *backing_file* 应该和输入镜像 (*filename*) 的基础镜像(base image)内容相同(路径、镜像格式等可以不同)。如果 *backing file* 指定的是相对路径，它相对的是包含 *output_filename* 的路径。

  如果指定了`-n`，那么目标卷的创建会被跳过，这对rbd等格式很有用，因为目标卷可能已经被用site scpecific选项创建好，这可能也是qemu-img所不支持的。

  乱序写可以用`-W`指定来提升性能，这仅仅在host device或者其他raw 块设备等预先创建的设备上推荐使用。乱序写功能在创建压缩镜像格式时不能用。

  *num_coroutines* 指定了一个进程中一共有多少个协程同时工作。(默认为8)

* create

  ```
  create [--object objectdef] [-q] [-f fmt] [-b backing_file] [-F backing_fmt] [-u] [-o options] filename [size]
  
  
  
  The size can also be specified using the size option with -o, it doesn’t need to be specified separately in this case.
  ```

  创建一个 *fmt* 格式的大小为 *size* 的新镜像，针对于镜像的具体格式，还可以指定更多的选项。

  如果`-b` *backing_file* 被指定，那么新镜像只会记录与 *backing_file* 所不同的内容，这种情况下也不用指定 *size* 。*backing_file* 永远不会被更改，除非你用`commit`这个monitor command或者你用qemu-img的`commit`命令。如果 *backing_file* 是一个相对路径，相对的是包含 *filename* 的路径。

  注意，指定的 *backing file* 会被打开检查是否是有效的。用`-u`选项可以指定不安全模式，这意味着即使 *backing_file* 打不开，新的进行也会被创建。为了用这种方式创建一个镜像，合适的backing file应该被创建，额外的选项也应该被指定。

  大小也可以被用`-o`选项指定，这就不需要分离地指定了(？？)。

  

* dd

  ```
  dd [--image-opts] [-U] [-f fmt] [-O output_fmt] [bs=block_size] [count=blocks] [skip=blocks] if=input of=output
  ```

  dd命令会从输入文件复制到输出文件的同时将 *fmt* 转换到 *output_fmt*。数据默认以512字节为单位读写，但是可以用 *block_size* 进行指定。如果`count=blocks`被指定，dd会在从输入读 *blocks* 个块后停止读取。 这个命令指定大小的格式类似dd(1)命令。

  

*  info

  ```
  info [--object objectdef] [--image-opts] [-f fmt] [--output=ofmt] [--backing-chain] [-U] filename
  Give information about the disk image filename. Use it in particular to know the size reserved on disk which can be different from the displayed size. If VM snapshots are stored in the disk image, they are displayed too. The command can output in the format ofmt which is either human or json.
  
  If a disk image has a backing file chain, information about each disk image in the chain can be recursively enumerated by using the option --backing-chain.
  
  For instance, if you have an image chain like:
  
  base.qcow2 <- snap1.qcow2 <- snap2.qcow2
  To enumerate information about each disk image in the above chain, starting from top to base, do:
  
  qemu-img info --backing-chain snap2.qcow2
  ```

  info会给出指定镜像文件的信息。它给出的大小信息可能和磁盘上所占用的大小不相等。如果VM的快照被存在镜像中也会被列出。这个指令会用json或者human的ofmt格式打印出信息。

  如果镜像存在一个backing file链，用`--backing-chain`选项可以递归地打印出链上所有镜像的信息。

  比如如果你的镜像链是这样：`base.qcow2 <- snap1.qcow2 <- snap2.qcow2`。那么为了打印出上述每个镜像的信息，命令应该这样写：`qemu-img info --backing-chain snap2.qcow2`。

* map

  ```
  map [-f fmt] [--output=ofmt] filename
  ```

  map命令会dump一个镜像的metadata和它的backing file chain。这个命令还会dump每个扇区的allocation状态，包含是在backing file chain中的哪个最外层(topmost)文件分配了这个扇区。

  有两个输出格式选项可以被指定：默认的`fmt`(human)只dump文件中已知非零的区域，已知为零的部分和整个链中未被分配的部分将被省略。qemu-img输出将标记一个文件开始可读的偏移量。每行有4个字段，例如：

  ```
  Offset          Length          Mapped to       File
  0               0x20000         0x50000         /tmp/overlay.qcow2
  0x100000        0x10000         0x95380000      /tmp/backing.qcow2
  ```

  这表示从偏移量0开始的0x20000 (131072)个字节(虚拟偏移)，在`/tmp/overlay.qcow2`文件中(以raw格式打开)的偏移量0x50000 (327680)找到(文件物理偏移)。如果数据是压缩、加密或者其他无法用raw格式读的，在human格式下会导致出错。注意文件名可能换行，这对脚本解析处理不安全。

  另一种json格式会以JSON字典形式格式输出。它除了包含和human格式相似的信息，还会包含一些细节信息：

  *  一个扇区是否包含实际数据(布尔型字段数据，如果是false，说明扇区未被分配或者被存储为优化后的全零clusters)
  * 是否已知数据被读为0(布尔字段为0)
  * 为了让输出更短，targe file被表达成链深度，比如深度为2表示backing file 的backing file的文件名。
  * JSON格式中，offset字段是可选的，它在human格式会省略或者错误退出时被省略。如果data是false的但offset出现，说明文件中对应的扇区没有被使用，但是被预分配了。

  要了解更多信息，可以去看QEMU代码中看`include/block/block.h`文件。

(to be continued ...)

* measure

  ```
  measure [--output=ofmt] [-O output_fmt] [-o options] [--size N | [--object objectdef] [--image-opts] [-f fmt] [-l snapshot_param] filename]
  ```

  计算一个新的镜像所需要的文件大小，信息可以被用来估算放进的一个一定容量的镜像所需要的逻辑卷或者SAN LUN的空间。估算得出的值肯定是够大的，这个命令也可以用human或者json这两个ofmt输出。

  如果大小 *N* 被给出，那么就会像`create`命令一样估算。如果 `filename` 被指定，那么就像`convert`命令一样来估算某个镜像转换后的大小，转换后的格式用 *output_fmt* 指定，当前存在的文件的格式用 *fmt* 指定。

  一个镜像中的快照可以用*snapshot_param*参数指定。

  例如以下字段将被打印：

  ```
  required size: 524288
  fully allocated size: 1074069504
  ```

  "required size"是新镜像的大小，如果镜像格式支持compact表示，它可能比磁盘的虚拟大小更小。”fully allocated size“是新镜像被写满整个sector后的大小，这是这个文件除了额外的内部快照、脏位图、vmstate数据和其他高级镜像格式特性外，最大可能占据的空间。

* snapshot

  ```
  snapshot [--object objectdef] [--image-opts] [-U] [-q] [-l | -a snapshot | -c snapshot | -d snapshot] filename
  ```

  列出、应用、创建或者删除一个镜像的快照。

* rebase

  ```
  rebase [--object objectdef] [--image-opts] [-U] [-q] [-f fmt] [-t cache] [-T src_cache] [-p] [-u] -b backing_file [-F backing_fmt] filename
  ```

  rebase可以改变镜像的backing file，只有qcow2和qed支持改变backing file。

  backing file会被改为 *backing_file* ，backing file 的格式也会被换为 *backing_fmt* (如果支持的话)。如果*backing_file* 被指定为空字符串("")，那么镜像会被rebased到没有backing file，即和任何backing file独立。如果*backing_file*指定的是相对路径，相对的是 *filename* 所在的路径。

  *cache*和*src_cache*分别指定了*filename*和*backing_file所用的cache模式。

  rebase有两种不同的模式：

  * safe模式 (默认)

    进行真正的rebase操作，新的backing file可能会和旧的不同，qemu-img rebase会让guest看到的内容不发生改变。

    具体的， 新的*backing_file*和旧的backing file不同的clusters都会被merged到 *filename* 中。

    注意，安全模式rebase是一个很昂贵的操作，其成本可以和转换一个格式相比较，它只有在旧的backing file存在时才可以工作。

  *  unsafe模式

    指定参数`-u`便使用了unsafe 模式，这种模式下backing file 会被直接替换掉而不对内容进行任何检查。用户必须指定正确的backing file，否则guest所看到的image就会被破坏。

    这种模式对重命名或者移动backing file到其他地方很有用。它可以不用访问旧的backing file，也就是说，你可以用它来修复一个backing file被重命名或者挪了地方的镜像。

  你可以用rebase命令来进行对两个镜像进行一次”diff“操作，当你拷贝或者克隆一个guest时，或者你想回到一个template 或者base image的thin image上时，这很有用。比如说，`base.img`被拷贝(克隆)为`modified.img`后被运行过了，所以两者之间存在一些不同，你可以用以下命令重建一个thin image `diff.qcow2`，它包含有两者的不同之处。

  ```
  qemu-img create -f qcow2 -b modified.img diff.qcow2
  qemu-img rebase -b base.img diff.qcow2
  ```

  在这之后，`modified.img`就可以被丢弃了，因为`base.img` + `diff.qcow2`包含了相同的信息。

* resize

  ```
  resize [--object objectdef] [--image-opts] [-f fmt] [--preallocation=prealloc] [-q] [--shrink] filename [+ | -]size
  ```

  resize可以改变磁盘镜像，就像它用 *size*被创建一样。

  用这个命令缩减磁盘镜像大小前，你一定要在Guest中用文件系统或者分区工具相应地减小文件系统或者分区的大小，否则数据很可能丢失！

  当缩减镜像时，`--shrink`选项必须制定。这告诉qemu-img用户已经知晓所有截断之后的数据将被丢弃。

  当用这个命令增加镜像大小时，你必须用guest中的文件系统工具或者分区工具来真正把新加的空间用起来。

  当增大镜像时，`--preallocation`选项可以被用来制定增加的区域怎么被host分配。那些值可用可以具体看NOTES中对format的描述。用这个选项可能导致轻微的数据的过量分配。

  