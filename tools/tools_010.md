# 配置pptpd

[Ubuntu 16.04环境下]

* 安装pptpd
```bash
$ apt install pptpd
```

* 配置pptpd.conf参数

~~~bash
$ vim /etc/pptpd.conf

option /etc/ppp/pptpd-options                   #指定PPP选项文件的位置
localip 192.168.0.1                             #VPN服务器的虚拟ip
remoteip 192.168.0.200-238,192.168.0.245        #分配给VPN客户端的虚拟ip
~~~

* 设置账号密码

```bash
$vim  /etc/ppp/chap-secrets

#格式：用户名   服务类型   密码   分配的ip地址
#第一个*代表服务可以是PPTPD也可以是L2TPD，第二个*代表随机分配ip
testpptp    *    12345678    *
```
* 配置dns

```bash
$ vim /etc/ppp/pptpd-options

# 找到ms-dns，取消注释，改成你喜欢的DNS
ms-dns 114.114.114.114
ms-dns 8.8.8.8
```

* 打开ipv4转发

```bash
# 打开配置文件
$ vim /etc/sysctl.conf

# 取消下面一行的注释：
net.ipv4.ip_forward=1

# 让配置生效
$ sysctl -p
```

* 配置NAT转发

```bash
# eth0 换成你的网口
$ iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

* 重启pptpd服务

```bash
$ service pptpd restart
```


> https://www.zivers.com/post/1498.html
>
> http://blog.csdn.net/junmuzi/article/details/62227073