# 虚拟机镜像格式和性能

## 1. QEMU的raw格式

## 2. QEMU的qcow2格式

* 压缩功能

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