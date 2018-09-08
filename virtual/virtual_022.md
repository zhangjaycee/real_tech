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



(to be continued ...)