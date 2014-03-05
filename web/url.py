#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib2

from yag import page
from yag import auth
from yag import img
from yag import logger

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

TEMPLATE = 'template/url.html'
RED = '<p class="text-danger">%s</p>'

auth_info = auth.cookie_auth(p.http_cookie)
if auth_info:
    if 'REQUEST_METHOD' in p.env:
        method = p.env.get('REQUEST_METHOD').upper()
        if method == 'GET':
            p.add_file(TEMPLATE, (' '))
        elif method == 'POST':
            form = p.form
            url = form.getvalue('url')
            if url:
                prefix = 'http://'
                if not url.startswith(prefix):
                    url = prefix + url
                try:                    
                    file_handle = urllib2.urlopen(url, timeout=3)
                    stream = file_handle.read()
                except IOError:
                    file_handle = None
                if file_handle:
                    username = auth_info[0]
                    _IMG_SUPPORTED = ['jpeg', 'gif', 'png', 'bmp', 'tiff']
                    if img.get_type_by_stream(stream) in _IMG_SUPPORTED:
                        img.save_file(stream, username)
                        p.redirect('user')
                    else:
                        p.add_file(TEMPLATE, (RED % u'不支持此图片文件类型'))
                else:
                    p.add_file(TEMPLATE, (RED % u'图片地址无效'))
            else:
                p.add_file(TEMPLATE, (RED % u'请输入图片地址'))
        else:
            p.redirect('static/error.html')
            logger.err(__name__, 'Request head method is %s' % (method))
    else:
        p.redirect('static/error.html')
        logger.err(__name__, 'REQUEST_METHOD not in os.environ')
else:
    p.redirect('login')

p.display()

