from argon2 import PasswordHasher, exceptions

def get_campuses(cursor):
	cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(cursor, /, *, campus=None):
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name`=%s""", (campus,))
	return cursor.fetchone()["id"]

def get_campus_name(cursor, /, *, id=None):
	cursor.execute("""SELECT `name` FROM `campuses`
					WHERE `id`=%s""", (id,))
	return cursor.fetchone()["name"]

def get_schools(cursor, /, *, campus_id=None):
	cursor.execute("""SELECT * FROM `schools`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_school_id(cursor, /, *, campus_id=None, school=None):
	cursor.execute("""SELECT `id` FROM `schools`
				   WHERE `name`=%s""", (campus_id, school))
	return cursor.fetchone()["id"]

def get_school_name(cursor, /, *, school_id=None):
	cursor.execute("""SELECT `name` FROM `schools`
					WHERE `id`=%s)""", (id,))
	return cursor.fetchone()["name"]

def get_faculty_basic_infos(cursor):
	cursor.execute("""SELECT * FROM `faculties`""")
	return cursor.fetchall()

def get_faculty_name(cursor, /, *, id):
	cursor.execute("""SELECT `name`
				   FROM `faculties`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def get_faculty_details(cursor, /, *, id=None, password=None):
	try:
		cursor.execute("""SELECT * FROM `faculty_view`
					   WHERE `id`=%s""", (id,))
		faculty = cursor.fetchone()
		ph = PasswordHasher()
		ph.verify(faculty["password"], password)
	except exceptions.VerifyMismatchError:
		if ph.check_needs_rehash(faculty["password"]):
			cursor.execute("""UPDATE `faculty_info`
						   SET `password`=%s""", ph.hash(password))
		del faculty["password"]
		del ph
		raise AssertionError("Incorrect Password")
	del faculty["password"]
	del password
	del ph
	return faculty
