from argon2 import PasswordHasher
from typehints import *
	"""Insert faculty information into the database"""
def insert_faculty_info(db_connector: Connection,
						cursor: Cursor, /, *,
						faculty_id: Optional[int] = None,
						phone: Optional[Union[int, str]] = None,
						salary: Optional[float] = None,
						password: Optional[str] = None) -> None:
	try:
		if not password:
<<<<<<< HEAD
			raise ValueError("Password is missing")
=======
			raise ValueError("Password is missing.")
>>>>>>> 886c1387824083f6d82a62c5d32fa7cc5d72551c
		ph: PasswordHasher = PasswordHasher()
		cursor.execute("""INSERT INTO `faculty_info`
					   VALUES (%s, %s, %s, %s)""",
					   (faculty_id, phone, salary, ph.hash(password)))
		del password
		del ph
		db_connector.commit()
	except Exception:
		del password
		del ph
		raise ValueError("Invalid ID or Password")

def add_section_class(db_connector: Connection,
					  cursor: Cursor, /, *,
					  id: Optional[int] = None,
					  section_id: Optional[int] = None,
					  class_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `section_class`
				   (`id`, `section_id`, `class_id`)
				   VALUES (%s, %s, %s)""", (id, section_id, class_id))
	db_connector.commit()

def add_student_section(db_connector: Connection,
						cursor: Cursor, /, *,
						section_id: Optional[int] = None,
						student_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `section_students`
				   (`section_id`, `student_id`)
				   VALUES (%s, %s)""", (section_id, student_id))
	db_connector.commit()

def add_faculty_section_course(db_connector: Connection,
						cursor: Cursor, /, *,
						id: Optional[int] = None,
						faculty_id: Optional[int] = None,
						section_id: Optional[int] = None,
						course_code: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `faculty_section_course`
				   (`id`, `faculty_id`, `section_id`, `course_code`)
				   VALUES (%s, %s, %s, %s)""",
				   (id, faculty_id, section_id, course_code))
	db_connector.commit()

def add_student_elective(db_connector: Connection,
						 cursor: Cursor, /, *,
						 student_id: Optional[int] = None,
						 course_code: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `student_electives`
				   (`student_id`, `course_code`)
				   VALUES (%s, %s)""", (student_id, course_code))
	db_connector.commit()

def insert_timetable(db_connector: Connection,
					 cursor: Cursor, /, *,
					 day: Optional[str] = None,
					 period_id: Optional[int] = None,
					 faculty_teaches_class_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `timetables`
				   VALUES(%s, %s, %s)""",
				   (day, period_id, faculty_teaches_class_id))
	db_connector.commit()
