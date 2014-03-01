#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import auth
from yag import img
from yag import logger

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

auth_info = auth.cookie_auth(p.http_cookie)
if auth_info:
    if 'REQUEST_METHOD' in p.env:
        method = p.env.get('REQUEST_METHOD').upper()
        if method == 'GET':
            username = auth_info[0]
            image_path = 'avatar.py/%s' % (img.get_hashcode(username))
            p.add_file('template/user.html', (image_path, username, image_path))
        else:
            p.redirect('static/error.html')
            logger.err(__name__, 'Request head method is %s' % (method))
    else:
        p.redirect('static/error.html')
        logger.err(__name__, 'REQUEST_METHOD not in os.environ')
else:
    p.redirect('login.py')

p.display()

