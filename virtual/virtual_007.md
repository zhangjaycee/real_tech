# 关于Qemu/KVM 虚拟机的网络配置

# 系统概况： 
* host 和 guest 都是用的 Ubuntu Server 16.04系统。
* 我的 host 机上有三块网卡2块有线网卡(接口 enp1s0 和 enp3s0)和1个无线网卡(接口 wls2s0)。
* 我的 host 机通过无线网卡连在一个路由器上，并因此能够连接到互联网，所在的网段是192.168.3.0\24，ip 固定为192.168.3.5。
* 其他两块有线网卡没有连接。

# 实验0：
## 效果：
guest 与 guest、guest 与 host 之间可以互相 ping 通；guest 不能访问 host 所在路由器网段(192.158.3.0\24)。
## 方案：
在 host 中搭建了一个虚拟网桥，将 qemu-bridge-helper 工具在启动虚拟机时创建的虚拟网络接口 tap0[1,2...] 与 host 桥接在一起，我手动配置了他们的网段是192.168.4.0\24。

## 步骤：

1.配置 host 的 /etc/network/interfaces ，在其中加入以下内容，然后通过 `/etc/init.d/networking restart` 重启服务来创建网桥。

~~~
auto br0
iface br0 inet static
address 192.168.4.1 # br0 的 ip 在192.168.4.0\24
netmask 255.255.255.0 
#bridge_ports enp1s0 # 实验发现，这里没必要将 host 的实体接口桥接，所以注释了起来
bridge_ports none # 但是又发现，这里不设置这个参数会导致网桥创建失败，所以我们可以
                  # 写一个不存在的接口来混过这个检查，比如我这里写了个 none
bridge_stp on
~~~

2.将刚建的虚拟网桥名称加入到 /etc/qemu/bridge.conf 或者 /usr/local/etc/qemu/bridge.conf，比如这里：
~~~
br0
~~~

3.启动 Qemu 虚拟机，这里的 `-net bridge,br=br0` 指定了网桥模式，qemu 会用 qemu-bridge-helper 创建 tap0 虚拟网络接口桥接入br0 的，我的启动命令如下：

~~~bash
# 注意如果创建两个以上虚拟机的时候，应该手动指定 mac 地址防止多个 guest 的 mac地址 重复
# 导致 guest 之间不能互相 ping 通，比如：
qemu-system-x86_64 -m 1000 -enable-kvm ~/vmimgs/u1604server.img \
-net nic,macaddr=52:54:00:12:34:57 -net bridge,br=br0 -vnc :1
~~~

4.通过 vnc 连入 guest，配置其 /etc/network/interfaces 文件，然后通过 `/etc/init.d/networking restart` 重启服务。
~~~
# KVM GUEST: /etc/network/interfaces

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto ens3
iface ens3 inet static
address 192.168.4.101 # 这个 ip 为手动指定，应在 br0 的同一网段
netmask 255.255.255.0
gateway 192.168.4.1 # 这里应该设置成 host 中 br0 的 ip，
                    # 相当于创建了默认到 br0 ip 的路由
#up route add default gw 192.168.4.1 dev ens3 # 经过实验，这句于上一句效果等
                                              # 价，二者留一即可，所以注释掉了

~~~

## 测试
~~~bash
#guest0(192.168.4.101) 中：
ping 192.168.4.1 -c 3 成功
ping 192.168.4.102 -c 3 成功
ssh jcvm0@192.168.4.102 登陆成功
#guest1(192.168.4.102) 中：
ping 192.168.4.1 -c 3 成功
ping 192.168.4.101 -c 3 成功
ssh jcvm0@192.168.4.101 登陆成功
#host 中：
ping 192.168.4.101 -c 3 成功
ping 192.168.4.102 -c 3 成功
ssh jcvm0@192.168.4.101 登陆成功
~~~

# 实现1：
## 实现效果：
在实验0的基础上，实现 guest 通过无线接口的网络连接互联网，相当于 host 做了一个 NAT。
## 步骤：
1. **以实验0为基础。**
2. 开启路由转发：编辑 /etc/sysctl.conf 配置文件，将 net.ipv4.ip_forward = 0 修改为net.ipv4.ip_forward = 1， 重启 host。
3. 利用 iptables 搭建 MASQUERADE 模式的 NAT，执行下面两条命令的一条即可，本实验中效果相同：
~~~
# 第一条命令中将 192.168.4.0\24 网段的数据包伪装成 wlp2s0 接口的 ip 
# 发送出去，所以要实现 guest 通过 NAT 共享上网，wlp2s0 处应该填写连入
# 互联网的网络接口，这里 wlp2s0 是我的无线网卡接口。
iptables -t nat -A POSTROUTING -s "192.168.4.0/255.255.255.0" -o wlp2s0 -j MASQUERADE 
# 第一条命令中将 192.168.4.0\24 网段的数据包伪装成 192.168.4.0\24 外的任何 ip 
# 发送出去，按我的理解 iptables 会自动判断哪些 ip 可以成为伪装的目标，所以这条命令
# 可能更加通用。
iptables -t nat -A POSTROUTING -s "192.168.4.0/255.255.255.0" ! -d "192.168.4.0/255.255.255.0" -j MASQUERADE
~~~

4.通过 vnc 连入 guest，配置其 /etc/network/interfaces 文件，然后通过 `/etc/init.d/networking restart` 重启服务。配置的方法只是在实验0的基础上加了一句，来配置 dns 服务器：
~~~
# KVM GUEST: /etc/network/interfaces

source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

auto ens3
iface ens3 inet static
address 192.168.4.101 # 这个 ip 为手动指定，应在 br0 的同一网段
netmask 255.255.255.0
gateway 192.168.4.1 # 这里应该设置成 host 中 br0 的 ip，相当于创建了默认到 br0 ip 的路由
#up route add default gw 192.168.4.1 dev ens3 # 经过实验，这句于上一句效果等价，二者留一即可，所以注释掉了
dns-nameservers 192.168.3.1 # 将 dns 服务器设置为我的路由器 ip 即可
~~~

## 测试
~~~bash
#guest0(192.168.4.101) 中：
ping 192.168.3.1 -c 3 成功
ping baidu.com -c 3 成功
#guest1(192.168.4.102) 中：
ping 192.168.3.1 -c 3 成功
ping baidu.com -c 3 成功
~~~


> [Tap networking with QEMU] https://wiki.archlinux.org/index.php/QEMU#Tap_networking_with_QEMU

> [qemu用tap方式启动vm的网络试验(ip route)] http://haoningabc.iteye.com/blog/2324350

> [Network bridge] https://wiki.archlinux.org/index.php/Network_bridge

> [qemu-bridge-helper Features] http://wiki.qemu.org/Features/HelperNetworking

> [4.4.1 QEMU支持的网络模式] http://smilejay.com/2012/08/qemu-kvm-networking-mode/

> [4.4.2 使用网桥模式] http://smilejay.com/2012/08/kvm-bridge-networking/

> [[关于virtio|virtual_008]]

> [KvmWithBridge] https://wiki.ubuntu.com/KvmWithBridge


