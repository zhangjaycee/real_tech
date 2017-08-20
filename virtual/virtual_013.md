# 虚拟机镜像格式和性能raw/qcow2

### qcow2格式的压缩功能
>https://qemu.weilnetz.de/doc/qemu-doc.html
>
> Only the formats qcow and qcow2 support compression. The compression is read-only. It means that if a compressed sector is rewritten, then it is rewritten as uncompressed data.
>


> https://www.jamescoyle.net/how-to/1810-qcow2-disk-images-and-performance
>
> qcow2 is, at best, a bit weird when it comes to compression (encryption works the same way, too!) in that compression is a one time event, or process that you run to compress an existing image. Any data written after this will be stored uncompressed.
>
> The next thing is to understand compression itself – compression (under the right circumstances) will reduce the size of the data stored on disk at the expense of CPU to compress (one off) and decompress (every time the data is accessed) the data. In certain circumstances, compression can result in a quicker read for the process consuming the data, such as where CPU is abundant and IO bandwidth is very small.
>
>

qcow2 支持基于zlib的压缩功能，但是只是一次性行为，再次被写时将是不压缩的版本。（怎么感觉像骗人一样。。。）

其主要应用于用qemu-img工具缩减镜像体积：

```bash
# 摘自http://www.tuxfixer.com/how-to-shrink-openstack-qcow2-image-with-qemu-img/
# Shrink qcow2 image without compression (larger file, short compression time):
qemu-img convert -O qcow2 centos7.qcow2 centos7_small.qcow2
# Shrink qcow2 image with compression (smaller file, long compression time):
qemu-img convert -O qcow2 -c centos7.qcow2 centos7_small.qcow2
```


## qemu镜像扩容方法

对于qcow2格式，可以直接用qemu-img命令扩容，例：
```
qemu-img resize data.qcow2 +10G
```
> [KVM guest磁盘扩容] http://www.topjishu.com/10131.html