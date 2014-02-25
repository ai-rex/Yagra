#!/usr/bin/python

from yag import page
from yag import img

p = page.Page()

p.add_header('Content-type: image/jpeg')

use_default = True

if 'REQUEST_URI' in p.env:
    uri = p.env.get('REQUEST_URI')
    if uri:
        items = uri.split('/')
        l = len(items)
        if l >= 2:
            hashcode = items[l - 1]
            filepath = img.get_image(hashcode)
            if filepath:
                p.add_file(filepath)
                p.display()
                use_default = False
if use_default:
    p.add_file(img.get_default())
    p.display()

