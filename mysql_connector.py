from mysql.connector import connect, errors
from dotenv import load_dotenv
from os import getenv

load_dotenv()

<<<<<<< HEAD
db_connector = connect(
	user="root", password=getenv("SASTRA_PWD"), host="localhost"
=======
db_connector = connector.connect(
	user="root", password=getenv("SASTRA_pwd"), host="localhost"
>>>>>>> 9ec0df21db46808944c299f096f1c9fdd15e3092
)

# db_connector = connect(user="root", ?, host="localhost")
if not db_connector.is_connected():
	raise Exception("Database connection failed")

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
