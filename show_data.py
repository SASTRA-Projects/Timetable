from typehints import *

def get_campuses(cursor, /) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(cursor, /, *, campus: Optional[str] = None) -> int:
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name` LIKE %s""", (campus,))
	return cursor.fetchone()["id"]

def get_campus_name(cursor, /, *, id: Optional[int] = None) -> str:
	cursor.execute("""SELECT `name` FROM `campuses`
					WHERE `id`=%s""", (id,))
	return cursor.fetchone()["name"]

def get_schools(cursor, /, *, campus_id: Optional[int] = None) -> Tuple[Optional[Dict[str, Union[int, str]]], ...]:
	cursor.execute("""SELECT `id`, `name` FROM `schools`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_school_id(cursor, /, *, campus_id: Optional[int] = None, school: Optional[str] = None) -> int:
	cursor.execute("""SELECT `id` FROM `schools`
				   WHERE `campus_id`=%s
				   AND `name`=%s""", (campus_id, school))
	return cursor.fetchone()["id"]

def get_school_name(cursor, /, *, id: Optional[int] = None) -> str:
	cursor.execute("""SELECT `name` FROM `schools`
					WHERE `id`=%s)""", (id,))
	return cursor.fetchone()["name"]

def get_buildings(cursor, /, *, school_id: Optional[int] = None) -> Tuple[Optional[Dict[str, int]], ...]:
	cursor.execute("""SELECT `id`, `no_of_rooms` FROM `buildings`
				   WHERE `school_id`=%s""", (school_id,))
	return cursor.fetchall()

def get_departments(cursor, /) -> Tuple[Optional[Dict[str, str]], ...]:
	cursor.execute("""SELECT * FROM `departments`""")
	return cursor.fetchall()

def get_departments_in_school(cursor, /, *, school_id: Optional[int] = None) -> Tuple[Optional[Dict[str, str]], ...]:
	cursor.execute("""SELECT `department` FROM `school_departments`
				   WHERE `school_id`=%s""", (school_id,))
	return cursor.fetchall()

def get_schools_with_department(cursor, /, *, department: Optional[str] = None):
	cursor.execute("""SELECT `school_id` FROM `school_departments`
				   WHERE `department` LIKE %s""", (department,))
	return cursor.fetchall()

def get_degrees(cursor, /):
	cursor.execute("""SELECT * FROM `degrees`""")
	return cursor.fetchall()

def get_degree_duration(cursor, /, *, degree: Optional[str] = None):
	cursor.execute("""SELECT `duartion` FROM `degrees`
				   WHERE `degree` LIKE %s""", (degree,))
	return cursor.fetchone()["duartion"]

def get_streams(cursor, /):
	cursor.execute("""SELECT * FROM `streams`""")
	return cursor.fetchall()

def get_streams_under_department(cursor, /, *, department: Optional[str] = None):
	cursor.execute("""SELECT `stream` FROM `school_streams`
				   WHERE `department` LIKE %s""", (department,))
	return cursor.fetchall()

def get_programmes(cursor, /):
	cursor.execute("""SELECT * FROM `programmes`""")
	return cursor.fetchall()

def get_programmes_with_degree(cursor, /, *, degree: Optional[str] = None):
	cursor.execute("""SELECT `programme` FROM `school_programmes`
				   WHERE `degree` LIKE %s""", (degree,))
	return cursor.fetchall()

def get_programmes_with_stream(cursor, /, *, stream: Optional[str] = None):
	cursor.execute("""SELECT `programme` FROM `school_programmes`
				   WHERE `stream` LIKE %s""", (stream,))
	return cursor.fetchall()

def get_programmes_in_campus(cursor, /, *, campus_id: Optional[int] = None):
	cursor.execute("""SELECT `programme` FROM `campus_programmes`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_campuses_with_programme_id(cursor, /, *, programme_id: Optional[int] = None):
	cursor.execute("""SELECT `campus_id` FROM `campus_programmes`
				   WHERE `programme_id`=%s""", (programme_id,))
	return cursor.fetchall()

def get_school_id(campus_id, school):
	cursor.execute("""SELECT `id` FROM `schools`
				   WHERE `name`=%s""", (campus_id, school))
	return cursor.fetchone()
