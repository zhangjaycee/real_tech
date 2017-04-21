# tmux

## 0. 安装

* mac下：
```bash
brew install tmux
```

## 1. 配置

配置文件路径为`~/.tmux.conf`:

```
#前缀从Ctrl+b 换为Ctrl + a
set -g prefix C-a
unbind C-b

#copy-mode 将快捷键设置为vi 模式
setw -g mode-keys vi

#将pane切换按键和调整大小按键从方向键换为类似vim的hjkl键
bind-key k select-pane -U
bind-key j select-pane -D
bind-key h select-pane -L
bind-key l select-pane -R
bind -r ^k resizep -U 10
bind -r ^j resizep -D 10
bind -r ^h resizep -L 10
bind -r ^l resizep -R 10
```

## 2. 使用
这里`PREFIX` 默认为Ctrl+b， 我配置成了Ctrl+a

### 会话

* 创建新的会话：

(bash中）  tmux new -s NAME_OF_YOUR_SESSION



(在tmux中) `PREFIX` :new -s NAME_OF_YOUR_SESSION

* 离开当前会话

`PREFIX` d

* 重新链接会话

tmux a

tmux attach -t NAME_OF_YOUR_SESSION

* tmux中切换会话

`PREFIX` s

* 查看所有会话

(bash中) tmux ls


### 窗格(Pane)

* 横向分割出新Pane

`PREFIX` %

* 纵向分割出新Pane

`PREFIX` "

* Pane间切换

`PREFIX` h[,j,k,l]

* 调整Pane大小

`PREFIX` Ctrl+h[,j,k,l]

* 把一个Pane分出到一个新的窗口

`PREFIX` !

* 把一个Pane并到某个窗口

`PREFIX` :join-pane -t [optional session name]:<destination pane index>

e.g. 激活一个Pane的情况下把这个Pane移动到窗口0中：

`PREFIX` :join-pane -t :0


### 复制粘贴

1. `PREFIX` [ 进入复制模式

1. 空格键开始选择内容，由于配置了`setw -g mode-keys vi`，选取方式类似Vim的visual模式

1. 按回车复制选中模式并退出复制模式

1. `PREFIX` ] 粘贴


### 窗口(Window)

```
PREFIX c 创建一个新的窗口
PREFIX n 切换到下一个窗口
PREFIX p 切换到上一个窗口
PREFIX l 最后一个窗口,和上一个窗口的概念不一样哟,谁试谁知道
PREFIX w 通过上下键选择当前窗口中打开的会话
PREFIX 数字 直接跳到你按的数字所在的窗口
PREFIX & 退出当前窗口
PREFIX d 临时断开会话 断开以后,还可以连上的哟:)
PREFIX " 分割出来一个窗口
PREFIX % 分割出来一个窗口
PREFIX o 在小窗口中切换
PREFIX (方向键)
PREFIX ! 关闭所有小窗口
PREFIX x 关闭当前光标处的小窗口
PREFIX t 钟表
PREFIX pageup/pagedo
```


## 3. 我当前的配置文件

```
#~/.tmux.conf
#前缀从Ctrl+b 换为Ctrl + a
set -g prefix C-a
unbind C-b

#copy-mode 将快捷键设置为vi  模
setw -g mode-keys vi

#将pane切换按键和调整大小按键从方向键换为类似vim  hjklh
bind-key k select-pane -U
bind-key j select-pane -D
bind-key h select-pane -L
bind-key l select-pane -R
bind -r ^k resizep -U 10
bind -r ^j resizep -D 10
bind -r ^h resizep -L 10
bind -r ^l resizep -R 10

# 状态栏
  # 颜色
  set -g status-bg black
  set -g status-fg white

  # 对齐方式
  set-option -g status-justify centre

  # 左下角
  set-option -g status-left '#[bg=black,fg=green][#[fg=cyan]#S#[fg=green]]'
  set-option -g status-left-length 20

  # 窗口列表
  setw -g automatic-rename on
  set-window-option -g window-status-format '#[dim]#I:#[default]#W#[fg=grey,dim]'
  set-window-option -g window-status-current-format '#[fg=cyan,bold]#I#[fg=blue]:#[fg=cyan]#W#[fg=dim]'

  # 右下角
  set -g status-right '#[fg=green][#[fg=cyan]%Y-%m-%d#[fg=green]]'

```


## 4. 参考和扩展
> http://blog.jobbole.com/87584/
>
> http://blog.chinaunix.net/uid-26285146-id-3252286.html

