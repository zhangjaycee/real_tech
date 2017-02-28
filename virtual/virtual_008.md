# 关于virtio

> https://wiki.archlinux.org/index.php/QEMU#Installing_virtio_drivers

> [paper] [virtio: Towards a De-Facto Standard For Virtual I/O Devices](http://www.ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)

> [Virtio基本原理(KVM半虚拟化驱动)](https://my.oschina.net/davehe/blog/130124)

> [(KVM连载)5.1.1 VIRTIO概述和基本原理（KVM半虚拟化驱动）](http://smilejay.com/2012/11/virtio-overview/)

> [Virtio 基本概念和设备操作 ⭐️ ] (http://www.ibm.com/developerworks/cn/linux/1402_caobb_virtio/)

> [Virtio：针对 Linux 的 I/O 虚拟化框架](https://www.ibm.com/developerworks/cn/linux/l-virtio/)

> [[Linux KVM]半虚拟化驱动（Paravirtualization Driver）](https://godleon.github.io/blog/2016/08/20/KVM-Paravirtualization-Drivers)

> [Virtio-Blk性能加速方案](http://royluo.org/2014/08/31/virtio-blk-improvement/)

> [Centos6下Virtio-SCSI(multi-queues)/Virtio-SCSI/Virtio-blk性能对比](http://blog.csdn.net/bobpen/article/details/41515119)

> [virtio-blk浅析 ⭐️ ](http://www.2cto.com/os/201408/329744.html)

> [QEMU-KVM I/O性能优化之Virtio-blk-data-plane](http://blog.sina.com.cn/s/blog_9c835df30102vpgd.html)

> [virtio-blk后端处理-请求接收、解析、提交
](http://blog.csdn.net/LPSTC123/article/details/45171515)⭐️


### 概述

对于qemu/kvm虚拟机来说，用不用virtio，决定了我们的虚拟化是半虚拟化还是全虚拟化。

决定虚拟机是半虚拟还是全虚拟的性质转变的标准只有一个：Guest机知不知道自己是一个虚拟机。具体来说，不使用virtio，虚拟机会像在真实物理环境下运行一样地运行——它不认为它是虚拟机；而使用virtio，就是让两部分virtio程序的互相通信，这两部分程序分别是前端驱动(frontend, Guest中)和后端设备(backend, Host中)，这样因为Guest中有了virtio的frontend部分，所以它的运行和物理机环境下有了区别，Guest按照一个使用virtio的虚拟机的方式运行——它知道了它是一个虚拟机。

virtio提高了io效率，（？也为host和guest间更复杂的合作机制实现提供了便利）


### 源码以及结构

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

* include/linux/virtio.h
```cpp
#ifndef _LINUX_VIRTIO_H
#define _LINUX_VIRTIO_H
/* Everything a virtio driver needs to work with any particular virtio
 * implementation. */
#include <linux/types.h>
#include <linux/scatterlist.h>
#include <linux/spinlock.h>
#include <linux/device.h>
#include <linux/mod_devicetable.h>
#include <linux/gfp.h>
#include <linux/vringh.h>

/**
 * virtqueue - a queue to register buffers for sending or receiving.
 * @list: the chain of virtqueues for this device
 * @callback: the function to call when buffers are consumed (can be NULL).
 * @name: the name of this virtqueue (mainly for debugging)
 * @vdev: the virtio device this queue was created for.
 * @priv: a pointer for the virtqueue implementation to use.
 * @index: the zero-based ordinal number for this queue.
 * @num_free: number of elements we expect to be able to fit.
 *
 * A note on @num_free: with indirect buffers, each buffer needs one
 * element in the queue, otherwise a buffer will need one element per
 * sg element.
 */
struct virtqueue {
	struct list_head list;
	void (*callback)(struct virtqueue *vq);
	const char *name;
	struct virtio_device *vdev;
	unsigned int index;
	unsigned int num_free;
	void *priv;
};

int virtqueue_add_outbuf(struct virtqueue *vq,
			 struct scatterlist sg[], unsigned int num,
			 void *data,
			 gfp_t gfp);

int virtqueue_add_inbuf(struct virtqueue *vq,
			struct scatterlist sg[], unsigned int num,
			void *data,
			gfp_t gfp);

int virtqueue_add_sgs(struct virtqueue *vq,
		      struct scatterlist *sgs[],
		      unsigned int out_sgs,
		      unsigned int in_sgs,
		      void *data,
		      gfp_t gfp);

bool virtqueue_kick(struct virtqueue *vq);

bool virtqueue_kick_prepare(struct virtqueue *vq);

bool virtqueue_notify(struct virtqueue *vq);

void *virtqueue_get_buf(struct virtqueue *vq, unsigned int *len);

void virtqueue_disable_cb(struct virtqueue *vq);

bool virtqueue_enable_cb(struct virtqueue *vq);

unsigned virtqueue_enable_cb_prepare(struct virtqueue *vq);

bool virtqueue_poll(struct virtqueue *vq, unsigned);

bool virtqueue_enable_cb_delayed(struct virtqueue *vq);

void *virtqueue_detach_unused_buf(struct virtqueue *vq);

unsigned int virtqueue_get_vring_size(struct virtqueue *vq);

bool virtqueue_is_broken(struct virtqueue *vq);

void *virtqueue_get_avail(struct virtqueue *vq);
void *virtqueue_get_used(struct virtqueue *vq);

/**
 * virtio_device - representation of a device using virtio
 * @index: unique position on the virtio bus
 * @failed: saved value for VIRTIO_CONFIG_S_FAILED bit (for restore)
 * @config_enabled: configuration change reporting enabled
 * @config_change_pending: configuration change reported while disabled
 * @config_lock: protects configuration change reporting
 * @dev: underlying device.
 * @id: the device type identification (used to match it with a driver).
 * @config: the configuration ops for this device.
 * @vringh_config: configuration ops for host vrings.
 * @vqs: the list of virtqueues for this device.
 * @features: the features supported by both driver and device.
 * @priv: private pointer for the driver's use.
 */
struct virtio_device {
	int index;
	bool failed;
	bool config_enabled;
	bool config_change_pending;
	spinlock_t config_lock;
	struct device dev;
	struct virtio_device_id id;
	const struct virtio_config_ops *config;
	const struct vringh_config_ops *vringh_config;
	struct list_head vqs;
	u64 features;
	void *priv;
};

static inline struct virtio_device *dev_to_virtio(struct device *_dev)
{
	return container_of(_dev, struct virtio_device, dev);
}

int register_virtio_device(struct virtio_device *dev);
void unregister_virtio_device(struct virtio_device *dev);

void virtio_break_device(struct virtio_device *dev);

void virtio_config_changed(struct virtio_device *dev);
#ifdef CONFIG_PM_SLEEP
int virtio_device_freeze(struct virtio_device *dev);
int virtio_device_restore(struct virtio_device *dev);
#endif

/**
 * virtio_driver - operations for a virtio I/O driver
 * @driver: underlying device driver (populate name and owner).
 * @id_table: the ids serviced by this driver.
 * @feature_table: an array of feature numbers supported by this driver.
 * @feature_table_size: number of entries in the feature table array.
 * @feature_table_legacy: same as feature_table but when working in legacy mode.
 * @feature_table_size_legacy: number of entries in feature table legacy array.
 * @probe: the function to call when a device is found.  Returns 0 or -errno.
 * @remove: the function to call when a device is removed.
 * @config_changed: optional function to call when the device configuration
 *    changes; may be called in interrupt context.
 */
struct virtio_driver {
	struct device_driver driver;
	const struct virtio_device_id *id_table;
	const unsigned int *feature_table;
	unsigned int feature_table_size;
	const unsigned int *feature_table_legacy;
	unsigned int feature_table_size_legacy;
	int (*probe)(struct virtio_device *dev);
	void (*scan)(struct virtio_device *dev);
	void (*remove)(struct virtio_device *dev);
	void (*config_changed)(struct virtio_device *dev);
#ifdef CONFIG_PM
	int (*freeze)(struct virtio_device *dev);
	int (*restore)(struct virtio_device *dev);
#endif
};

static inline struct virtio_driver *drv_to_virtio(struct device_driver *drv)
{
	return container_of(drv, struct virtio_driver, driver);
}

int register_virtio_driver(struct virtio_driver *drv);
void unregister_virtio_driver(struct virtio_driver *drv);

/* module_virtio_driver() - Helper macro for drivers that don't do
 * anything special in module init/exit.  This eliminates a lot of
 * boilerplate.  Each module may only use this macro once, and
 * calling it replaces module_init() and module_exit()
 */
#define module_virtio_driver(__virtio_driver) \
	module_driver(__virtio_driver, register_virtio_driver, \
			unregister_virtio_driver)
#endif /* _LINUX_VIRTIO_H */

```


* include
```

```

