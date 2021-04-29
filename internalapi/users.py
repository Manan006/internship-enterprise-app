from internalapi.methods import methods
from internalapi.cache import cache
from internalapi.response import Response
from internalapi.db import Cursor
from internalapi.db import db
from  internalapi import communication
from passlib.hash import pbkdf2_sha256 as hashing_algorithm
import datetime
class user:
    class userObject:
        def __init__(self,data):
            for item in data:
                exec(f'self.{item} = data[item]')
            self.json = data
        def edit(self,attr,value):
            attr=attr.lower()
            if attr in ['password','email_verified','organisations','phone_verified']:
                table="users"
            elif attr in ['name','email','phone','manager','country','city']:
                table="employee"
            else:
                return Response(200,"Invalid Attribute")
            Cursor.execute(f"SELECT EXISTS(SELECT `employ_id` FROM `users` WHERE `employ_id`='{self.id}')")
            if not Cursor.fetchall()[0][0]:
                return Response(202)
            prepare=f"UPDATE `{table}` SET `{attr}`='{value}' WHERE `employ_id`='{self.id}'"
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

    def fetch(id):
        user_prepare=f"SELECT `employ_id`,`password`,`email_verified`,`organisation`,`phone_verified`,`account_created`,`sessions`,`designation`,`admin` FROM `users` WHERE `employ_id`='{id}' LIMIT 1;"
        Cursor.execute(user_prepare)
        user_attr=Cursor.fetchall()
        employee_prepare=f"SELECT `name`,`email`,`phone`,`manager`,`country`,`city`,`department` FROM `employee` WHERE `employ_id`='{id}' LIMIT 1;"
        Cursor.execute(employee_prepare)
        employee_attr=Cursor.fetchall()
        if len(user_attr)<1:
            return Response(202)
        user_attr=user_attr[0]
        employee_attr=employee_attr[0]
        data={
        'id':user_attr[0],
        'password':user_attr[1],
        'email_verified':user_attr[2],
        'organisation':user_attr[3],
        'phone_verified':user_attr[4],
        'name':employee_attr[0],
        'email':employee_attr[1],
        'phone':employee_attr[2],
        'manager':employee_attr[3],
        'country':employee_attr[4],
        'city':employee_attr[5],
        'sessions':methods.make_list(user_attr[6]).content,
        'account_created':user_attr[5],
        'department':user_attr[6],
        'designation':user_attr[7],        
        'adminstration':user_attr[8]        
        }
        return Response(100,user.userObject(data=data))
    def create(data):
        try:
            phone=data['phone']
            name=data['name']
            email=data['email']
            country=data['country']
            city=data['city']
            manager=data['manager']
            organisation=data['organisation']
            designation=data['designation']
            admin=data['admin']
        except KeyError:
            return Response(201)
        if cache.get('email',data['email']).success:
            return Response(200,"Email in use")
        elif phone!=None and cache.get('phone',phone).success:
            return Response(200,"Phone number in use")
        password=methods.generateRandom(12)
        password_hash=hashing_algorithm.hash(password)
        employ_id=db.get_employ_id()
        cache.set('phone',phone,employ_id)
        cache.set('email',email,employ_id)    
        prepare=f"INSERT INTO `employee` (`employ_id`,`name`,`phone`,`email`,`country`,`city`) VALUES ('{employ_id}','{name}','{phone}','{email}','{country}','{city}')"
        Cursor.execute(prepare)
        prepare=f"INSERT INTO `users` (`employ_id`,`password`,`account_created`) VALUES ('{employ_id}','{password_hash}','{datetime.datetime.utcnow()}')"
        Cursor.execute(prepare)
        employ=user.fetch(employ_id).content
        #verify.email.sendVerifyEmail(employ)
        communication.email.send_password(employ.email,password)
        return Response(100,employ)
