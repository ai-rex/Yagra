import hashlib
import imghdr

import sec
import db_op

__all__ = ['get_type_by_stream', 'save_file', 'get_hashcode', 'get_default',
           'get_image']

_SAVE_PATH = '/tmp/'
_DEFAULT_IMG = 'rex'

def get_type_by_stream(stream):
    """Check the data stream and return what type of image it is."""
    return imghdr.what('', stream)

def save_file(data, username):
    """Save the image data into file and record the file path."""
    filepath = _SAVE_PATH + username
    with open(filepath, 'wb') as f:
        f.write(data)
    db_op.add_image(get_hashcode(username), username)

def get_hashcode(username):
    """Return MD5 hex digest of the lower case input string."""
    return hashlib.md5(username.lower()).hexdigest()

def get_default():
    """Return the file path of the default image."""
    return _SAVE_PATH + _DEFAULT_IMG

def get_image(hashcode):
    """Get the image file path by hash code."""
    if sec.check_hashcode(hashcode):
        images = db_op.get_image(hashcode)
        if len(images) == 1:
            filename = images[0][1]
            return _SAVE_PATH + filename
    return None

