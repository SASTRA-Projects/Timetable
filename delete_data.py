from triggers import *

def delete_campus(campus):
	database.cursor.execute("""DELETE FROM `campuses`
				   WHERE `name`=%s""", (campus,))
	database.db_connector.commit()
