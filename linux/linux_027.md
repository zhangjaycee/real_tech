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
```

### restore

从这堆文件中将进程恢复过来。

### Lazy Restore & Migration

---

[1] Lazy Migration in CRIU’s master branch, https://lisas.de/~adrian/?p=1287

[2] Userfaultfd, https://criu.org/Userfaultfd

[3] man page, https://github.com/checkpoint-restore/criu/blob/master/Documentation/criu.txt