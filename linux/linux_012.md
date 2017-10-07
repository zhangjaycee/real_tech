## Linux下限制硬件资源(CPU核心数)


#### 动态开关CPU核心数

> https://www.cyberciti.biz/faq/debian-rhel-centos-redhat-suse-hotplug-cpu/

> http://www.2cto.com/os/201306/220885.html

通过linux支持的cpu核心的hotplug，可以系统全局限制使用CPU的核心数。例子：

~~~bash
# 开启第二个CPU核
echo 1 > /sys/devices/system/cpu/cpu1/online
# 关闭第二个CPU核
echo 0 > /sys/devices/system/cpu/cpu1/online
~~~


#### ulimit

#### cgroups

06年被提出，已经在内核中，可以限制CPU、内存和IO

[1] Cgroups控制cpu，内存，io示例, http://www.cnblogs.com/yanghuahui/p/3751826.html

[2] Docker背后的内核知识——cgroups资源限制, http://www.infoq.com/cn/articles/docker-kernel-knowledge-cgroups-resource-isolation

#### taskset