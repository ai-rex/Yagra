import hashlib

import sec
import db_op

__all__ = ['save_file', 'get_hashcode', 'get_default', 'get_image']

_SAVE_PATH = '/tmp/'
_DEFAULT_IMG = 'rex'

def save_file(data, username):
    filepath = _SAVE_PATH + username
    with open(filepath, 'wb') as f:
        f.write(data)
    db_op.add_image(get_hashcode(username), filepath)

def get_hashcode(username):
    return hashlib.md5(username).hexdigest()

def get_default():
    return _SAVE_PATH + _DEFAULT_IMG

def get_image(hashcode):
    if sec.check_hashcode(hashcode):
        images = db_op.get_image(hashcode)
        if len(images) == 1:
            filepath = images[0][1]
            return filepath
    return None

