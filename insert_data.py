from timetable import database

def insert_timetable(day, period_id, faculty_teaches_class_id):
	try:
		database.cursor.execute("""INSERT INTO `timetables`
					   			VALUES(%s, %s, %s)""", day, period_id, faculty_teaches_class_id)
		return True
	except database.errors.Error as error:
		database.db_connector.rollback()
		print(error)
		return False
