## Jc的常用Git命令记录
>
1. [创建仓库](#创建仓库)
1. [提交更改](#提交更改)
1. [分支管理](#分支管理)
1. [撤销与回退](#撤销与回退)

## 创建仓库
**git init** 创建仓库

**git clone** *xxx.git(远程库的地址)* 克隆一个远程仓库

**git remote** add origin *xxx.git(远程库的地址)* 指定一个远程仓库地址，命名为origin

## 提交更改
**git rm** *file_name* 删除文件

**git add** *file_name*  添加文件到仓库暂存区(index)

**git commit -m** "xxx" 提交更改给仓库

**git commit -am** "xxx" 上两条的终极合体，添加所有已追踪文件的更改到暂存区，并提交
**git log** 显示提交日志

**git status** 显示当前仓库状态

**git push [-f]** [*remote_name*] [*branch_name*]  上传到远程仓库,加-f表示强制覆盖远程仓库的上传(要谨慎)

**git pull** [*remote_name*] [*branch_name*] 从远程拉取最新内容到指定分支

## 分支管理
**git branch** 查看本地分支

**git branch -r** 查看远程分支

**git branch** *branch_name*  本地创建新分支

**git branch -d** *branch_name* 删除指定分支

**git push** origin  :*branch-name* 删除远程指定分支，注意冒号前有个空格

**git checkout** *branch_name*  切换分支

**git checkout -b** *branch_name*  上两条的合体，创建新分支并切换至这个新分支

**git merge** *branch_name* 将指定分支合并到当前所在的分支

## 撤销与回退
**git checkout HEAD** *file_name*  丢弃对某文件工的修改，把文件恢复到最后一次commit状态（修改了暂存区和工作区）

**git reset [--mixed] HEAD[~n]** [*file_name*]回退到HEAD所指的提交(只修改了暂存区，不修改工作区)

**git reset --hard HEAD[~n]** [*file_name*] 回退到HEAD所指的提交(暂存区和工作区都修改)

**git reset --soft HEAD[~n]** [*file_name*]回退到HEAD所指的提交(不修改暂存区和工作区)

## bash提示符显示仓库状态

```bash
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

export PS1="\[\033[01;35m\]\u@\h\[\033[01;35m\] \W\[\033[00m\]\[\033[33m\]\$(parse_git_branch)\[\033[00m\] \[\033[01;35m\]$\[\033[01;00m\]  \[\e[m\]"
```

