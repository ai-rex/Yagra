Yagra
=====
Yet Another GRAvatar

## 目录
* 安装使用说明
  * 系统需求
  * MySQL数据库
  * Apache配置
  * Yagra安装与配置
* 设计说明
  * 基本架构
  * 安全性

## 安装使用说明

### 系统需求
系统需要预先安装

* Python 2.7.3
* Apache 2.2.22
* MySQL 5.5.31
* mysql-python 1.2.3

### MySQL数据库
使用root帐号登录数据库，执行项目中的sql/init\_db.sql文件，建立相关数据库与表

    SOURCE /Yagra/sql/init_db.sql
创建新的用户名为yagra，密码为yagra的帐号

    CREATE USER 'yagra'@'localhost' IDENTIFIED BY 'yagra';
注：由于执行语句会被写入log，需要确保log的访问权限以防止密码泄漏。

选择mysql数据库，在db表中添加yagra账户的访问权限

    USE mysql
    INSERT INTO db SET Host='%', Db='Yagra', User='yagra', Select_priv='Y', Insert_priv='Y', Update_priv='Y', Delete_priv='Y';
重启mysql服务使得更改生效

    /etc/init.d/mysql restart

### Apache配置
假设用户放置网站的目录为/Yagra/web/，Apache的目录配置如下

    DocumentRoot /Yagra/web/
    <Directory /Yagra/web/>
        AllowOverride None

        RewriteEngine on
        RewriteRule ^avatar/([0-9a-f]{32})$ avatar.py?hashcode=$1
        RewriteRule ^([a-z]+)$ $1.py

        RewriteRule ^template static/404.html
        RewriteRule ^yag static/404.html

        ErrorDocument 404 /static/404.html

        AddHandler cgi-script .py
        Options -Indexes +ExecCGI -MultiViews -SymLinksIfOwnerMatch

        DirectoryIndex index.py

        Order allow,deny
        Allow from all
    </Directory>

Apache默认没有启用rewrite模块，使用以下命令启用

    cd /etc/apache2/mods-enabled
    ln -s ../mods-available/rewrite.load rewrite.load

重启Apache服务器以使得修改生效

    /etc/init.d/apache2 restart

注：如果条件允许，尽量启用SSL以防止网络监听窃取密码和COOKIE，提高安全性。

### Yagra安装与配置
假定网站目录为/Yagra/web，只需将项目目录中web文件夹中所有文件拷贝到/Yagra/web即可。

自定义数据库连接，可以修改项目目录中web/yag/db\_op.py文件中的如下设置

    _HOST = 'localhost'
    _USERNAME = 'yagra'
    _PASSWORD = 'yagra'
    _DATABASE = 'Yagra'
    _UNICODE = True
    _CHARSET = 'utf8'

自定义用户图片上传目录与自定义默认图片名称，修改web/yag/img.py，注意保存图片的目录需要apache帐户的写权限

    _SAVE_PATH = '/Yagra/upload/'
    _DEFAULT_IMG = '/Yagra/web/static/rex.jpeg'

在本机浏览器键入locahost即可看到首页。

## 设计说明

### 基本架构
用于公开访问的页面

    index.py  reg.py  login.py  logout.py  user.py  new.py  avatar.py

_index.py_
网站默认页，提供用户注册与登录入口。

_reg.py_
注册页面，注册要求用户名长度在4-32个字符，字符可以是字母或者数字，密码长度不少于6个字符，可以使用任意字符。

_login.py_
登录页面，输入注册时的用户名和密码即可登录，用户名不区分大小写。

_logout.py_
退出模块，执行即退出登录，并自动跳转到登录页面。

_user.py_
用户页面，显示用户头像和头像API链接，提供上传图片页面入口。

_new.py_
图片上传页面，接收图片数据并保存，根据图片数据判断图片类型，支持jpeg、gif、png、bmp和tiff图片格式。

_avatar.py_
图片API，根据用户名小写的MD5哈希值返回图片，若不存在则返回默认图片，自动判断图片类型并在返回HTTP头中注明。

若未登录访问需要登录访问的页面，将重定向到登录页面。

所有这些页面的模板文件对应的位于web/template文件夹中。

web/yag目录中的模块为网站页面HTTP输入输出、数据访问、IO安全性等提供支持

    auth.py  db_op.py  db.py  img.py  logger.py  page.py  sec.py

web/static目录保存了需要静态访问的错误页面、404页面和默认头像图片

    404.html  error.html  rex.jpeg

### 安全性
* 在服务器端需要安全的保存用户数据，数据库中的用户密码使用哈希密文保存，每个用户具备独立的盐，哈希算法为SHA256。

* 在用户端，浏览器的COOKIE只包含用户名与一串随机串TOKEN。

* 用户注册和登录时，往服务器传输的是明文密码，故需要SSL支持以提供额外的安全性。COOKIE虽然不包含明文密码，但SSL连接可增强安全性。

* 对任何用户提交数据进行严格检查，特别是SQL语句参数与页面显示部分，杜绝SQL注入攻击和XSS攻击。

* 对于不需要展示给用户的页面，重写URL跳转到404页面。

