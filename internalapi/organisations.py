from internalapi.db import Cursor
from internalapi.response import Response
from internalapi.db import db
class organisations:
    class orgObject:
        def __init__(self,data):
                for item in data:
                    exec(f'self.{item} = data[item]')
                self.json = data
    def fetch(id):
        prepare=f"SELECT `name`,`phone`,`email`,`address`,`country` FROM `organisation` WHERE `id`='{id}'"
        Cursor.execute(prepare)
        items=Cursor.fetchall()
        if len(items)<1:
            return Response(202)
        data={
            "id":id
            "name":items[0],
            "phone":items[1],
            "email":items[2],
            "address":items[3],
            "country":items[4]
        }
        return Response(100,organisations.orgObject(data=data))
    def create(data):
        try:
            phone=data['phone']
            name=data['name']
            email=data['email']
            country=data['country']
            city=data['address']
        except KeyError:
            return Response(201)
        id=db.get_org_id()
        prepare=""
                