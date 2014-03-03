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
    INSERT INTO db SET Db='Yagra', User='yagra', Select_priv='Y', Insert_priv='Y', Update_priv='Y', Delete_priv='Y';
重启mysql服务使得更改生效

    /etc/init.d/mysql restart


