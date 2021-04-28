import MySQLdb
from internalapi.db import Cursor
from internalapi.response import Response
from passlib.hash import pbkdf2_sha256 as hashing_algorithm
import random

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
    def make_list(item):
        try:
            return Response(100,eval(item))
        except Exception as exception:
            return Response(200,exception)
    def verify_password(password,hash):
        return Response(hashing_algorithm.verify(password,hash))
      
    