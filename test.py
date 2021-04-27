import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()
mydb = mysql.connector.connect(
  host="localhost",
  user=os.getenv('db_user'),
  password=os.getenv('db_password'))

Cursor = mydb.cursor()
Cursor.execute(f"USE {os.getenv('db_name')}")
# Cursor.execute("""CREATE TABLE `users` (
# `employ_id` VARCHAR(10),
#  `user_id` VARCHAR(16),
# `password` VARCHAR(150) NOT NULL,
# `email_verified` BOOLEAN DEFAULT 0,
# `account_created` DATETIME NOT NULL,
# `sessions` VARCHAR(200) DEFAULT '[]',
# `organisations` VARCHAR(150) DEFAULT '[]',
#  PRIMARY KEY (user_id)
#  );""")
# Cursor.execute("""CREATE TABLE `employee` (
# `employ_id` VARCHAR(10),
# `name` VARCHAR(100) NOT NULL,
# `email` VARCHAR(100) NOT NULL,
# `phone` VARCHAR(16),
# `department` VARCHAR(200),
# `manager` VARCHAR(10),
# `country` VARCHAR(100),
# `city` VARCHAR(100)
# PRIMARY KEY (employ_id));""")
# Cursor.execute("""ALTER TABLE `users`
# ADD FOREIGN KEY (`employ_id`) REFERENCES employee(`employ_id`);""")
# Cursor.execute("""ALTER TABLE `employee`
# ADD FOREIGN KEY (`manager`) REFERENCES employee(`employ_id`);""")
# Cursor.execute("""CREATE TABLE `cache`(
#   `namespace` VARCHAR(50) NOT NULL,
#   `key` VARCHAR(500) NOT NULL,
#   `value` VARCHAR(500)
#   );""")