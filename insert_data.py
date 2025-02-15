from argon2 import PasswordHasher
import datetime
import os

def insert_timetable(db_connector, cursor, day, period_id, faculty_teaches_class_id):
	try:
		cursor.execute("""INSERT INTO `timetables`
					   VALUES(%s, %s, %s)""",
					   (day, period_id, faculty_teaches_class_id))
		db_connector.commit()
		return True
	except Exception as error:
		db_connector.rollback()
		return False

def insert_faculty_basic_info(db_connector, cursor, *, id, name, phone, campus_id, department, join_year=datetime.date.today().year):
	try:
		cursor.execute("""INSERT INTO `faculties`
				   VALUES(%s, %s, %s, %s, %s, %s)""",
				   (id, name, phone, join_year, campus_id, department))
		db_connector.commit()
		return True
	except Exception as error:
		db_connector.rollback()
		return False

def insert_faculty_info(db_connector, cursor, id, salary, __password):
	try:
		ph = PasswordHasher()
		cursor.execute("""INSERT INTO `faculty_info`
				   VALUES(%s, %s, %s)""",
				   (id, salary, ph.hash(__password)))
		del __password
		del ph
		db_connector.commit()
		return True
	except Exception as error:
		del __password
		del ph
		db_connector.rollback()
		return False
