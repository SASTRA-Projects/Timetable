from mysql import connector
from dotenv import load_dotenv
from os import getenv

load_dotenv()

db_connector = connector.connect(
	user="root", password=getenv("SASTRA_pwd"), host="localhost"
)
cursor = db_connector.cursor()

if not db_connector.is_connected():
	raise Exception("Database connection failed")

def close():
	cursor.close()
	db_connector.close()
	exit()

if __name__ == "__main__":
	close()
