import cgi
import cgitb
import Cookie
import sys
import os

__all__ = ['Page']

cgitb.enable()

class Page(object):
    """Inferface for handling http request and http response.

    Contains:
    env -- os.environ
    form -- cgi.FieldStorage()
    http_cookie -- HTTP request cookie saved in Cookie.SimpleCookie instance.  
    cookie -- Cookie.SimpleCookie instance for setting cookie.
    """
    def __init__(self):
        # Input attributes
        self.env = os.environ
        self.form = cgi.FieldStorage()
        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            self.http_cookie = Cookie.SimpleCookie()
            self.http_cookie.load(cookie_string)
        else:
            self.http_cookie = None

        # Output attributes
        self._headers = []
        self._content = []
        self.cookie = Cookie.SimpleCookie()

    def add_header(self, header):
        """Add a HTTP response header."""
        if header:
            self._headers.append(header)

    def add(self, content):
        """Add a string to the response."""
        self._content.append(content)

    def add_file(self, filename, params=None):
        """Read a file and add the content string to the response."""
        if params:
            with open(filename, 'rb') as f:
                filedata = f.read().decode('utf8')
                filedata = filedata % params
                self._content.append(filedata.encode('utf8'))
        else:
            with open(filename, 'rb') as f:
                self._content.append(f.read())

    def redirect(self, url):
        """Redirect to url."""
        self.add_header('Location: %s' % (url))

    def display(self):
        """Write all the data back and finish the HTTP response."""
        self.add_header(self.cookie.output())
        sys.stdout.write('\r\n'.join(self._headers) + '\r\n\r\n')
        sys.stdout.write(''.join(self._content))

