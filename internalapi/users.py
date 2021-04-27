from internalapi.methods import methods
from internalapi.cache import cache
from internalapi.response import Response
from internalapi.db import Cursor
from passlib.hash import pbkdf2_sha256 as hashing_algorithm
import datetime
class user:
    class userObject:
        def __init__(data):
            for item in data:
                exec(f'self.{item} = data[item]')
            self.json = data
    def fetch(id):
        prepare=f"SELECT `employ_id`,`password`,`email_verified`,`organisations`,`phone_verified` FROM `users` WHERE `employ_id`='{id}' LIMIT 1;"
        Cursor.execute(prepare)
        user_attr=Cursor.fetchall()
        employee_prepare=f"SELECT `name`,`email`,`phone`,`manager`,`country`,`city` FROM `employee` WHERE `employ_id`='{id}' LIMIT 1;"
        Cursor.execute(prepare)
        employee_attr=Cursor.fetchall()
        if len(user_attr)<1:
            return Response(202)
        user_attr=user_attr[0]
        employee_attr=employee_attr[0]
        data={
        'id':user_attr[0],
        'password':user_attr[1],
        'email_verified':user_attr[2],
        'organisations':user_attr[3],
        'phone_verified':user_attr[4],
        'name':employee_attr[0],
        'email':employee_attr[1],
        'phone':employee_attr[2],
        'manager':employee_attr[3],
        'country':employee_attr[4],
        'city':employee_attr[5]
        }
        return Response(100,userObject(data=data))
    def create(data):
        try:
            phone=data['phone']
            name=data['name']
            email=data['email']
            country=data['country']
            city=data['city']
            manager=data['manager']
        except KeyError:
            return Response(201)
        if cache.get('email',data['email']).success:
            return Response(200,"Email in use")
        elif phone!=None and cache.get('phone',phone).success:
            return Response(200,"Phone number in use")
        #password=methods.generateRandom(16)
        password="12345"
        password_hash=hashing_algorithm.hash(password)
        employ_id=methods.get_employ_id()
        cache.set('phone',phone,employ_id)
        cache.set('email',email,employ_id)    
        prepare=f"INSERT INTO `employee` (`employ_id`,`name`,`phone`,`email`,`country`,`city`) VALUES ('{employ_id}','{name}','{phone}','{email}','{country}','{city}')"
        Cursor.execute(prepare)
        prepare=f"INSERT INTO `users` (`employ_id`,`password`,`account_created`) VALUES ('{employ_id}','{password_hash}','{datetime.datetime.utcnow()}')"
        Cursor.execute(prepare)

        return Response(100,employ_id)

              