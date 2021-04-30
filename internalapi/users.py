from internalapi.methods import methods
from internalapi.cache import cache
from internalapi.response import Response
from internalapi.db import Cursor
from internalapi.db import db
from  internalapi import communication
from passlib.hash import pbkdf2_sha256 as hashing_algorithm
from internalapi.organisations import organisations
import datetime
class user:
    class userObject:
        def __init__(self,data):
            for item in data:
                exec(f'self.{item} = data[item]')
            self.json = data
        def edit(self,attr,value):
            attr=attr.lower()
            if attr not in ['password','email_verified','sessions','organisations','phone_verified','name','email','phone','manager','country','city','department','admin','employ_id']:
                return Response(200,"Invalid Attribute")
            Cursor.execute(f"SELECT EXISTS(SELECT `employ_id` FROM `users` WHERE `employ_id`='{self.id}')")
            if not Cursor.fetchall()[0][0]:
                return Response(202)
            prepare=f"UPDATE `users` SET `{attr}`='{value}' WHERE `id`='{self.id}'"
            try:
                Cursor.execute(prepare)
            except Exception as exception:
                return Response(200,exception)
            else:
                return (100)
        def is_admin(self):
            if self.adminstration>0:
                return True
            return False
        def is_owner(self):
            if self.adminstration>1:
                return True
            return False
        def delete(self):
            prepare=f"DELETE FROM `users` WHERE `id`='{self.id}' LIMIT 1"
            Cursor.execute(prepare)
            return Response(100)
    def fetch(id):
        prepare=f"SELECT `id`,`password`,`email_verified`,`organisation`,`phone_verified`,`account_created`,`sessions`,`designation`,`admin`,`name`,`email`,`phone`,`manager`,`country`,`city`,`department`,`employ_id` FROM `users` WHERE `id`='{id}' LIMIT 1;"
        Cursor.execute(prepare)
        data=Cursor.fetchall()
        if len(data)<1:
            return Response(202)
        data=data[0]
        data={
        'id':data[0],
        'password':data[1],
        'email_verified':data[2],
        'organisation':data[3],
        'phone_verified':data[4],
        'account_created':data[5],
        'sessions':methods.make_list(data[6]).content,
        'designation':data[7],        
        'admin':data[8],        
        'name':data[9],
        'email':data[10],
        'phone':data[11],
        'manager':data[12],
        'country':data[13],
        'city':data[14],
        'department':data[15],
        'employ_id':data[16]
        }
        return Response(100,user.userObject(data=data))
    def create(data):
        try:
            organisation=data['organisation']
            designation=data['designation']
            admin=data['admin']
            name=data['name']
            email=data['email']
            phone=data['phone']
            manager=data['manager']
            country=data['country']
            city=data['city']
            department=data['department']
            employ_id=data['employ_id']
        except KeyError:
            return Response(201)
        if cache.get('email',data['email']).success:
            return Response(200,"Email in use")
        elif phone!=None and cache.get('phone',phone).success:
            return Response(200,"Phone number in use")
        organisation=organisations.fetch(organisation)
        if not organisation.success:
            return Response(202,"Organisation not found")
        organisation=organisation.content
        password=methods.generateRandom(12)
        password_hash=hashing_algorithm.hash(password)
        id=db.get_user_id()
        employ_id=db.get_employ_id(organisation)
        prepare=f"""INSERT INTO `users` 
        (`id`,`password`,`account_created`,`organisation`,`designation`,`admin`,`employ_id`,`name`,`email`,`phone`,`department`,`manager`,`country`,`city`) 
        VALUES ('{id}','{password_hash}','{datetime.datetime.utcnow()}','{organisation.id}','{designation}','{admin}','{employ_id}','{name}','{email}','{phone}','{department}','{manager}','{country}','{city}')"""
        Cursor.execute(prepare)
        cache.set('phone',phone,id)
        cache.set('email',email,id)    
        employ=user.fetch(id).content
        communication.email.send_password(employ.email,password)
        return Response(100,employ)
