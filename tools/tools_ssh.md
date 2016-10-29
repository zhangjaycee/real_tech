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