from mysql_connector import cursor, close

def show_campuses():
	cursor.execute("""SELECT * FROM `campuses`""")
	return cursor.fetchall()

def get_campus_id(campus):
	cursor.execute("""SELECT `id` FROM `campuses`
				   WHERE `name`=?)""", (campus,))
	campus_id = cursor.fetchone()
	return campus_id

def show_blocks(campus_id):
	cursor.execute("""SELECT * FROM `blocks`
				   WHERE `campus_id`=?""", (campus_id,))
	return cursor.fetchall()
