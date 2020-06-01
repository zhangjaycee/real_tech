# QEMU-KVM网络栈

## 1. Host创建和配置网桥br0

* 创建网桥br0
```bash
ip link add br0 type bridge
ifconfig br0 up
```

* 为网桥绑定ip。设置`/etc/sysconfig/network-scripts/ifcfg-br0`文件，将网桥ip设置成192.168.10.1，后续我们将配置虚拟机中与tap后端所对应的网卡为192.168.10.XXX：

```bash
DEVICE=br0
#ONBOOT=yes
BOOTPROTO=static
IPADDR=192.168.10.1
NETMASK=255.255.255.0
GATEWAY=220.113.20.38
NM_CONTROLLED=NO
```

* 重启网络服务：
```bash
systemctl network restart
```

## 2. 设置qemu-ifup和qemu-ifdown脚本[4]

qemu-ifup脚本会被设置`-netdev tap`参数的QEMU调用，来创建tap接口并绑定到br0网桥上。qemu-ifdown则是解绑和销毁tap接口。

* `/etc/qemu-ifup`

```bash
#!/bin/sh
set -x

switch=br0

if [ -n "$1" ];then
        #tunctl -u `whoami` -t $1
        ip tuntap add $1 mode tap user `whoami`
        ip link set $1 up
        sleep 0.5s
        #brctl addif $switch $1
        ip link set $1 master $switch
        exit 0
else
        echo "Error: no interface specified"
        exit 1
fi
```

* `/etc/qemu-ifdown`

```bash
#!/bin/bash
#This is a qemu-ifdown script for bridging.
#You can use it when starting a KVM guest with bridge mode network.
#Don't use this script in most cases; QEMU will handle it automatically.

#set your bridge name
switch=br0

if [ -n "$1" ]; then
    # Delete the specified interfacename
    # tunctl -d $1
    #release TAP interface from bridge
    brctl delif ${switch} $1
    #shutdown the TAP interface
    ip link set $1 down
    exit 0
else
    echo "Error: no interface specified"
    exit 1
fi
```

## 3. 用适当的QEMU参数启动Guest

* 这里设置了两个网卡，一个使用user模式的网络后端，转发ssh协议的22端口到2222，连入虚拟机进一步配置；
另一个是绑定到网桥的tap设备作为后端，用于虚拟机间的通信。

```bash
qemu-system-x86_64 \
... \
-device virtio-net,netdev=n0,mac=52:55:00:d1:55:00 \
-netdev user,hostfwd=tcp::2222-:22,id=n0 \
-device virtio-net,netdev=n1,mac=52:55:00:d1:56:00 \
-netdev tap,id=n1
... 
```

## 4. 进入设置guest进行配置

* 用user模式后端的2222端口进入guest

```bash
ssh root@localhost -p2222
```

* 配置guest tap0对应网口的静态ip。

我的guest中，user网卡对应eth0，ip已经是10.0.2.15；tap网卡对应eth1，因此应该编辑`/etc/sysconfig/network-scriptes/ifcfg-eth1`：

```bash
DEVICE=eth1
ONBOOT=yes
BOOTPROTO=static
IPADDR=192.168.10.2
NETMASK=255.255.255.0
GATEWAY=192.168.10.1
#NM_CONTROLLED=NO
```

* Guest中设置路由表[3]
```bash
ip route add default via 10.0.2.2 dev eth0
ip route add 192.168.10.0/24 via 192.168.10.1 dev eth1
```


---

[1] https://www.linux-kvm.org/page/Networking

[2] https://www.qemu.org/2018/05/31/nic-parameter/

[3] https://serverfault.com/questions/123553/how-to-set-the-preferred-network-interface-in-linux

[4] https://github.com/smilejay/kvm-book/blob/master/scripts/qemu-ifup
