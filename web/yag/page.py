import cgi
import cgitb
import Cookie
import sys
import os

cgitb.enable()

class Page(object):
    def __init__(self):
        self.env = os.environ

        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            self.http_cookie = Cookie.SimpleCookie()
            self.http_cookie.load(cookie_string)
        else:
            self.http_cookie = None

        self.form = cgi.FieldStorage()        

        self.cookie = Cookie.SimpleCookie()
        self._headers = ""
        self._content = ""

    def add_header(self, header):
        if header:
            self._headers += header + '\r\n'

    def add(self, content):
        self._content += content

    def add_file(self, filename):
        with open(filename) as f:
            self._content += f.read()

    def display(self):
        self.add_header(self.cookie.output())
        sys.stdout.write(self._headers + '\r\n')
        sys.stdout.write(self._content)

