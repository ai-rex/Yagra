import sec
import db_op

def exist_user(username):
    if sec.check_username(username):
        user = db_op.get_user(username)
        if len(user) > 0:
            return True
    return False

def add_user(username, password):
    if sec.check_username(username) and sec.check_password(password):
        safe_password, salt = sec.get_safe_password(password)
        if db_op.add_user(username, safe_password, salt):
            return True
    return False

def auth(username, password):
    if sec.check_username(username) and sec.check_password(password):
        users = db_op.get_user(username)
        if len(users) == 1:
            user = users[0]
            safe_password = user[1]
            salt = user[2]
            if sec.verify_password(safe_password, password, salt):
                return True
    return False

def save_auth(username, cookie):
    token = sec.gen_token()
    cookie_string = username + '_' + token
    cookie['token'] = cookie_string
    db_op.add_auth(username, token)

def cookie_auth(http_cookie):
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
    db_op.del_auth(username)

