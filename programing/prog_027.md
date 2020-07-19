# GCC编译器参数


* __attribute__((packed))

用于将struct或者union中的对齐减到最小，减少内存占用，也减少传输带宽，（也能减少自动对齐带来的复杂性？）。

e.g.[1][2]
```c
struct
{
    char a;
    int b __attribute__((packed));
};
```

QEMU中也有类似定义[3]：
```c
#if defined(_WIN32) && (defined(__x86_64__) || defined(__i386__))
# define VU_PACKED __attribute__((gcc_struct, packed))
#else
# define VU_PACKED __attribute__((packed))
#endif
...
typedef struct VhostUserMsg {
    int request;

#define VHOST_USER_VERSION_MASK     (0x3)
#define VHOST_USER_REPLY_MASK       (0x1 << 2)
#define VHOST_USER_NEED_REPLY_MASK  (0x1 << 3)
    uint32_t flags;
    uint32_t size; /* the following payload size */

    union {
#define VHOST_USER_VRING_IDX_MASK   (0xff)
#define VHOST_USER_VRING_NOFD_MASK  (0x1 << 8)
        uint64_t u64;
        struct vhost_vring_state state;
        struct vhost_vring_addr addr;
        VhostUserMemory memory;
        VhostUserMemRegMsg memreg;
        VhostUserLog log;
        VhostUserConfig config;
        VhostUserVringArea area;
        VhostUserInflight inflight;
    } payload;

    int fds[VHOST_MEMORY_BASELINE_NREGIONS];
    int fd_num;
    uint8_t *data;
} VU_PACKED VhostUserMsg;
```



---
[1] https://gcc.gnu.org/onlinedocs/gcc-4.0.2/gcc/Type-Attributes.html
[2] http://blog.chinaunix.net/uid-25768133-id-3485479.html
[3] https://github.com/qemu/qemu/blob/master/contrib/libvhost-user/libvhost-user.h