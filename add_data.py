from mysql_connector import db_connector, cursor, close

def add_campus(campus):
	if len(campus) > 40:
		raise Exception("Limits Error: Length exceeded!")

	cursor.execute("""INSERT INTO `campuses` (`name`)
				   VALUES (%s)""", (campus,))
	db_connector.commit()

def add_school(campus_id, school):
	cursor.execute("""INSERT INTO `schools` (`campus_id`, `name`)
				   VALUES (%s, %s)""", (campus_id, school))
	db_connector.commit()


def add_building(school_id, no_of_rooms):
	cursor.execute("""INSERT INTO `buildings` (`school_id`, `no_of_rooms`)
				   VALUES (%s, %s)""", (school_id, no_of_rooms))
	db_connector.commit()
