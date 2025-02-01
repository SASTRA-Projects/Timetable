from mysql_connector import cursor, close

def show_campuses():
	cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(campus):
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name`=%s)""", (campus,))
	return cursor.fetchone()

def show_schools(campus_id):
	cursor.execute("""SELECT * FROM `schools`
				   WHERE `campus_id`=%s""", (campus_id,))
	return cursor.fetchall()

def get_school_id(campus_id, school):
	cursor.execute("""SELECT `id` FROM `schools`
				   WHERE `name`=%s""", (campus_id, school))
	return cursor.fetchone()
