from mysql_connector import db_connector, cursor, close

def add_campus(campus):
	if len(campus) > 40:
		raise Exception("Limits Error: Length exceeded!")

	cursor.execute("""INSERT INTO `campuses` (`name`)
				   VALUES (%s)""", (campus,))
	db_connector.commit()

def add_block(block, campus_id):
	cursor.execute("""INSERT INTO `blocks` (`name`, `campus_id`)
				   VALUES (%s, %s)""", (block, campus_id))
	db_connector.commit()
