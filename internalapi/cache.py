from internalapi.response import Response
from internalapi.db import Cursor
from internalapi.users import user
class cache:
    def set(namespace, key, value):
        prepare=f"INSERT INTO `cache` (`namespace`,`key`,`value`) VALUES ('{namespace}','{key}','{value}');"
        Cursor.execute(prepare)
        return Response(100)

    def get(namespace, key):
        prepare=f"SELECT `value` FROM `cache` WHERE `namespace`='{namespace}' AND `key`='{key}';"
        Cursor.execute(prepare)
        value=Cursor.fetchall()
        print(len(value))
        if len(value)<1:
            return Response(202)
        value=value[0][0]
        user.fetch(value).content
        return Response(100,value)
    def remove(namespace, key):
        prepare=f"DELETE FROM `cache` WHERE `namespace`='{namespace}' AND `key`='{key}';"
        Cursor.execute(prepare)
        return Response(100)
