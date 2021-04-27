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