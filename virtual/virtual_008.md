# 关于virtio


(以下内容2019年前更新，以下资料仅供参考。wiki中的 [[Qemu进行读/写的流程|virtual_009]] 中有一些更新的分析。)

---

> 
1. [概述](#概述)
2. [前端驱动分析](#前端驱动分析linux-kernel)
3. [后端设备分析](#后端设备分析qemu)
3. [virtio-blk和multiqueue](#virtio-bllk和multiqueue)
4. [相关资料](#相关资料)


### 概述

对于qemu/kvm虚拟机来说，用不用virtio，决定了我们的虚拟化是半虚拟化还是全虚拟化。

决定虚拟机是半虚拟还是全虚拟的性质转变的标准只有一个：Guest机知不知道自己是一个虚拟机。具体来说，不使用virtio，虚拟机会像在真实物理环境下运行一样地运行——它不认为它是虚拟机；而使用virtio，就是让两部分virtio程序的互相通信，这两部分程序分别是前端驱动(frontend, Guest中)和后端设备(backend, Host中)，这样因为Guest中有了virtio的frontend部分，所以它的运行和物理机环境下有了区别，Guest按照一个使用virtio的虚拟机的方式运行——它知道了它是一个虚拟机。

virtio提高了io效率，（？也为host和guest间更复杂的合作机制实现提供了便利）



### 前端驱动分析（Linux Kernel）

[1] virtio-blk浅析, http://www.2cto.com/os/201408/329744.html

[2] Virtio：针对 Linux 的 I/O 虚拟化框架, https://www.ibm.com/developerworks/cn/linux/l-virtio/

[3] Virtio 原理与Guest OS driver, http://blog.csdn.net/wanthelping/article/details/47069429

[4] virtio-blk请求发起, http://blog.csdn.net/LPSTC123/article/details/44983707

[5] The multiqueue block layer, https://lwn.net/Articles/552904/

[6] Linux Multi-Queue Block IO Queueing Mechanism (blk-mq),(https://www.thomas-krenn.com/en/wiki/Linux_Multi-Queue_Block_IO_Queueing_Mechanism_(blk-mq)

[7] KVM+QEMU世界中的pci总线与virtio总线, http://blog.chinaunix.net/uid-23769728-id-4467752.html

[8] virtio前端驱动详解, http://www.cnblogs.com/ck1020/p/6044134.html



前端驱动已经并到Linux内核主线了，所以要去内核找相关代码分析。

* linux 内核与virtio、virtio-blk相关的文件与目录结构：

```

include/uapi/linux
	├── virtio_blk.h
	└── virtio_ring.h

include/linux
	├── virtio.h
	├── virtio_byteorder.h
	├── virtio_caif.h
	├── virtio_config.h
	├── virtio_console.h
	├── virtio_mmio.h
	└── virtio_ring.h

drivers/block/virtio_blk.c

drivers/virtio/
	├── Kconfig
	├── Makefile
	├── config.c
	├── virtio.c
	├── virtio_balloon.c
	├── virtio_input.c
	├── virtio_mmio.c
	├── virtio_pci_common.c
	├── virtio_pci_common.h
	├── virtio_pci_legacy.c
	├── virtio_pci_modern.c
	└── virtio_ring.c

drivers/vhost/
	├── Kconfig
	├── Makefile
	├── net.c
	├── scsi.c
	├── test.c
	├── test.h
	├── vhost.c
	├── vhost.h
	└── vringh.c

```

* 部分相关的重要数据结构

```
drivers/virtio/virtio_ring.c                                        drivers/block/virtio_blk.c                                          include/linux/virtio.h                                       include/linux/virtio_config.h                                    include/linux/device.h

 +---------------------------------------------------------------+    +--------------------------------------------------------------+    +-------------------------------------------+                 +-----------------------------------------------------------+      +----------------------------------------------------------------------+
 |                                                               |    |   struct virtio_blk {                                        |    |  struct virtqueue {                       |                 |                                                           |      |  struct device {                                                     |
 |  struct vring_virtqueue {                                     |    |    struct virtio_device *vdev;                               |    |   struct list_head list;                  |                 |                                                           |      |   struct device  *parent;                                            |
 |   struct virtqueue vq;                                        |    |                                                              |    |   void (*callback)(struct virtqueue *vq); |                 | struct virtio_config_ops {                                |      |                                                                      |
 |                                                               |    |    /* The disk structure for the kernel. */                  |    |   const char *name;                       |                 |  void (*get)(struct virtio_device *vdev, unsigned offset, |      |   struct device_private *p;                                          |
 |   /* Actual memory layout for this queue */                   |    |    struct gendisk *disk;                                     |    |   struct virtio_device *vdev;             |                 |       void *buf, unsigned len);                           |      |                                                                      |
 |   struct vring vring;                                         |    |                                                              |    |   unsigned int index;                     |                 |  void (*set)(struct virtio_device *vdev, unsigned offset, |      |   struct kobject kobj;                                               |
 |                                                               |    |    /* Block layer tags. */                                   |    |   unsigned int num_free;                  |                 |       const void *buf, unsigned len);                     |      |   const char  *init_name; /* initial name of the device */           |
 |   /* Can we use weak barriers? */                             |    |    struct blk_mq_tag_set tag_set;                            |    |   void *priv;                             |                 |  u32 (*generation)(struct virtio_device *vdev);           |      |   const struct device_type *type;                                    |
 |   bool weak_barriers;                                         |    |                                                              |    |  };                                       |                 |  u8 (*get_status)(struct virtio_device *vdev);            |      |                                                                      |
 |                                                               |    |    /* Process context for config space updates */            |    |                                           |                 |  void (*set_status)(struct virtio_device *vdev, u8 status)|      |   struct mutex  mutex; /* mutex to synchronize calls to              |
 |   /* Other side has made a mess, don't try any more. */       |    |    struct work_struct config_work;                           |    +-------------------------------------------+                 |  void (*reset)(struct virtio_device *vdev);               |      |        * its driver.                                                 |
 |   bool broken;                                                |    |                                                              |                                                                  |  int (*find_vqs)(struct virtio_device *, unsigned nvqs,   |      |        */                                                            |
 |                                                               |    |    /* What host tells us, plus 2 for header & tailer. */     |    +---------------------------------------------------+         |    struct virtqueue *vqs[],                               |      |                                                                      |
 |   /* Host supports indirect buffers */                        |    |    unsigned int sg_elems;                                    |    |                                                   |         |    vq_callback_t *callbacks[],                            |      |   struct bus_type *bus;  /* type of bus device is on */              |
 |   bool indirect;                                              |    |                                                              |    |  struct virtio_device {                           |         |    const char *names[]);                                  |      |   struct device_driver *driver; /* which driver has allocated this   |
 |                                                               |    |    /* Ida index + used to track minor number allocations. */ |    |   int index;                                      |         |  void (*del_vqs)(struct virtio_device *);                 |      |          device */                                                   |
 |   /* Host publishes avail event idx */                        |    |    int index;                                                |    |   bool failed;                                    |         |  u64 (*get_features)(struct virtio_device *vdev);         |      |   void  *platform_data; /* Platform specific data, device            |
 |   bool event;                                                 |    |                                                              |    |   bool config_enabled;                            |         |  int (*finalize_features)(struct virtio_device *vdev);    |      |          core doesn't touch it */                                    |
 |                                                               |    |    /* num of vqs */                                          |    |   bool config_change_pending;                     |         |  const char *(*bus_name)(struct virtio_device *vdev);     |      |   void  *driver_data; /* Driver data, set and get with               |
 |   /* Head of free buffer list. */                             |    |    int num_vqs;                                              |    |   spinlock_t config_lock;                         |         |  int (*set_vq_affinity)(struct virtqueue *vq, int cpu);   |      |          dev_set/get_drvdata */                                      |
 |   unsigned int free_head;                                     |    |    struct virtio_blk_vq *vqs;                                |    |   struct device dev;                              |         | };                                                        |      |   struct dev_pm_info power;                                          |
 |   /* Number we've added since last sync. */                   |    |   };                                                         |    |   struct virtio_device_id id;                     |         |                                                           |      |   struct dev_pm_domain *pm_domain;                                   |
 |   unsigned int num_added;                                     |    |                                                              |    |   const struct virtio_config_ops *config;         |         |                                                           |      |                                                                      |
 |                                                               |    +--------------------------------------------------------------+    |   const struct vringh_config_ops *vringh_config;  |         +-----------------------------------------------------------+      |   ...                                                                |
 |   /* Last used index we've seen. */                           |                                                                        |   struct list_head vqs;                           |                                                                            |                                                                      |
 |   u16 last_used_idx;                                          |  include/uapi/linux/virtio_ring.h    +---------------------+           |   u64 features;                                   |                                                                            |   /* arch specific additions */                                      |
 |                                                               |     +----------------------------+   |struct vring_avail { |           |   void *priv;                                     |                                                                            |   struct dev_archdata archdata;                                      |
 |   /* Last written value to avail+>flags */                    |     | struct vring {             |   | __virtio16 flags;   |           |  };                                               |                                                                            |                                                                      |
 |   u16 avail_flags_shadow;                                     |     |  unsigned int num;         |   | __virtio16 idx;     |           |                                                   |                                                                            |   struct device_node *of_node; /* associated device tree node */     |
 |                                                               |     |                            |   | __virtio16 ring[];  |           +---------------------------------------------------+                                                                            |   struct fwnode_handle *fwnode; /* firmware device node */           |
 |   /* Last written value to avail+>idx in guest byte order */  |     |  struct vring_desc *desc;  |   |};                   |                                                                                                                                            |                                                                      |
 |   u16 avail_idx_shadow;                                       |     |                            |   +---------------------+---------+ +-----------------------------------------------------+                                                                          |   dev_t   devt; /* dev_t, creates the sysfs "dev" */                 |
 |                                                               |     |  struct vring_avail *avail;|   |struct vring_used {            | | struct virtio_driver {                              |                                                                          |   u32   id; /* device instance */                                    |
 |   /* How to notify other side. FIXME: commonalize hcalls! */  |     |                            |   | __virtio16 flags;             | |  struct device_driver driver;                       |                                                                          |                                                                      |
 |   bool (*notify)(struct virtqueue *vq);                       |     |  struct vring_used *used;  |   | __virtio16 idx;               | |  const struct virtio_device_id *id_table;           |                                                                          |   spinlock_t  devres_lock;                                           |
 |                                                               |     | };                         |   | struct vring_used_elem ring[];| |  const unsigned int *feature_table;                 |                                                                          |   struct list_head devres_head;                                      |
 |  #ifdef DEBUG                                                 |     |                            |   |};                             | |  unsigned int feature_table_size;                   |                                                                          |                                                                      |
 |   /* They're supposed to lock for us. */                      |     +----------------------------+   +-------------------------------+ |  const unsigned int *feature_table_legacy;          |                                                                          |   struct klist_node knode_class;                                     |
 |   unsigned int in_use;                                        |     +------------------------------------------------+                 |  unsigned int feature_table_size_legacy;            |                                                                          |   struct class  *class;                                              |
 |                                                               |     |struct vring_desc {                             |                 |  int (*probe)(struct virtio_device *dev);           |                                                                          |   const struct attribute_group **groups; /* optional groups */       |
 |   /* Figure out if their kicks are too delayed. */            |     | /* Address (guest-physical). */                |                 |  void (*scan)(struct virtio_device *dev);           |                                                                          |                                                                      |
 |   bool last_add_time_valid;                                   |     | __virtio64 addr;                               |                 |  void (*remove)(struct virtio_device *dev);         |                                                                          |   void (*release)(struct device *dev);                               |
 |   ktime_t last_add_time;                                      |     | /* Length. */                                  |                 |  void (*config_changed)(struct virtio_device *dev); |                                                                          |   struct iommu_group *iommu_group;                                   |
 |  #endif                                                       |     | __virtio32 len;                                |                 | #ifdef CONFIG_PM                                    |                                                                          |                                                                      |
 |                                                               |     | /* The flags as indicated above. */            |                 |  int (*freeze)(struct virtio_device *dev);          |                                                                          |   bool   offline_disabled:1;                                         |
 |   /* Tokens for callbacks. */                                 |     | __virtio16 flags;                              |                 |  int (*restore)(struct virtio_device *dev);         |                                                                          |   bool   offline:1;                                                  |
 |   void *data[];                                               |     | /* We chain unused descriptors via this, too */|                 | #endif                                              |                                                                          |  };                                                                  |
 |  };                                                           |     | __virtio16 next;                               |                 | };                                                  |                                                                          |                                                                      |
 |                                                               |     |};                                              |                 +-----------------------------------------------------+                                                                          +----------------------------------------------------------------------+
 +---------------------------------------------------------------+     +------------------------------------------------+                                                                                                                                                  +-------------------------------------------------------------------+
                                                                                                                                                                                                                                                                           | struct device_driver {                                            |
                                                                                                                                                                                                                                                                           |  const char  *name;                                               |
                                                                                                                                                                                                                                                                           |  struct bus_type  *bus;                                           |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  struct module  *owner;                                           |
                                                                                                                                                                                                                                                                           |  const char  *mod_name; /* used for built+in modules */           |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  bool suppress_bind_attrs; /* disables bind/unbind via sysfs */   |
                                                                                                                                                                                                                                                                           |  enum probe_type probe_type;                                      |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  const struct of_device_id *of_match_table;                       |
                                                                                                                                                                                                                                                                           |  const struct acpi_device_id *acpi_match_table;                   |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  int (*probe) (struct device *dev);                               |
                                                                                                                                                                                                                                                                           |  int (*remove) (struct device *dev);                              |
                                                                                                                                                                                                                                                                           |  void (*shutdown) (struct device *dev);                           |
                                                                                                                                                                                                                                                                           |  int (*suspend) (struct device *dev, pm_message_t state);         |
                                                                                                                                                                                                                                                                           |  int (*resume) (struct device *dev);                              |
                                                                                                                                                                                                                                                                           |  const struct attribute_group **groups;                           |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  const struct dev_pm_ops *pm;                                     |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           |  struct driver_private *p;                                        |
                                                                                                                                                                                                                                                                           | };                                                                |
                                                                                                                                                                                                                                                                           |                                                                   |
                                                                                                                                                                                                                                                                           +-------------------------------------------------------------------+
```
### 后端设备分析（QEMU）


[1] virtio-blk后端处理-请求接收、解析、提交
, http://blog.csdn.net/LPSTC123/article/details/45171515

[2] Qemu-kvm的ioeventfd创建与触发的大致流程, http://blog.csdn.net/LPSTC123/article/details/45111949

[3] virtio后端驱动详解, http://www.cnblogs.com/ck1020/p/5939777.html

[4] virtIO前后端notify机制详解, http://www.cnblogs.com/ck1020/p/6066007.html



后端设备已经在QEMU实现，所以要分析的代码在QEMU中。

* qemu中与virtio、virtio-blk相关的文件与目录结构：

```
hw/block/dataplane/virtio-blk.c
hw/block/dataplane/virtio-blk.h
hw/block/virtio-blk.c
hw/virtio/virtio.c
include/hw/virtio
include/hw/virtio/virtio-blk.h
include/hw/virtio/virtio.h
include/standard-headers/linux/virtio_blk.h
include/standard-headers/linux/virtio_ring.h
```
* 部分相关的重要数据结构
```
                                                         +------------------------------------------------------------------------------+
                                                         |                                                                              |
    hw/virtio/virtio.c                                   v                                                                              |
                                                                                                                                        |
     +----------------------------------------------------------+     +------------------------------+                                  |
     |   struct VirtQueue                                       |     |typedef struct VRing          |                                  |
     |   {                                                      |     |{                             |                                  |
     |       VRing vring;   <---------------------------------------> |    unsigned int num;         |                                  |
     |                                                          |     |    unsigned int num_default; |                                  |
     |       /* Next head to pop */                             |     |    unsigned int align;       |                                  |
     |       uint16_t last_avail_idx;                           |     |    hwaddr desc;              |                                  |
     |                                                          |     |    hwaddr avail;             |                                  |
     |       /* Last avail_idx read from VQ. */                 |     |    hwaddr used;              |                                  |
     |       uint16_t shadow_avail_idx;                         |     |} VRing;                      |                                  |
     |                                                          |     +------------------------------+                                  |
     |       uint16_t used_idx;                                 |                                                                       |
     |                                                          |     +------------------------------+ +------------------------------+ |
     |       /* Last used index value we have signalled on */   |     |  typedef struct VRingAvail   | |   typedef struct VRingDesc   | |
+--> |       uint16_t signalled_used;                           |     |  {                           | |   {                          | |
|    |                                                          |     |      uint16_t flags;         | |       uint64_t addr;         | |
|    |       /* Last used index value we have signalled on */   |     |      uint16_t idx;           | |       uint32_t len;          | |
|    |       bool signalled_used_valid;                         |     |      uint16_t ring[0];       | |       uint16_t flags;        | |
|    |                                                          |     |  } VRingAvail;               | |       uint16_t next;         | |
|    |       /* Notification enabled? */                        |     +------------------------------+ |   } VRingDesc;               | |
|    |       bool notification;                                 |     +------------------------------+ +------------------------------+ |
|    |                                                          |     | typedef struct VRingUsed     |                                  |
|    |       uint16_t queue_index;                              |     | {                            |                                  |
|    |                                                          |     |     uint16_t flags;          |                                  |
|    |       int inuse;                                         |     |     uint16_t idx;            |                                  |
|    |                                                          |     |     VRingUsedElem ring[0];   |                                  |
|    |       uint16_t vector;                                   |     | } VRingUsed;                 |                                  |
|    |       VirtIOHandleOutput handle_output;                  |     +------------------------------+                                  |
|    |       VirtIOHandleOutput handle_aio_output;              |     +------------------------------+                                  |
|    |       VirtIODevice *vdev;                                |     | typedef struct VRingUsedElem |                                  |
|    |       EventNotifier guest_notifier;                      |     | {                            |                                  |
|    |       EventNotifier host_notifier;                       |     |     uint32_t id;             |                                  |
|    |       QLIST_ENTRY(VirtQueue) node;                       |     |     uint32_t len;            |                                  |
|    |   };                                                     |     | } VRingUsedElem;             |                                  |
|    +----------------------------------------------------------+     +------------------------------+                                  |
|                                                                                                                                       |
|   include/hw/virtio/virtio-blk.h                          (kernel)/include/uapi/linux/virtio_blk.h                                    |
|                                                           include/standard-headers/linux/virtio_blk.h                                 |
|    +------------------------------------+                   +--------------------------------------+                                  |
|    |typedef struct VirtIOBlockReq {     | <---------------> |  struct virtio_blk_outhdr {          |                                  |
|    |    VirtQueueElement elem;          |                   |   /* VIRTIO_BLK_T* */                |                                  |
+----+    int64_t sector_num;             +----+              |   __virtio32 type;                   |                                  |
     |    VirtIOBlock *dev;               |    |              |   /* io priority. */                 |                                  |
     |    VirtQueue *vq;                  |    |              |   __virtio32 ioprio;                 |                                  |
+--> |    struct virtio_blk_inhdr *in;    | <--+              |   /* Sector (ie. 512 byte offset) */ |                                  |
|    |    struct virtio_blk_outhdr out;   |                   |   __virtio64 sector;                 |                                  |
|    |    QEMUIOVector qiov;              | <-------+         |  };                                  |                                  |
|    |    size_t in_len;                  |         |         +--------------------------------------+                                  |
|    |    struct VirtIOBlockReq *next;    |         |                                                                                   |
|    |    struct VirtIOBlockReq *mr_next; |         |                                                                                   |
|    |    BlockAcctCookie acct;           +---+     |        include/hw/virtio/virtio.h                                                 |
|    |} VirtIOBlockReq;                   |   |     |                                                                                   |
|    +-----------------------------------++   |     |                                                                                   |
|    +----------------------------+      |    |     |         +--------------------------------+                                        |
|    | struct virtio_blk_inhdr    |      |    |     |         |typedef struct VirtQueueElement |                                        |
|    | {                          |      |    |     |         |{                               |                                        |
|    |     unsigned char status;  | <----+    |     +-------> |    unsigned int index;         |                                        |
|    | };                         |           |               |    unsigned int out_num;       |                                        |
|    +----------------------------+           v               |    unsigned int in_num;        |                                        |
|    +----------------------------------------+---+           |    hwaddr *in_addr;            |                                        |
|    | typedef struct VirtIOBlock {               |           |    hwaddr *out_addr;           |                                        |
|    |     VirtIODevice parent_obj;               |           |    struct iovec *in_sg;        |                                        |
|    |     BlockBackend *blk;                     |           |    struct iovec *out_sg;       |                                        |
|    |     void *rq;                              |           |} VirtQueueElement;             |                                        |
|    |     QEMUBH *bh;                            |           +--------------------------------+                                        |
|    |     VirtIOBlkConf conf;                    |           +-----------------------------------------------------------+             |
|    |     unsigned short sector_mask;            |           |struct VirtIODevice                                        |             |
|    |     bool original_wce;                     |           |{                                                          |             |
|    |     VMChangeStateEntry *change;            |           |    DeviceState parent_obj;                                |             |
|    |     bool dataplane_disabled;               +---------> |    const char *name;                                      |             |
|    |     bool dataplane_started;                |           |    uint8_t status;                                        |             |
|    |     struct VirtIOBlockDataPlane *dataplane;|           |    uint8_t isr;                                           |             |
|    | } VirtIOBlock;                             |           |    uint16_t queue_sel;                                    |             |
|    |                                            | <-+       |    uint64_t guest_features;                               |             |
|    +--------------------------------------------+   |       |    uint64_t host_features;                                | <-----------+
|    +------------------------------+                 |       |    size_t config_len;                                     |
|    | struct VirtIOBlkConf         |                 |       |    void *config;                                          |
|    | {                            |                 |       |    uint16_t config_vector;                                |
|    |     BlockConf conf;          |                 |       |    uint32_t generation;                                   |
|    |     IOThread *iothread;      |                 |       |    int nvectors;                                          |
|    |     char *serial;            | <---------------+       |    VirtQueue *vq;                                         |
|    |     uint32_t scsi;           |                         |    uint16_t device_id;                                    |
|    |     uint32_t config_wce;     |                         |    bool vm_running;                                       |
|    |     uint32_t request_merging;|                         |    bool broken; /* device in invalid state, needs reset * |
|    |     uint16_t num_queues;     |                         |    VMChangeStateEntry *vmstate;                           |
|    | };                           |                         |    char *bus_name;                                        |
|    +------------------------------+                         |    uint8_t device_endian;                                 |
|    +----------------------------------------------------+   |    bool use_guest_notifier_mask;                          |
|    |typedef struct MultiReqBuffer {                     |   |    QLIST_HEAD(, VirtQueue) *vector_queues;                |
|    |    VirtIOBlockReq *reqs[VIRTIO_BLK_MAX_MERGE_REQS];|   |};                                                         |
+----+    unsigned int num_reqs;                          |   +-----------------------------------------------------------+
     |    bool is_write;                                  |
     |} MultiReqBuffer;                                   |
     +----------------------------------------------------+

    include/hw/virtio/virtio.h

     +----------------------------------------------------------------------+
     |typedef struct VirtioDeviceClass {                                    |
     |    /*v private >*/                                                   |
     |    DeviceClass parent;                                               |
     |    /*v public >*/                                                    |
     |                                                                      |
     |    /* This is what a VirtioDevice must implement */                  |
     |    DeviceRealize realize;                                            |
     |    DeviceUnrealize unrealize;                                        |
     |    uint64_t (*get_features)(VirtIODevice *vdev,                      |
     |                             uint64_t requested_features,             |
     |                             Error **errp);                           |
     |    uint64_t (*bad_features)(VirtIODevice *vdev);                     |
     |    void (*set_features)(VirtIODevice *vdev, uint64_t val);           |
     |    int (*validate_features)(VirtIODevice *vdev);                     |
     |    void (*get_config)(VirtIODevice *vdev, uint8_t *config);          |
     |    void (*set_config)(VirtIODevice *vdev, const uint8_t *config);    |
     |    void (*reset)(VirtIODevice *vdev);                                |
     |    void (*set_status)(VirtIODevice *vdev, uint8_t val);              |
     |    /* For transitional devices, this is a bitmap of features         |
     |     * that are only exposed on the legacy interface but not          |
     |     * the modern one.                                                |
     |     */                                                               |
     |    uint64_t legacy_features;                                         |
     |    /* Test and clear event pending status.                           |
     |     * Should be called after unmask to avoid losing events.          |
     |     * If backend does not support masking,                           |
     |     * must check in frontend instead.                                |
     |     */                                                               |
     |    bool (*guest_notifier_pending)(VirtIODevice *vdev, int n);        |
     |    /* Mask/unmask events from this vq. Any events reported           |
     |     * while masked will become pending.                              |
     |     * If backend does not support masking,                           |
     |     * must mask in frontend instead.                                 |
     |     */                                                               |
     |    void (*guest_notifier_mask)(VirtIODevice *vdev, int n, bool mask);|
     |    int (*start_ioeventfd)(VirtIODevice *vdev);                       |
     |    void (*stop_ioeventfd)(VirtIODevice *vdev);                       |
     |    /* Saving and loading of a device; trying to deprecate save/load  |
     |     * use vmsd for new devices.                                      |
     |     */                                                               |
     |    void (*save)(VirtIODevice *vdev, QEMUFile *f);                    |
     |    int (*load)(VirtIODevice *vdev, QEMUFile *f, int version_id);     |
     |    const VMStateDescription *vmsd;                                   |
     |} VirtioDeviceClass;                                                  |
     +----------------------------------------------------------------------+


```


### virtio-blk和multiqueue
用以下命令`gitk [QEMU_SRC]/hw/block/dataplane/virtio-blk.c` 搜索multiqueue，可以看到，virtio-blk dataplane在16年6月QEMU2.7开始支持multi VirtQueue了，但是这种multi是假的，因为还是只有一个IOThread，将来可能当QEMU Block layer支持multiqueue时，可能会使用multi IOThreads。
```

Author: Stefan Hajnoczi <stefanha@redhat.com>  2016-06-21 20:13:15
Committer: Stefan Hajnoczi <stefanha@redhat.com>  2016-06-28 20:08:32
Parent: b234cdda958b329dbbec840702c65432f4907623 (virtio-blk: tell dataplane which vq to notify)
Child:  ab3b9c1be8739f109596985588eb061b7f66c1d1 (virtio-blk: dataplane cleanup)
Branches: master, remotes/origin/master, remotes/origin/stable-2.10, remotes/origin/stable-2.7, remotes/origin/stable-2.8, remotes/origin/stable-2.9
Follows: v2.6.0
Precedes: v2.7.0-rc0

    virtio-blk: dataplane multiqueue support
    
    Monitor ioeventfds for all virtqueues in the device's AioContext.  This
    is not true multiqueue because requests from all virtqueues are
    processed in a single IOThread.  In the future it will be possible to
    use multiple IOThreads when the QEMU block layer supports multiqueue.
    
    Signed-off-by: Stefan Hajnoczi <stefanha@redhat.com>
    Reviewed-by: Fam Zheng <famz@redhat.com>
    Message-id: 1466511196-12612-7-git-send-email-stefanha@redhat.com
    Signed-off-by: Stefan Hajnoczi <stefanha@redhat.com>

                 ...
```

还可以注意到`[QEMU_SRC]/qemu/docs/devel/multiple-iothreads.txt`文件，以下是关于它的解释：
```
Author: Stefan Hajnoczi <stefanha@redhat.com>  2014-07-23 19:55:32
Committer: Kevin Wolf <kwolf@redhat.com>  2014-08-15 21:07:13
Parent: 8e436ec1f307a01882fd9166477667370c9dbfff (docs: Make the recommendation for the backing file name position a requirement)
Child:  5c6b3c50cca2106e5fbcbc6efa94c2f8b9d29fd8 (Merge remote-tracking branch 'remotes/stefanha/tags/tracing-pull-request' into staging)
Branches: master, remotes/origin/master, remotes/origin/stable-2.10, remotes/origin/stable-2.2, remotes/origin/stable-2.3, remotes/origin/stable-2.4, remotes/origin/stable-2.5, remotes/origin/stable-2.6, remotes/origin/stable-2.7, remotes/origin/stable-2.8, remotes/origin/stable-2.9
Follows: v2.1.0
Precedes: v2.2.0-rc0

    docs/multiple-iothreads.txt: add documentation on IOThread programming
    
    This document explains how IOThreads and the main loop are related,
    especially how to write code that can run in an IOThread.  Currently
    only virtio-blk-data-plane uses these techniques.  The next obvious
    target is virtio-scsi; there has also been work on virtio-net.
    
    Signed-off-by: Stefan Hajnoczi <stefanha@redhat.com>
    Reviewed-by: Eric Blake <eblake@redhat.com>
```
QEMU-devel上讨论过这个问题：is it possible to use a disk with multiple iothreads ?（http://qemu-devel.nongnu.narkive.com/evjo6jLa/is-it-possible-to-use-a-disk-with-multiple-iothreads）

Stefan Hajnoczi在KVM Forum 14中解释了IO Thread的设计（https://www.youtube.com/watch?v=KVD9FVlbqmY）

论文"Improving Performance by Bridging the Semantic Gap between Multi-queue SSD and I/O Virtualization Framework" 将QEMU原来的一个iothread变为多个，每个vCPU绑定一个。

### 相关资料

[1] [paper]virtio: Towards a De-Facto Standard For Virtual I/O Devices(http://www.ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)

[2] (KVM连载)5.1.1 VIRTIO概述和基本原理（KVM半虚拟化驱动, http://smilejay.com/2012/11/virtio-overview/

[3] Virtio 基本概念和设备操作, http://www.ibm.com/developerworks/cn/linux/1402_caobb_virtio/

[4] Virtio：针对 Linux 的 I/O 虚拟化框架, https://www.ibm.com/developerworks/cn/linux/l-virtio/

[5] [Linux KVM]半虚拟化驱动（Paravirtualization Driver, https://godleon.github.io/blog/2016/08/20/KVM-Paravirtualization-Drivers

[6] Virtio-Blk性能加速方案, http://royluo.org/2014/08/31/virtio-blk-improvement/

[7] Centos6下Virtio-SCSI(multi-queues)/Virtio-SCSI/Virtio-blk性能对比, http://blog.csdn.net/bobpen/article/details/41515119

[8] QEMU-KVM I/O性能优化之Virtio-blk-data-plane, http://blog.sina.com.cn/s/blog_9c835df30102vpgd.html

[9] read 系统调用剖析, https://www.ibm.com/developerworks/cn/linux/l-cn-read/

[10] virtio驱动如何同设备交互, http://blog.csdn.net/qiushanjushi/article/details/38404341

[11] Virtio-Blk浅析, http://royluo.org/2014/08/29/virtio-blk/
