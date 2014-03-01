#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import auth
from yag import sec
from yag import logger

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

T = 'template/reg.html'
T_INFO = 'template/info.html'
T_ERR = 'static/error.html'

RED_TEXT = u'<p class="text-danger">%s</p>'

if 'REQUEST_METHOD' in p.env:
    method = p.env.get('REQUEST_METHOD').upper()
    if method == 'GET':
        p.add_file(T, ('', ''))
    elif method == 'POST':
        form = p.form
        username = form.getvalue('username')
        password = form.getvalue('password')
        if sec.check_username(username):
            if sec.check_password(password):
                if not auth.exist_user(username):
                    if auth.add_user(username, password):
                        p.add_file(T_INFO, (u'注册成功！', 'login.py'))
                    else:
                        p.add_file(T, (RED_TEXT % u'用户名已存在', ''))
                else:
                    p.add_file(T, (RED_TEXT % u'用户名已存在', ''))
            else:
                p.add_file(T, ('', RED_TEXT % u'请输入足够长度的密码'))
        else:
            p.add_file(T, (RED_TEXT % u'请输入正确格式的用户名', ''))
    else:
        p.redirect(T_ERR)
        logger.err(__name__, 'Request head method is %s' % (method))
else:
    p.redirect(T_ERR)
    logger.err(__name__, 'REQUEST_METHOD not in os.environ')

p.display()

