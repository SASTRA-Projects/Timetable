# These algorithm needs verification

# def break_periods(cursor, breaks=True):
# 	cursor.execute("""SELECT `id`, `start_time`, `end_time`
# 							FROM `periods`
# 							WHERE `is_break`=%s""", (breaks,))
# 	return cursor.fetchall()

# def occupied_periods(cursor, class_id):
# 	cursor.execute("""SELECT `day`, `period_id`
# 						 	FROM `timetables`
# 						 	JOIN `faculty_teaches_class_id` `FTC`
# 						 	ON `FTC`.`id`=`timetables`.`faculty_teaches_class_id`
# 							WHERE `FTC`.`class_id`=%s""", (class_id,))
# 	return cursor.fetchall()

# def all_periods(cursor):
# 	cursor.execute("""SELECT `days`.`day`, `periods`.`period_id`
# 						 	FROM `days`, `periods`""")
# 	return cursor.fetchall()

# def available_periods(cursor, class_id):
# 	return list(set(all_periods()).difference(occupied_periods(class_id)))

# def faculty_id(cursor, faculty_teaches_class_id):
# 	cursor.execute("""SELECT `faculty_id`
# 						 	FROM `faculty_teaches_class`
# 						 	WHERE `id`=%s""", (faculty_teaches_class_id,))
# 	return cursor.fetchone()

# def faculty_department(cursor, faculty_id):
# 	cursor.execute("""SELECT `name`, `department`
# 						 	FROM `faculties`
# 						 	WHERE `id`=%s""", (faculty_id,))
# 	return cursor.fetchone()

# def course_faculties(cursor, course_id):
# 	cursor.execute("""SELECT `FTC`.`faculty_id`
# 						 	FROM `faculty_teaches_class` `FTC`
# 							JOIN `section_course`
# 						 	ON `section_course`.`id`=`FTC`.`section_course_id`
# 							WHERE `section_course`.`course_id`=%s""", (course_id,))
# 	return cursor.fetchall()

# def periods_split_up(cursor, course_id):
# 	cursor.execute("""SELECT `L`, `P`, `T`
# 					   		FROM `courses`
# 						 	WHERE `id`=%s""", (course_id,))
# 	return cursor.fetchone()

from argon2 import PasswordHasher, exceptions

def get_courses(cursor, /):
    cursor.execute("""SELECT * FROM `courses`""")
    return cursor.fetchall()

def get_course(cursor, /, *, code=None):
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `code`=%s""", (code,))
    course = cursor.fetchone()
    course.pop("code", None)
    return course

def get_elective_courses(cursor, /):
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `is_elective`=%s""", (True,))
    return cursor.fetchall()

def get_nonelective_courses(cursor, /):
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `is_elective`=%s""", (False,))
    return cursor.fetchall()

def get_courses_with_lab(cursor, /):
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `P` > %s""", (0,))
    return cursor.fetchall()

def get_courses_without_lab(cursor, /):
    cursor.execute("""SELECT * FROM `courses`
                   WHERE `P`=%s""", (0,))
    return cursor.fetchall()

def get_classes(cursor, /):
    cursor.execute("""SELECT * FROM `classes`""")
    return cursor.fetchall()

def get_class(cursor, /, building_id=None):
    cursor.execute("""SELECT * FROM `classes`
                   WHERE `building_id`=%s""", (building_id,))
    classes = cursor.fetchall()
    for _class in classes:
        _class.pop("building_id", None)
    return classes

def get_lab_classes(cursor, /):
    cursor.execute("""SELECT * FROM `classes`
                   WHERE `is_lab`=%s""", (True,))
    return cursor.fetchall()

def get_non_lab_classes(cursor, /):
    cursor.execute("""SELECT * FROM `classes`
                   WHERE `is_lab`=%s""", (False,))
    return cursor.fetchall()

def get_faculties(cursor, /):
	cursor.execute("""SELECT * FROM `faculties`""")
	return cursor.fetchall()

def get_faculty(cursor, /, *, id=None):
	cursor.execute("""SELECT `name` FROM `faculties`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def get_students(cursor, /):
	cursor.execute("""SELECT * FROM `students`""")
	return cursor.fetchall()

def get_student(cursor, /, *, id=None):
	cursor.execute("""SELECT `name` FROM `students`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def get_student_by_details(cursor, /, *,
                           campus_id=None,
                           join_year=None,
                           programme_id=None,
                           roll_no=None):
	cursor.execute("""SELECT `name` FROM `students`
				   WHERE `campus_id`=%s
                   AND `join_id`=%s
                   AND `programme_id`=%s
                   AND `roll_no`=%s""",
                   (campus_id, join_year, programme_id, roll_no))
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

def get_student_details(cursor, /, *, 
                        campus_id=None,
                        join_year=None,
                        programme_id=None,
                        roll_no=None):
    pass
