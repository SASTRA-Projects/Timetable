from argon2 import PasswordHasher
import datetime

def insert_faculty_basic_info(db_connector,
							  cursor, /, *,
							  id=None,
							  name=None,
							  campus_id=None,
							  department=None,
							  join_year=datetime.date.today().year,
							  phone=None,):
	cursor.execute("""INSERT INTO `faculties`
				   VALUES(%s, %s, %s, %s, %s, %s)""",
				   (id, name, campus_id, department, join_year, phone))
	db_connector.commit()

def insert_student_basic_info(db_connector,
							  cursor, /, *,
							  id=None,
							  name=None,
							  campus_id=None,
							  join_year=datetime.date.today().year,
							  programme_id=None,
							  roll_no=None,
							  phone=None):
	cursor.execute("""INSERT INTO `students`
				   VALUES(%s, %s, %s, %s, %s, %s, %s)""",
				   (id, name, campus_id, join_year, programme_id, roll_no, phone))
	db_connector.commit()

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
