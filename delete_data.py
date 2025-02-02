from triggers import *

def delete_campus(campus):
	cursor.execute("""DELETE FROM `campuses`
				   WHERE `name`=%s""", (campus,))
	db_connector.commit()
