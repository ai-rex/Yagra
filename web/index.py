#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import auth

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

if auth.cookie_auth(p.http_cookie):
    p.redirect('user')
else:
    p.add_file('template/index.html')

p.display()

