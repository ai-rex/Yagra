import hashlib

import sec
import db_op

SAVE_PATH = '/tmp/'
DEFAULT_IMG = 'rex'

def save_file(data, username):
    filepath = SAVE_PATH + username
    with open(filepath, 'wb') as f:
        f.write(data)
    db_op.add_image(get_hashcode(username), filepath)

def get_hashcode(username):
    return hashlib.md5(username).hexdigest()

def get_default():
    return SAVE_PATH + DEFAULT_IMG

def get_image(hashcode):
    if sec.check_hashcode(hashcode):
        images = db_op.get_image(hashcode)
        if len(images) == 1:
            filepath = images[0][1]
            return filepath
    return None

