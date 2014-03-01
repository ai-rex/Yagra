#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from yag import page
from yag import img

p = page.Page()

content_type = 'Content-type: image/%s'

use_default = True

def respond_image(page, filepath):
    with open(filepath) as f:
        data = f.read()
    page.add_header(content_type % img.get_type_by_stream(data))
    page.add(data)
    page.display()

hashcode = p.form.getvalue('hashcode')
if hashcode:
    filepath = img.get_image(hashcode)
    if filepath:
        respond_image(p, filepath)
        use_default = False
if use_default:
    respond_image(p, img.get_default())

