def show_campuses(cursor):
	cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(cursor, campus):
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name`=%s)""", (campus,))
	return cursor.fetchone()

def show_schools(cursor, campus_id):
	cursor.execute("""SELECT * FROM `schools`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_school_id(cursor, campus_id, school):
	cursor.execute("""SELECT `id` FROM `schools`
				   WHERE `name`=%s""", (campus_id, school))
	return cursor.fetchone()
