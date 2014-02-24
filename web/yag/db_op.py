import db

HOST = 'localhost'
USERNAME = 'yagra'
PASSWORD = 'yagra'
DATABASE = 'Yagra'
UNICODE = True
CHARSET = 'utf8'

def database():
    if not globals().get('_d'):
        _d = None
        global _d
    if _d:
        return _d
    else:
        _d = db.Database(host=HOST, user=USERNAME, passwd=PASSWORD, db=DATABASE,
                         use_unicode=UNICODE, charset=CHARSET)
        return _d

def run_sql(sql):
    d = database()
    return d.execute(sql)

def escape_string(string):
    d = database()
    return d.escape_string(string)

def add_user(username, password, salt):
    password = escape_string(password)
    salt = escape_string(salt)
    sql = "INSERT INTO User VALUES ('%s', '%s', '%s');" % (username, password,
                                                           salt)
    run_sql(sql)

def get_user(username):
    sql = "SELECT * FROM User WHERE username='%s';" % (username)
    return run_sql(sql)

def add_auth(username, token):
    sql = "INSERT INTO Auth VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE \
           token='%s';" % (username, token, token)
    run_sql(sql)

def get_auth(username):
    sql = "SELECT * FROM Auth WHERE username='%s';" % (username)
    return run_sql(sql)

def del_auth(username):
    sql = "DELETE FROM Auth where username='%s';" % (username)
    run_sql(sql)

def get_image(hashcode):
    sql = "SELECT * FROM Image where hashcode='%s';" % (hashcode)
    return run_sql(sql)

def add_image(hashcode, filename):
    sql = "INSERT INTO Image VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE \
           filename='%s';" % (hashcode, filename, filename)
    run_sql(sql)

