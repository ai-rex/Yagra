import re
import os
import hashlib

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

def get_salt():
    salt = os.urandom(32)
    return salt

def get_safe_password(password):
    salt = get_salt()
    return hashlib.sha256(password+salt).digest(), salt
    

