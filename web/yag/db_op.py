import db

__all__ = ['add_user', 'get_user', 'add_auth', 'get_auth', 'del_auth',
           'add_image', 'get_image']

_HOST = 'localhost'
_USERNAME = 'yagra'
_PASSWORD = 'yagra'
_DATABASE = 'Yagra'
_UNICODE = True
_CHARSET = 'utf8'

def _database():
    # Get the Database instance.  
    if not globals().get('_d'):
        global _d
        _d = None
    if _d:
        return _d
    else:
        _d = db.Database(host=_HOST, user=_USERNAME, passwd=_PASSWORD,
                         db=_DATABASE, use_unicode=_UNICODE, charset=_CHARSET)
        return _d

def _run_sql(sql):
    # Execute a SQL string and return a tuple with data item(s) inside.  
    d = _database()
    return d.execute(sql)

def _escape_string(string):
    # Escape a string with special character(s).  
    d = _database()
    return d.escape_string(string)

def add_user(username, password, salt):
    """Add an user information to database and return True if succeed.  

    Keyword arguments:
    username -- the user name string
    password -- the user password hashed with salt
    salt -- the salt for hashing the user password
    """
    password = _escape_string(password)
    salt = _escape_string(salt)
    sql = "INSERT INTO User VALUES ('%s', '%s', '%s');" % (username, password,
                                                           salt)
    try:
        _run_sql(sql)
        return True
    except db.IntegrityError as e:
        return False

def get_user(username):
    """Get the user information by username string."""
    sql = "SELECT * FROM User WHERE username='%s';" % (username)
    return _run_sql(sql)

def add_auth(username, token):
    """Add the access token."""
    sql = "INSERT INTO Auth VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE \
           token='%s';" % (username, token, token)
    _run_sql(sql)

def get_auth(username):
    """Get the access token."""
    sql = "SELECT * FROM Auth WHERE username='%s';" % (username)
    return _run_sql(sql)

def del_auth(username):
    """Delete the access token."""
    sql = "DELETE FROM Auth where username='%s';" % (username)
    _run_sql(sql)

def get_image(hashcode):
    """Get the image file name by hashcode."""
    sql = "SELECT * FROM Image where hashcode='%s';" % (hashcode)
    return _run_sql(sql)

def add_image(hashcode, filename):
    """Save the image file name."""
    sql = "INSERT INTO Image VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE \
           filename='%s';" % (hashcode, filename, filename)
    _run_sql(sql)

