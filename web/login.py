#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import auth

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

if 'REQUEST_METHOD' in p.env:
    method = p.env.get('REQUEST_METHOD').upper()
    if method == 'GET':
        if auth.cookie_auth(p.http_cookie):
            p.redirect('user.py')
        else:
            p.add_file('template/login.html')
    elif method == 'POST':
        form = p.form
        username = form.getvalue('username')
        password = form.getvalue('password')
        if auth.auth(username, password):
            auth.save_auth(username, p.cookie)
            p.redirect('user.py')
        else:
            p.add('username or password error')
    else:
        p.add('method error')
else:
    p.add('environ has no REQUEST_METHOD')

p.display()

