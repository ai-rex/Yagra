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
        if auth.cookie_auth(p.http_cookie):
            p.redirect('user')
        else:
            p.add_file('template/login.html')
    elif method == 'POST':
        form = p.form
        username = form.getvalue('username')
        password = form.getvalue('password')
        reg_username = auth.auth(username, password)
        if reg_username:
            auth.save_auth(reg_username, p.cookie)
            p.redirect('user')
        else:
            p.add_file('template/info.html', (u'用户名或密码错误', 'login'))
    else:
        p.redirect('static/error.html')
        logger.err(__name__, 'Request head method is %s' % (method))
else:
    p.redirect('static/error.html')
    logger.err(__name__, 'REQUEST_METHOD not in os.environ')

p.display()

