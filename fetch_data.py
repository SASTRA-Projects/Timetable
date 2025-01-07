from timetable import database

def break_periods(breaks=True):
	database.cursor.execute("""SELECT `id`, `start_time`, `end_time`
							FROM `periods`
							WHERE `is_break`=%s""", (breaks,))
	return database.cursor.fetchall()

def occupied_periods(class_id):
	database.cursor.execute("""SELECT `day`, `period_id`
						 	FROM `timetables`
						 	JOIN `faculty_teaches_class_id` `FTC`
						 	ON `FTC`.`id`=`timetables`.`faculty_teaches_class_id`
							WHERE `FTC`.`class_id`=%s""", (class_id,))
	return database.cursor.fetchall()

def all_periods():
	database.cursor.execute("""SELECT `days`.`day`, `periods`.`period_id`
						 	FROM `days`, `periods`""")
	return database.cursor.fetchall()

def available_periods(class_id):
	return list(set(all_periods()).difference(occupied_periods(class_id)))

def faculty_id(faculty_teaches_class_id):
	database.cursor.execute("""SELECT `faculty_id`
						 	FROM `faculty_teaches_class`
						 	WHERE `id`=%s""", (faculty_teaches_class_id,))
	return database.cursor.fetchone()

def faculty_department(faculty_id):
	database.cursor.execute("""SELECT `name`, `department`
						 	FROM `faculties`
						 	WHERE `id`=%s""", (faculty_id,))
	return database.cursor.fetchone()

def course_faculties(course_id):
	database.cursor.execute("""SELECT `FTC`.`faculty_id`
						 	FROM `faculty_teaches_class` `FTC`
							JOIN `section_course`
						 	ON `section_course`.`id`=`FTC`.`section_course_id`
							WHERE `section_course`.`course_id`=%s""", (course_id,))
	return database.cursor.fetchall()

def periods_split_up(course_id):
	database.cursor.execute("""SELECT `L`, `P`, `T`
					   		FROM `courses`
						 	WHERE `id`=%s""", (course_id,))
	return database.cursor.fetchone()
