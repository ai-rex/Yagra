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
            p.add_file('template/new.html', (' '))
        elif method == 'POST':
            form = p.form
            fileitem = form['filename']
            if fileitem.filename:
                username = auth_info[0]
                stream = fileitem.file.read()
                _IMG_SUPPORTED = ['jpeg', 'gif', 'png', 'bmp', 'tiff']
                if img.get_type_by_stream(stream) in _IMG_SUPPORTED:
                    img.save_file(stream, username)
                    p.redirect('user')
                else:
                    p.add_file(
                        'template/new.html',
                        (u'<p class="text-danger">请上传支持的图片文件</p>')
                    )
            else:
                p.add_file('template/new.html',
                           (u'<p class="text-danger">请选择一个文件</p>'))
        else:
            p.redirect('static/error.html')
            logger.err(__name__, 'Request head method is %s' % (method))
    else:
        p.redirect('static/error.html')
        logger.err(__name__, 'REQUEST_METHOD not in os.environ')
else:
    p.redirect('login')

p.display()

