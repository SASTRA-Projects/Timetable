def add_campus(db_connector, cursor, campus):
	if len(campus) > 40:
		raise ValueError("Limit Error: Length exceeded!\nAllowed length is 40 bytes.")

	cursor.execute("""INSERT INTO `campuses` (`name`)
				   VALUES (%s)""", (campus,))
	db_connector.commit()

def add_school(db_connector, cursor, campus_id, school):
	cursor.execute("""INSERT INTO `schools` (`campus_id`, `name`)
				   VALUES (%s, %s)""", (campus_id, school))
	db_connector.commit()


def add_building(db_connector, cursor, school_id, no_of_rooms):
	cursor.execute("""INSERT INTO `buildings` (`school_id`, `no_of_rooms`)
				   VALUES (%s, %s)""", (school_id, no_of_rooms))
	db_connector.commit()
