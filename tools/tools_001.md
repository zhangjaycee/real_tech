# Vim 
## 实用操作
#### 折叠

> http://blog.sina.com.cn/s/blog_7acf472901017ad6.html

#### 查看路径
~~~
#查看当前文件的绝对路径 
`:pwd` (normal)
#查看当前文件的绝对路径+文件名 
`1<C-g>` (normal)
~~~
#### 自动补全 
~~~
`<C-p>` (insert)
~~~
#### 搜索不分大小写
~~~
#在模式前加\c，如：
/\chello (normall) 
#会搜出hello和Hello、HELLO......
~~~
#### 在一对匹配的符号之间跳转 
~~~
%
~~~
#### 搜索时的非贪婪匹配
直接用`*`进行匹配（查找或者替换）时，是贪婪模式的，要使用非贪婪匹配，用`\{-}`代替`*`。
### 配置方法
一般的配置文件在` ~/.vimrc`
插件`*.vim`一般都放在`~/.vim/`目录下
### 我使用的vim插件和工具
* The NERD tree (http://www.vim.org/scripts/script.php?script_id=1658)
* cscope
* taglist: https://www.vim.org/scripts/script.php?script_id=273
* Pathogen: https://github.com/tpope/vim-pathogen
* Mark: https://www.vim.org/scripts/script.php?script_id=2666

### 我的配置文件
~~~
set nu
set expandtab
set tabstop=4 " 设定 tab 长度为 4
set softtabstop=4 " 使得按退格键时可以一次删掉 4 个空格
set autoindent
set shiftwidth=4 " 设定 << 和 >> 命令移动时的宽度为 4
set hlsearch
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8
"set mouse=a
syntax on
set autochdir
set tags=tags;
set backspace=indent,eol,start
nnoremap <silent> <F2> :NERDTreeToggle<CR>
nnoremap <silent> <F3> :copen<CR>
nnoremap <silent> <F4> :cclose<CR>
nnoremap <silent> <C-y> :cclose<CR>
nnoremap <silent> <C-t> <C-o>
nnoremap <silent> <Down> :cclose<CR>
nnoremap <silent> <Up> :copen<CR>
nnoremap <silent> <Left> :NERDTreeToggle<CR>
nnoremap <silent> <Right> :TlistToggle<CR>
inoremap <silent> <C-h> <Left>
inoremap <silent> <C-j> <Down>
inoremap <silent> <C-k> <Up>
inoremap <silent> <C-l> <Right>
inoremap <silent> <C-w> <C-Right>
inoremap <silent> <C-b> <C-Left>
inoremap <silent> <C-a> <C-o>0
inoremap <silent> <C-e> <C-o>$
"自动加载cscope.out
if has("cscope")
	set csprg=/usr/local/bin/cscope
	set csto=0
	set cst
	set nocsverb
	" add any database in current directory
	if filereadable("cscope.out")
	    cs add cscope.out
	" else add database pointed to by environment
	elseif $CSCOPE_DB != ""
	    cs add $CSCOPE_DB
	endif
	set csverb
endif
"查找C代码符号
nmap <C-\>s :cs find s <C-R>=expand("<cword>")<CR><CR> 
"查找本定义
nmap <C-]> :cs find g <C-R>=expand("<cword>")<CR><CR> :copen<CR> 
"查找调用本函数的函数
nmap <C-\> :cs find c <C-R>=expand("<cword>")<CR><CR> :copen<CR> 
"查找本字符串
nmap <C-\>t :cs find t <C-R>=expand("<cword>")<CR><CR> :copen<CR> 
"查找本egrep模式
nmap <C-\>e :cs find e <C-R>=expand("<cword>")<CR><CR> 
"查找本文件
nmap <C-\>f :cs find f <C-R>=expand("<cfile>")<CR><CR> 
"查找包含本文件的文件
nmap <C-\>i :cs find i <C-R>=expand("<cfile>")<CR><CR> 
"找本函数调用的函数
nmap <C-\>d :cs find d <C-R>=expand("<cword>")<CR><CR> 
"cscope结果加入到quickfix list
set cscopequickfix=s-,c-,d-,g-,i-,t-,e-
"显示不可见的tab字符
"set list
"set listchars=tab:▸\
" Pathogen
execute pathogen#infect()
call pathogen#helptags() " generate helptags for everything in 'runtimepath'
syntax on
filetype plugin indent on
let Tlist_Use_Right_Window   = 1
~~~

## 在终端中启用vi模式

> https://sanctum.geek.nz/arabesque/vi-mode-in-bash/

在~/.inputrc中加入：
```
set editing-mode vi
```

或者在~/.bashrc中加入：
```
set -o vi
```

区别在于前者应用于所有终端输入，如bash、mysql交互，后者只用于bash

### 使用VIM编写Makefile时如何避免tab被扩展成4个空格
转自：http://blog.csdn.net/happen23/article/details/50680282

> 一般写代码的时候，都将tab键转换成4个空格（通过set expandtab命令）
不过，写Makefile的时候，tab有特殊含义——表明这行是规则，不是目标——不能转换成空格
但是执行set noexpandtab命令又麻烦，怎么办呢？
可以先敲ctrl-v组合键，再敲tab键，这样就不会被转换成空格了


## vim中如何贪婪匹配 [1]

```
vim中的匹配实在是不如perl好用，一直想实现非贪婪匹配，今天偶然发现可以用量词匹配来实现，具体可以看:h /\{
\{n,m} Matches n to m of the preceding atom, as many as possible
\{n} Matches n of the preceding atom
\{n,} Matches at least n of the preceding atom, as many as possible
\{,m} Matches 0 to m of the preceding atom, as many as possible
\{} Matches 0 or more of the preceding atom, as many as possible (like *)
\{-n,m} matches n to m of the preceding atom, as few as possible
\{-n} matches n of the preceding atom
\{-n,} matches at least n of the preceding atom, as few as possible
\{-,m} matches 0 to m of the preceding atom, as few as possible
\{-} matches 0 or more of the preceding atom, as few as possible
也就是.\{-}可以实现.*的非贪婪匹配，.\{-1,}可以实现.+的非贪婪匹配。
```

---

[1] http://blog.csdn.net/jiaolongdy/article/details/40588585

