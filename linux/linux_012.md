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

#### taskset