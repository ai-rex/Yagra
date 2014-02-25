#!/usr/bin/python

from yag import page
from yag import auth
from yag import img

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

auth_info = auth.cookie_auth(p.http_cookie)
if auth_info:
    if 'REQUEST_METHOD' in p.env:
        method = p.env.get('REQUEST_METHOD').upper()
        if method == 'GET':
            username = auth_info[0]
            image_path = 'avatar.py/%s' % (img.get_hashcode(username))
            p.add_file('template/user.html', (username, image_path, 
                                                  image_path))
        elif method == 'POST':
            form = p.form
            fileitem = form['filename']
            if fileitem.filename:
                username = auth_info[0]
                img.save_file(fileitem.file.read(), username)
                p.add('The file was uploaded successfully')
            else:
                p.add('No file was uploaded')
        else:
            p.add('method error')
    else:
        p.add('environ has no REQUEST_METHOD')
else:
    p.redirect('login.py')

p.display()

