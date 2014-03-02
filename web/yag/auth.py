import sec
import db_op

__all__ = ['exist_user', 'add_user', 'auth', 'save_auth', 'cookie_auth',
           'del_auth']

def exist_user(username):
    """Return True if username exists."""
    if sec.check_username(username):
        users = db_op.get_user(username)
        if len(users) > 0:
            return True
    return False

def add_user(username, password):
    """Add a new user and return True if succeed."""
    if sec.check_username(username) and sec.check_password(password):
        safe_password, salt = sec.get_safe_password(password)
        if db_op.add_user(username, safe_password, salt):
            return True
    return False

def auth(username, password):
    """Reurn the username registered while giving the right password."""
    if sec.check_username(username) and sec.check_password(password):
        users = db_op.get_user(username)
        if len(users) == 1:
            user = users[0]
            reg_username = user[0]
            safe_password = user[1]
            salt = user[2]
            if sec.verify_password(safe_password, password, salt):
                return reg_username
    return None

def save_auth(username, cookie):
    """Save the access token to cookie."""
    token = sec.gen_token()
    cookie_string = username + '_' + token
    cookie['token'] = cookie_string
    db_op.add_auth(username, token)

def cookie_auth(http_cookie):
    """Return a tuple while giving the cookie with right token."""
    if http_cookie:
        cookie_string = http_cookie.get('token').value
        if cookie_string and sec.check_cookie(cookie_string):
            username, token = cookie_string.split('_')
            auths = db_op.get_auth(username)
            if len(auths) == 1:
                auth = auths[0]
                if (username, token) == auth:
                    return auth
    return None

def del_auth(username):
    """Remove the access token saved by username"""
    db_op.del_auth(username)

