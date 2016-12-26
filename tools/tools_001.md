## Vim 
### 实用操作
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
### 配置方法
一般的配置文件在 ~/.vimrc
插件*.vim一般在~/.vim/目录下
### 我使用的vim插件和工具
* The NERD tree (http://www.vim.org/scripts/script.php?script_id=1658)
* cscope

### 我的配置文件
~~~
set nu
set expandtab
set tabstop=4
set softtabstop=4
set autoindent
set hlsearch
set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936
set termencoding=utf-8
set encoding=utf-8
set mouse=a
syntax on
set autochdir
set tags=tags;
set backspace=indent,eol,start
nnoremap <silent> <F2> :NERDTreeToggle<CR>
nnoremap <silent> <F3> :copen<CR>
nnoremap <silent> <F4> :cclose<CR>
nnoremap <silent> <C-y> :cclose<CR>
nnoremap <silent> <C-t> <C-o>
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
~~~

