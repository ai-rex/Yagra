import cgi
import cgitb
import Cookie
import sys
import os

__all__ = ['Page']

cgitb.enable()

class Page(object):
    def __init__(self):
        self.env = os.environ
        self.form = cgi.FieldStorage()
        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            self.http_cookie = Cookie.SimpleCookie()
            self.http_cookie.load(cookie_string)
        else:
            self.http_cookie = None

        self._headers = []
        self._content = []
        self.cookie = Cookie.SimpleCookie()

    def add_header(self, header):
        if header:
            self._headers.append(header)

    def add(self, content):
        self._content.append(content)

    def add_file(self, filename, params=None):
        if params:
            with open(filename, 'rb') as f:
                filedata = f.read().decode('utf8')
                filedata = filedata % params
                self._content.append(filedata.encode('utf8'))
        else:
            with open(filename, 'rb') as f:
                self._content.append(f.read())

    def redirect(self, url):
        self.add_header('Location: %s' % (url))

    def display(self):
        self.add_header(self.cookie.output())
        sys.stdout.write('\r\n'.join(self._headers) + '\r\n\r\n')
        sys.stdout.write(''.join(self._content))

