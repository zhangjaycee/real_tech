# 包管理器


## pip

pip install *pkg_name*[==*version*]

加 -i参数可以临时换源，防止官方源国内太慢
```
#常用国内源
#豆瓣
http://pypi.douban.com/simple/
#清华
https://pypi.tuna.tsinghua.edu.cn/simple
```

## gem

gem install *pkg_name* [-v *version*]

## yum

yum list *pkg_name* 列出所有版本

yum install *pkg_version* 安装指定版本

```bash
更新：yum update
安装：yum install xxx
移除：yum remove xxx
清除已经安装过的档案（/var/cache/yum/）：yum clean all

搜寻：yum search xxx

列出所有可安装的软件包：yum list
eg：yum list php*

列出所指定的软件包 
命令：yum list <package_name>

列出所有可更新的软件包 
命令：yum list updates

列出所有已安装的软件包 
命令：yum list installed

列出所有已安装但不在 Yum Repository 內的软件包 
命令：yum list extras

查询档案讯息：yum info xxx
```

## apt

* 常用

apt install *pkg_name*[=*version*] 安装[指定版本的]包

apt-cache search *pkg_name* 模糊搜索包，后边会列出每个包大概是做什么的

apt list [-a] *pkg_name* 列出[所有]包的版本

* 其他

```bash

配置文件/etc/apt/sources.list 
常用的APT命令参数： 

apt-cache show package 获取包的相关信息，如说明、大小、版本等 

apt-get install package 安装包 

apt-get install package - - reinstall 重新安装包 

apt-get -f install 修复安装"-f = ——fix-missing" 

apt-get remove package 删除包 

apt-get remove package - - purge 删除包，包括删除配置文件等 

apt-get update 更新源 ，重新获取软件包列表

apt-get upgrade 更新已安装的包 

apt-get dist-upgrade 升级系统 

apt-get dselect-upgrade 依照dselect 的选择更新 

apt-cache depends package 了解使用依赖 

apt-cache rdepends package 是查看该包被哪些包依赖 

apt-get build-dep package 安装相关的编译环境 

apt-get source package 下载该包的源代码 

apt-get clean && apt-get autoclean 清理无用的包 

apt-get check 检查是否有损坏的依赖
```

> 参考：

> http://494981.blog.51cto.com/484981/1383655