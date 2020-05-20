## About SSH

## Ubuntu上开启SSH服务

SSH分客户端openssh-client和openssh-server，openssh-client已经系统自带安装了，要使本机开放SSH服务就需要安装openssh-server

* apt安装
>sudo apt-get install openssh-server

* 确认sshserver是否启动
>ps -ef |grep sshd

* 如果没有则可以这样启动
>sudo /etc/init.d/ssh start

* 配置ssh-server
ssh-server配置文件位于/etc/ssh/sshd_config ，可以定义SSH的服务端口，默认端口是22。
配置后需要然后重启SSH服务：
>sudo service ssh restart

* 客户机可以登陆SSH
>ssh _username_@_sshserver_ip_ [-p _端口号_]

* 断开连接
>exit


## SCP
* 上传
```
# 命令：
scp -pr -P [port_number] [path_to_upload] [user_name]@[server_address]:[dir]
# 例子：
scp -pr -P 22 ~/Desktop/mycode.tar.gz root@192.168.1.10:~/srcs/
```

* 下载
```
# 命令：
scp -pr -P [port_number] [user_name]@[server_address]:[dir] [path_to_download] 
# 例子：
scp -pr -P 22 root@192.168.1.10:~/srcs/server_code.tar.gz ~/Desktop/
```

## 建立无须密码验证的ssh/scp连接

1.Client上某用户执行ssh-keygen命令，生成建立安全信任关系的证书
```shell
ssh-keygen -b 1024 -t rsa
```

2.将公钥证书id_rsa.pub内容复制到Server某用户的~/.ssh/authorized_keys目录中
```shell
## 方法1
scp -p ~/.ssh/id_rsa.pub  [username]@[server_ip]:[user_home]/.ssh/authorized_keys
## 方法2
client: cat ~/.ssh/id_rsa.pub #然后复制它
server: vim ~/.ssh/authorized_keys #然后粘贴保存
```

3.完成

### 注意
对于非root用户，文件的权限可能导致出现问题：

---

[1]linux 非root用户 普通用户ssh 登录 解决, http://www.blogjava.net/hello-yun/archive/2012/05/16/378329.html


## 利用ssh命令配置一台远程服务器作为git配置代理

```bash
# 监听本地1080端口为socks5代理，
ssh -Nf -D 0.0.0.0:1080 USERNAME@REMOTE_IP
# 配置git以刚刚简历的本地socks5代理来进行网络通信
git config --global http.proxy "socks5://127.0.0.1:1080"
```

---
[1] 搭建socks5代理的几种方法, https://www.cnblogs.com/dgjnszf/p/11752817.html