#!/usr/bin/python

from yag import page
from yag import auth

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

if 'REQUEST_METHOD' in p.env:
    method = p.env.get('REQUEST_METHOD').upper()
    if method == 'GET':
        auth_info = auth.cookie_auth(p.http_cookie)
        if auth_info:
            auth.del_auth(auth_info[0])
        p.redirect('login.py')
    else:
        p.add('method error')
else:
    p.add('environ has no REQUEST_METHOD')

p.display()

