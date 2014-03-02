import re
import os
import hashlib
import binascii

__all__ = ['check_username', 'check_password', 'gen_salt', 'get_safe_password',
           'verify_password', 'gen_token', 'check_cookie', 'check_hashcode']

_MIN_USERNAME_LENGTH = 4
_MAX_USERNAME_LENGTH = 32
_MIN_PASSWORD_LENGTH = 6

def check_username(username):
    """Return True if the username is valid."""
    if isinstance(username, str):
        pattern = '^[0-9A-Za-z]{%d,%d}$' % (_MIN_USERNAME_LENGTH, 
                                            _MAX_USERNAME_LENGTH)
        if re.match(pattern, username):
            return True
    return False

def check_password(password):
    """Return True if the password is valid."""
    if isinstance(password, str):
        if len(password) >= _MIN_PASSWORD_LENGTH:
            return True
    return False

def gen_salt():
    """Return a true random binary string."""
    salt = os.urandom(32)
    return salt

def get_safe_password(password):
    """Generate a salt hashed password."""
    salt = gen_salt()
    return hashlib.sha256(password+salt).digest(), salt

def verify_password(safe_password, password, salt):
    """Return True if the input password is correct."""
    p = hashlib.sha256(password+salt).digest()
    if p == safe_password:
        return True
    else:
        return False

def gen_token():
    """Return a true random string."""
    token = os.urandom(16)
    return binascii.hexlify(token)

def check_cookie(cookie):
    """Return True if the cookie string is legal."""
    if isinstance(cookie, str):
        pattern = '^[0-9A-Za-z]{%d,%d}_[0-9a-f]{32}$' % (_MIN_USERNAME_LENGTH,
                                                         _MAX_USERNAME_LENGTH)
        if re.match(pattern, cookie):
            return True
    return False

def check_hashcode(hashcode):
    """Return True if the hash code is legal."""
    pattern = '^[0-9a-f]{32}$'
    if re.match(pattern, hashcode):
        return True
    return False

