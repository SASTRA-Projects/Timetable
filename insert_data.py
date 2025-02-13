def insert_timetable(db_connector, cursor, day, period_id, faculty_teaches_class_id):
	try:
		cursor.execute("""INSERT INTO `timetables`
					   			VALUES(%s, %s, %s)""", day, period_id, faculty_teaches_class_id)
		db_connector.commit()
		return True
	except Exception as error:
		db_connector.rollback()
		print(error)
		return False
