# Mac Terminal下怎么让Git命令可以在按Tab时自动补全[转]

原文：http://blog.csdn.net/zhangt85/article/details/43611997

直接进入正题：

```shell
$ brew list
```

查看你是否已经安装了"`bash-completion"，如果没有，继续往下看：`

```shell
$ brew install bash-completion
#####安装完成之后######
$ brew info bash-completion 　
#####下边这句话很重要#######
==> Caveats
Add the following lines to your ~/.bash_profile:
if [ -f $(brew --prefix)/etc/bash_completion ]; then
. $(brew --prefix)/etc/bash_completion
fi
```

将if...then...那一句添加到~/.bash_profile（如果没有该文件，新建一个）

重启终端，以上为安装bash-completion部分。

接下来将Git源码clone到本地

```shell
$ git clone https://github.com/git/git.git
```

找到"contrib/completion/"目录下的git-completion.bash，将该文件拷贝到~/下并重命名为.git-completion.bash

```shell
$ cp git-completion.bash ~/.git-completion.bash
```

在~/.bashrc文件（该目录下如果没有，新建一个）中添加下边的内容

```shell
source ~/.git-completion.bash
```

好了，重启终端以后就大功告成了

```shell
$ git --h[tab][tab] --help --html-path
```
