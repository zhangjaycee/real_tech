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
