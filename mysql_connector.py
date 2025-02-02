import pymysql
from dotenv import load_dotenv
from os import getenv

load_dotenv()

timeout = 20
db_connector = pymysql.connect(
  charset=getenv("CHARSET"),
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  host=getenv("HOST"),
  password=getenv("PWD"),
  read_timeout=timeout,
  port=17216,
  user=getenv("USER"),
  write_timeout=timeout,
)

cursor = db_connector.cursor()
db_connector.autocommit = False

cursor.execute("""CREATE DATABASE IF NOT EXISTS `SASTRA`""")
cursor.execute("""USE `SASTRA`""")

def close():
	db_connector.commit()
	cursor.close()
	db_connector.close()
	exit()

if __name__ == "__main__":
	close()
