import re
import os
import hashlib
import binascii

MIN_USERNAME_LENGTH=4
MAX_USERNAME_LENGTH=32

def check_username(username):
    if isinstance(username, str):
        pattern = '^[0-9A-Za-z]{%d,%d}$' % (MIN_USERNAME_LENGTH, 
                                             MAX_USERNAME_LENGTH)
        if re.match(pattern, username):
            return True
    return False

def check_password(password):
    if isinstance(password, str):
        if len(password) > 0:
            return True
    return False

def gen_salt():
    salt = os.urandom(32)
    return salt

def get_safe_password(password):
    salt = gen_salt()
    return hashlib.sha256(password+salt).digest(), salt

def verify_password(safe_password, password, salt):
    p = hashlib.sha256(password+salt).digest()
    if p == safe_password:
        return True
    else:
        return False

def gen_token():
    token = os.urandom(16)
    return binascii.hexlify(token)

def check_cookie(cookie):
    if isinstance(cookie, str):
        pattern = '^[0-9A-Za-z]{%d,%d}_[0-9a-f]{32}$' % (MIN_USERNAME_LENGTH,
                                                         MAX_USERNAME_LENGTH)
        if re.match(pattern, cookie):
            return True
    return False

def check_hashcode(hashcode):
    pattern = '^[0-9a-f]{32}$'
    if re.match(pattern, hashcode):
        return True
    return False
