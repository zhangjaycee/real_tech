# 搭建SMB共享文件服务器

(Ubuntu为例)

1. 安装smb服务端。

2. 添加一个Linux用户，创建一个共享文件夹，如：
```
sudo adduser nbjl
su nbjl
cd /home/nbjl
mkdir sharedir
```
3. 添加 **对应的** smb用户
```
sudo smbpasswd -a nbjl
```


4. 修改 /etc/samba/smb.conf,添加示例：
```
[nbjl-storage]
path = /home/nbjl/sharedir
valid users = nbjl
read only = no
```

5. 重启smb服务器
```bash
sudo service smbd restart
```


---
[1] How to Create a Network Share Via Samba Via CLI (Command-line interface/Linux Terminal) - Uncomplicated, Simple and Brief Way!, https://help.ubuntu.com/community/How%20to%20Create%20a%20Network%20Share%20Via%20Samba%20Via%20CLI%20%28Command-line%20interface/Linux%20Terminal%29%20-%20Uncomplicated%2C%20Simple%20and%20Brief%20Way%21