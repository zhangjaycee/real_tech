# web server的配置





---
https://blog.csdn.net/aliveqf/article/details/70444387


## 用Python通过web页面分享本机文件夹[1]

* 可以选择配置一个简单的web服务器：
```bash
# 以8080端口创建一个简单服务器，默认会分享当前目录的文件供下载
python -m SimpleHTTPServer 8080
# 或python3：
python3 -m http.server 8080
```

* 也可以选择搭建一个简单ftp服务器：

```bash
python -m pyftpdlib
python -m pyftpdlib -w -d /**/ -u USERNAME -P PASSWORD
```

---
[1] https://blog.csdn.net/qq_41880069/article/details/88881748