import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('db_user'),
  password=os.getenv('db_password'),
  autocommit=True)

mydb.cursor().execute(f"USE {os.getenv('db_name')}")
Cursor = mydb.cursor()

class db:
  def get_employ_id():
    prepare="SELECT `employ_id` FROM `users` ORDER BY `employ_id` LIMIT 1"
    Cursor.execute(prepare)
    item=Cursor.fetchall()
    if len(item)>0:
        return int(item[0][0])+1
    else:
        return 1
  def get_org_id():
    prepare="SELECT `employ_id` FROM `organsations` ORDER BY `id` LIMIT 1"
    Cursor.execute(prepare)
    item=Cursor.fetchall()
    if len(item)>0:
        return int(item[0][0])+1
    else:
        return 1