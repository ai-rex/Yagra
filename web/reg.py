#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import auth
from yag import logger

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

if 'REQUEST_METHOD' in p.env:
    method = p.env.get('REQUEST_METHOD').upper()
    if method == 'GET':
        p.add_file('template/reg.html')
    elif method == 'POST':
        form = p.form
        username = form.getvalue('username')
        password = form.getvalue('password')
        if not auth.exist_user(username):
            if auth.add_user(username, password):
                p.add_file('template/info.html', (u'注册成功！', 'login.py'))
            else:
                p.add_file('template/info.html', 
                           (u'不能使用空密码，或用户名已存在', 'reg.py'))
        else:
            p.add_file('template/info.html', 
                       (u'用户名不符合规范，或用户名已存在', 'reg.py'))
    else:
        p.redirect('static/error.html')
        logger.err(__name__, 'Request head method is %s' % (method))
else:
    p.redirect('static/error.html')
    logger.err(__name__, 'REQUEST_METHOD not in os.environ')

p.display()

