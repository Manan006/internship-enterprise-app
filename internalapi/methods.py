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
    def generateRandom(n):
        return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwzyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(n))
    def make_list(item):
        try:
            return Response(100,eval(item))
        except Exception as exception:
            return Response(200,exception)
    def verify_password(password,hash):
        return Response(100,hashing_algorithm.verify(password,hash))
    