#!/usr/bin/python

from yag import page
from yag import auth

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
                p.add('reg success')
            else:
                p.add('empty password or username has been used')
        else:
            p.add('invalid username or username has been used')
    else:
        p.add('method error')
else:
    p.add('environ has no REQUEST_METHOD')

p.display()

