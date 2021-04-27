import MySQLdb
from internalapi.db import Cursor
class methods:
    def is_int(item):
        try:
            item=int(item)
        except:
            return False
        else:
            return True
    def escape_mysql(item):
        return MySQLdb.escape_string(item)
    def get_employ_id():
        prepare="SELECT `employ_id` FROM `users` ORDER BY `employ_id` LIMIT 1"
        Cursor.execute(prepare)
        item=Cursor.fetchall()
        return int(item[0][0])+1
    def generateRandom(n):
        return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n))
    