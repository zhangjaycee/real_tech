# 关于Qemu/KVM 虚拟机的网络配置

# 实现1：
## 实现效果：
0. 我的实验平台host有2个以太网卡(有线网卡)和1个无线网卡，实验用了一个有线网卡(enp1s0)和一个无线网卡(enp2s0)网卡host 和 guest 之间都是用的 Ubuntu Server 16.04系统。
1. guest和host不在一个网段，如：我的host机通过wls2p0无线网卡连接在192.168.3.*网段的无线路由器下；而各guest和host机的ens1p0有线网卡桥接在一起，并都被手动分配了192.168.4.*网段。
2.  


# 创建一个bridge
1. 创建
> [Network bridge] https://wiki.archlinux.org/index.php/Network_bridge

2. DHCP (?)

# 创建 /usr/local/etc/qemu/bridge.conf (例如)
~~~
vmridge0
vmridge1
vmbr0
br0
br1
~~~

# 把 /usr/local/libexec/qemu-bridge-helper加上可执行权限

# 执行命令
~~~
sudo qemu-system-x86_64 -m 1000 -enable-kvm [bridge_name].img -net nic -net bridge,br=[bridge_name] -vnc :1
~~~

# 参考

> [Tap networking with QEMU] https://wiki.archlinux.org/index.php/QEMU#Tap_networking_with_QEMU

> [4.4.1 QEMU支持的网络模式] http://smilejay.com/2012/08/qemu-kvm-networking-mode/

> [4.4.2 使用网桥模式] http://smilejay.com/2012/08/kvm-bridge-networking/

> [qemu-kvm桥接网络报错问题] http://www.361way.com/qemu-kvm-bridge-net/4760.html

> [Features/HelperNetworking] http://wiki.qemu.org/Features/HelperNetworking

> [[关于virtio|virtual_008]]

> [Network bridge] https://wiki.archlinux.org/index.php/Network_bridge

> [KvmWithBridge] https://wiki.ubuntu.com/KvmWithBridge

> [qemu用tap方式启动vm的网络试验(ip route)] http://haoningabc.iteye.com/blog/2324350
