# Xen的Hypervisor和Domain0的关系

>参考 http://www.xuebuyuan.com/556261.html?mobile=1

* 在《Xen Virtualization》中对“Xen domain”作了如下定义：
>Xen domain is a specific instance of a Xen virtual machine running on a specific physical piece of hardware.

意思是说domain是运行在物理硬件上的Xen虚拟机的一个实例。通俗点说就是一个Xen虚拟出来的虚拟机实例，不要忘记了Xen是一个可以创建和管理虚拟机的软件。这里不说“Xen”是虚拟机软件，就像我们平时说虚拟机就说VMWare。因为虚拟机是Xen虚拟出来的产物，不是Xen本身。
* 关于domain，《Xen virtualization》中还说：
>Xen supports two basic types of domains with different uses and capabilities.

这说明domain是Xen虚拟的产物，而Domain0是Xen虚拟出的产物中的一个最特殊的一个。其特殊之处在后面会提到。
Xen有能力虚拟出虚拟机，那么有相关的方法管理这些虚拟机的。
* 《Xen virtualzation》中说:
>Xen manages access to memory and hardware resources through a combination of its hypervisor and a specially privileged Xen-modified kernel that is used to manage,monitor ,and administer all other Xen virtual machines running on a specific piece of hardware.This
specially privileged Xen kernel is known as domain0.

上面清楚的说，Xen是借助管理程序（Hypervisor）和Domain0管理内存和硬件资源的访问的。
Hypervisor和Domain都有管理内存和硬件资源的访问的。而需要访问内存和硬件资源的自然就是虚拟机了，所以就达到了管理其他虚拟机的目的了。Domain0的管理功能就是其特殊之处。
那么这两个东西具体管理着些什么呢？又是怎么分工管理的呢？
继续，
* 在《Xen virtualzation》中说：
>One of the goals of Xen has always been to separate implementation requirements from policy decisions, leaving administrative and configuration options to the domain0 system rather than hardwiring them into the hypervisor. Loe-level CPU and memory allocation
and management is done by the hypervisor because this is a physical requirement for running multiple virtual machines on a single physical system. The hypervisor is responsible for creating , managing ,and deleting the virtual network interfaces and virtual
block devices associated with each guest domain.

上面的意思大致是说“Xen把策略的制定和策略的实施分离，把管理和配置工作交给Domain0进行，而不将管理和配置工作交给Hypervisor实施”。翻译的比较勉强，通俗的说就是 “虚拟机的管理工作分为两类，一类是确定如何管理，一类是确定管理之后的实施。Domain0进行第一类，Hypervisor进行第二类。”就是说，我们在Domain0中可以设置对虚拟机的管理参数，Hypervisor按照我们做Domain0中设置的参数去设置虚拟机。
这就是Hypervisor和Domain0的关系。
