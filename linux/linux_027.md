# Checkpoint&Restore in Userspace (CRIU)

### dump

将某个进程（树）相关的所有数据都dump到一堆文件中。

与dump有关的文件操作：

```cpp
// CRIU_SRC_PATH/criu/cr-dump.c
 int cr_dump_tasks(pid_t pid)
          while(...) {
                  dump_one_task(item);
          }

 static int dump_one_task(struct pstree_item *item)
          struct parasite_drain_fd *dfds = NULL;
          dfds = xmalloc(sizeof(*dfds));
          ret = collect_fds(pid, &dfds);
          ret = dump_task_files_seized(parasite_ctl, item, dfds);


// CRIU_SRC_PATH/criu/files.c
int dump_task_files_seized(struct parasite_ctl *ctl, struct pstree_item *item, struct parasite_drain_fd *dfds)
          while(...) {
             ret = dump_one_file(item->pid, dfds->fds[i + off],lfds[i], opts + i, ctl, &e);
          }

static int dump_one_file(struct pid *pid, int fd, int lfd, struct fd_opts *opts, struct parasite_ctl *ctl, FdinfoEntry *e)
         dump_socket(&p, lfd, e);  -+
         dump_chrdev(&p, lfd, e);   +-->   do_dump_gen_file();  --->  dump_one_reg_file();
           ...                      |
           ...                     -+


// CRIU_SRC_PATH/criu/files-reg.c
int dump_one_reg_file(int lfd, u32 id, const struct fd_parms *p)
        return pb_write_one(rimg, &fe, PB_FILE);
        

// CRIU_SRC_PATH/criu/protobuf.c
/*
 * Writes PB record (header + packed object pointed by @obj)
 * to file @fd, using @getpksize to get packed size and @pack
 * to implement packing
 *
 *  0 on success
 * -1 on error
 */
int pb_write_one(struct cr_img *img, void *obj, int type)
       ret = bwritev(&img->_x, iov, 2);


// CRIU_SRC_PATH/criu/bfd.c
int bwritev(struct bfd *bfd, const struct iovec *iov, int cnt)
       return writev(bfd->fd, iov, cnt);

```

一些相关的函数指针注册结构和宏定义结构，读代码时可能会用到。

```cpp
// criu/files-reg.c
#define FD_PARMS_INIT           \
(struct fd_parms) {         \
    .fd = FD_DESC_INVALID,  \
    .fown   = FOWN_ENTRY__INIT, \
    .link   = NULL,         \
    .mnt_id = -1,           \
}

// criu/include/files.h
const struct fdtype_ops regfile_dump_ops = {
    .type       = FD_TYPES__REG,
    .dump       = dump_one_reg_file,
};

// criu/image-desc.c
// 不同类型image文件的文件名和文件打开标志位的定义
struct cr_fd_desc_tmpl imgset_template[CR_FD_MAX] = {
    FD_ENTRY(INVENTORY, "inventory"),
    FD_ENTRY(FDINFO,    "fdinfo-%u"),
    FD_ENTRY(PAGEMAP,   "pagemap-%lu"),
       ...
}
```

### restore

从这堆文件中将进程恢复过来。从打印的日志文件，可以分析出最耗时的读文件过程在`CRIU_SRCS/criu/pie/restorer.c`:


```cpp
/*
 * The main routine to restore task via sigreturn.
 * This one is very special, we never return there
 * but use sigreturn facility to restore core registers
 * and jump execution to some predefined ip read from
 * core file.
 */
long __export_restore_task(struct task_restore_args *args)
{
    ...
      
    rio = args->vma_ios;
    for (i = 0; i < args->vma_ios_n; i++) {
        struct iovec *iovs = rio->iovs;
        int nr = rio->nr_iovs;
        ssize_t r;

        while (nr) {
            pr_debug("Preadv %lx:%d... (%d iovs)\n",
                    (unsigned long)iovs->iov_base,
                    (int)iovs->iov_len, nr);
            r = sys_preadv(args->vma_ios_fd, iovs, nr, rio->off);
            if (r < 0) {
                pr_err("Can't read pages data (%d)\n", (int)r);
                goto core_restore_end;
            }

            pr_debug("`- returned %ld\n", (long)r);
            rio->off += r;
            /* Advance the iovecs */
            do {
                if (iovs->iov_len <= r) {
                    pr_debug("   `- skip pagemap\n");
                    r -= iovs->iov_len;
                    iovs++;
                    nr--;
                    continue;
                }

                iovs->iov_base += r;
                iovs->iov_len -= r;
                break;
            } while (nr > 0);
        }

        rio = ((void *)rio) + RIO_SIZE(rio->nr_iovs);
    }

    sys_close(args->vma_ios_fd);
    
    ...
}
```

### Lazy Restore & Migration

主要用到了userfaultfd[2]，关于Userfaultfd，详见本wiki另一个wiki页：[Page fault](https://github.com/zhangjaycee/real_tech/wiki/linux_031)。



### log 

CRIU以`pr_debug()`函数打印日志，的log相关数据结构定义在`SRC_PATH/criu/log.c`。每次打印日志，都会打印时间戳，可以观察耗时情况。

```cpp
static void timediff(struct timeval *from, struct timeval *to)
{
    to->tv_sec -= from->tv_sec;
    if (to->tv_usec >= from->tv_usec)
        to->tv_usec -= from->tv_usec;
    else {
        to->tv_sec--;
        to->tv_usec += 1000000 - from->tv_usec;
    }
}
...
```
---

[1] Lazy Migration in CRIU’s master branch, https://lisas.de/~adrian/?p=1287

[2] Userfaultfd, https://criu.org/Userfaultfd

[3] man page, https://github.com/checkpoint-restore/criu/blob/master/Documentation/criu.txt

[4] CRIU wiki - Copy-on-write memory, https://criu.org/Copy-on-write_memory 