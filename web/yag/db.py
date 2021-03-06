import MySQLdb
from  _mysql_exceptions import IntegrityError

__all__ = ['Database']

class Database(object):
    """Simplified interface for accessing MySQLdb."""
    def __init__(self, **kwargs):
        self.connection = MySQLdb.connect(**kwargs)
        self.connection.autocommit(True)

    def execute(self, sql):
        """Execute a SQL string and return a tuple."""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def escape_string(self, string):
        """Escape string with special character(s)."""
        return MySQLdb.escape_string(string)

if __name__ == '__main__':
    db = Database(host='localhost', user='yagra', passwd='yagra', db='Yagra',
                  use_unicode=True, charset='utf8')
    print db.execute("insert into User values( \
                          'yagra', \
                          '0123456789abcdef0123456789abcdef', \
                          '0123456789abcdef0123456789abcdef' \
                      );")
    print db.execute('select * from User limit 3;')
        
