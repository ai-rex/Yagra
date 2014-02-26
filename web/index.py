#!/usr/bin/python

from yag import page

p = page.Page()

p.add_header('Content-type: text/html; charset=utf8')

p.add_file('template/index.html')

p.display()

