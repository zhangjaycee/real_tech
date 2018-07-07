# 文件操作命令

## dd

## fallocate

fallocate是一个命令行命令，同样也是个Linux系统调用。

用作系统调用时，可以用来文件打洞：[man 2 fallocate]

```

   Deallocating file space
       Specifying  the  FALLOC_FL_PUNCH_HOLE  flag (available since Linux 2.6.38) in
       mode deallocates space (i.e., creates a hole) in the byte range  starting  at
       offset  and  continuing  for  len bytes.  Within the specified range, partial
       file system blocks are zeroed, and whole file system blocks are removed  from
       the  file.   After  a  successful call, subsequent reads from this range will
       return zeroes.

       The FALLOC_FL_PUNCH_HOLE flag must be ORed with FALLOC_FL_KEEP_SIZE in  mode;
       in other words, even when punching off the end of the file, the file size (as
       reported by stat(2)) does not change.

       Not all file systems support FALLOC_FL_PUNCH_HOLE; if a file  system  doesn't
       support  the  operation, an error is returned.  The operation is supported on
       at least the following filesystems:

       *  XFS (since Linux 2.6.38)

       *  ext4 (since Linux 3.0)

       *  Btrfs (since Linux 3.7)

       *  tmpfs (since Linux 3.5)

```