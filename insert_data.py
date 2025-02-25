from argon2 import PasswordHasher

def insert_timetable(db_connector, cursor, /, *, day=None, period_id=None, faculty_teaches_class_id=None):
	cursor.execute("""INSERT INTO `timetables`
				   VALUES(%s, %s, %s)""",
				   (day, period_id, faculty_teaches_class_id))
	db_connector.commit()

def insert_faculty_info(db_connector, cursor, /, *, id=None, salary=None, __password=None):
	try:
		ph = PasswordHasher()
		cursor.execute("""INSERT INTO `faculty_info`
				   VALUES(%s, %s, %s)""",
				   (id, salary, ph.hash(__password)))
		del __password
		del ph
	except Exception:
		del __password
		del ph
		raise ValueError("Invalid ID or Password")
