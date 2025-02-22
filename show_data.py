def get_campuses(cursor, /):
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

def get_school_name(cursor, /, *, id=None):
	cursor.execute("""SELECT `name` FROM `schools`
					WHERE `id`=%s)""", (id,))
	return cursor.fetchone()["name"]

def get_buildings(cursor, /, *, school_id=None):
	cursor.execute("""SELECT * FROM `buildings`
				   WHERE `school_id`=%s""", (school_id,))
	return cursor.fetchall()

def get_departments(cursor, /):
	cursor.execute("""SELECT * FROM `departments`""")
	return cursor.fetchall()

def get_departments_in_school(cursor, /, *, school_id=None):
	cursor.execute("""SELECT `department` FROM `school_departments`
				   WHERE `school_id`=%s""", (school_id,))
	return cursor.fetchall()

def get_schools_with_department(cursor, /, *, department=None):
	cursor.execute("""SELECT `school_id` FROM `school_departments`
				   WHERE `department`=%s""", (department,))
	return cursor.fetchall()

def get_degrees(cursor, /):
	cursor.execute("""SELECT * FROM `degrees`""")
	return cursor.fetchall()

def get_degree_duration(cursor, /, *, degree=None):
	cursor.execute("""SELECT `duartion` FROM `degrees`
				   WHERE `degree`=%s""", (degree,))
	return cursor.fetchone()["duartion"]

def get_streams(cursor, /):
	cursor.execute("""SELECT * FROM `streams`""")
	return cursor.fetchall()

def get_streams_under_department(cursor, /, *, department=None):
	cursor.execute("""SELECT `stream` FROM `school_streams`
				   WHERE `department`=%s""", (department,))
	return cursor.fetchall()

def get_programmes(cursor, /):
	cursor.execute("""SELECT * FROM `programmes`""")
	return cursor.fetchall()

def get_programmes_with_degree(cursor, /, *, degree=None):
	cursor.execute("""SELECT `programme` FROM `school_programmes`
				   WHERE `degree`=%s""", (degree,))
	return cursor.fetchall()

def get_programmes_with_stream(cursor, /, *, stream=None):
	cursor.execute("""SELECT `programme` FROM `school_programmes`
				   WHERE `stream`=%s""", (stream,))
	return cursor.fetchall()

def get_programmes_in_campus(cursor, /, *, campus_id=None):
	cursor.execute("""SELECT `programme` FROM `campus_programmes`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_campuses_with_programme(cursor, /, *, programme=None):
	cursor.execute("""SELECT `campus_id` FROM `campus_programmes`
				   WHERE `programme`=%s""", (programme,))
	return cursor.fetchall()
