from argon2 import PasswordHasher
from typehints import *

def insert_timetable(db_connector: Connection,
					 cursor: Cursor, /, *,
					 day: Optional[str] = None,
					 period_id: Optional[int] = None,
					 faculty_teaches_class_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `timetables`
				   VALUES(%s, %s, %s)""",
				   (day, period_id, faculty_teaches_class_id))
	db_connector.commit()

def insert_faculty_info(db_connector: Connection,
						cursor: Cursor, /, *,
						faculty_id: Optional[int] = None,
						phone: Optional[Union[int, str]] = None,
						salary: Optional[float] = None,
						password: Optional[str] = None) -> None:
	try:
		if not password:
			raise ValueError("Password is missing.")
		ph: PasswordHasher = PasswordHasher()
		cursor.execute("""INSERT INTO `faculty_info`
					   VALUES(%s, %s, %s, %s)""",
					   (faculty_id, phone, salary, ph.hash(password)))
		del password
		del ph
		db_connector.commit()
	except Exception:
		del password
		del ph
		raise ValueError("Invalid ID or Password")
