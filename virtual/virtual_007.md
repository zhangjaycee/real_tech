# 关于Qemu/KVM 虚拟机的网络配置

> [Tap networking with QEMU] https://wiki.archlinux.org/index.php/QEMU#Tap_networking_with_QEMU

> [4.4.1 QEMU支持的网络模式] http://smilejay.com/2012/08/qemu-kvm-networking-mode/

> [4.4.2 使用网桥模式] http://smilejay.com/2012/08/kvm-bridge-networking/

> [qemu-kvm桥接网络报错问题] http://www.361way.com/qemu-kvm-bridge-net/4760.html

> [Features/HelperNetworking] http://wiki.qemu.org/Features/HelperNetworking

> [[关于virtio|virtual_008]]

> [Network bridge] https://wiki.archlinux.org/index.php/Network_bridge

1. 创建一个bridge

2. 创建 /usr/local/etc/qemu/bridge.conf (例如)
~~~
vmridge0
vmridge1
~~~

3. 把 /usr/local/libexec/qemu-bridge-helper加上可执行权限

4. 执行命令
