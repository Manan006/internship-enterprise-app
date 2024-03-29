from internalapi.db import Cursor
from internalapi.response import Response
from internalapi.db import db
from internalapi.methods import methods
from passlib.hash import pbkdf2_sha256 as hashing_algorithm
from  internalapi import communication
from internalapi.cache import cache
class organisations:
    class orgObject:
        def __init__(self,data):
                for item in data:
                    exec(f'self.{item} = data[item]')
                self.json = data
    def fetch(id):
        if methods.is_int(id):
            prepare=f"SELECT `name`,`phone`,`email`,`address`,`country`,`id` FROM `organisations` WHERE `id`=%s"            
        else:
            prepare=f"SELECT `name`,`phone`,`email`,`address`,`country`,`id` FROM `organisations` WHERE `name`=%s"            
        Cursor.execute(prepare,(id,))
        items=Cursor.fetchall()
        if len(items)<1:
            return Response(202)
        items=items[0]
        data={
                "name":items[0],
                "phone":items[1],
                "email":items[2],
                "address":items[3],
                "country":items[4],
                "id":items[5]
            }
        return Response(100,organisations.orgObject(data=data))
    def create(data):
        try:
            phone=data['phone']
            name=data['name']
            email=data['email']
            country=data['country']
            address=data['address']
            employ_name=data['employ_name']
            designation=data['designation']
            department=data['department']
            employ_id=data['employ_id']
        except KeyError:
            return Response(201)
        id=db.get_org_id()
        data={
        "name":employ_name,
        "email":email,
        "phone":phone,
        "city":address,
        "country":country,
        "manager":None,
        "organisation":id,
        "designation":designation,
        "admin":2,
        "department":department,
        "employ_id":employ_id
        }
        from internalapi.users import user        
        item=user.create(data=data)
        if not item.success:
            return item
        prepare=f"""INSERT INTO `organisations` (`id`,`name`,`phone`,`email`,`country`,`address`) 
        VALUES (%s,%s,%s,%s,%s,%s)"""
        Cursor.execute(prepare,(id,name,phone,email,country,address))

        return Response(100,organisations.fetch(id))
        