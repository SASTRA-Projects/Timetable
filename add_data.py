import datetime

def add_campus(db_connector, cursor, /, *, id=None, campus=None):
	cursor.execute("""INSERT INTO `campuses` (`id`, `name`)
				   VALUES (%s, %s)""", (id, campus))
	db_connector.commit()

def add_school(db_connector, cursor, /, *, id=None, school=None, campus_id=None):
	cursor.execute("""INSERT INTO `schools` (`id`, `name`, `campus_id`)
				   VALUES (%s, %s, %s)""", (id, school, campus_id))
	db_connector.commit()


def add_building(db_connector, cursor, /, *, id=None, school_id=None, no_of_rooms=None):
	cursor.execute("""INSERT INTO `buildings` (`id`, `school_id`, `no_of_rooms`)
				   VALUES (%s, %s, %s)""", (id, school_id, no_of_rooms))
	db_connector.commit()

def add_department(db_connector, cursor, /, *, department=None):
	cursor.execute("""INSERT INTO `departments` (`name`)
				   VALUES (%s)""", (department,))
	db_connector.commit()

def add_degree(db_connector, cursor, /, *, degree=None, duration=None):
	cursor.execute("""INSERT INTO `degrees` (`name`, `duration`)
				   VALUES (%s, %s)""", (degree, duration))
	db_connector.commit()

def add_stream(db_connector, cursor, /, *, stream=None, department=None):
	cursor.execute("""INSERT INTO `streams` (`name`, `department`)
				   VALUES (%s, %s)""", (stream, department))
	db_connector.commit()

def add_programme(db_connector, cursor, /, *, id=None, degree=None, stream=None):
	cursor.execute("""INSERT INTO `programmes` (`id`, `degree`, `stream`)
				   VALUES (%s, %s, %s)""", (id, degree, stream))
	db_connector.commit()

def add_course(db_connector,
			   cursor, /, *,
			   code=None,
			   course=None,
			   department=None,
			   credits=None,
			   L=None,
			   P=None,
			   T=None,
			   is_elective=None):
	cursor.execute("""INSERT INTO `courses` (`code`, `name`,
											 `department`, `credits`,
											 `L`, `P`, `T`,
											 `is_elective`)
				
				   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
				   (code, course, department, credits, L, P, T, is_elective))
	db_connector.commit()

def add_campus_programme(db_connector, cursor, /, *, campus_id=None, programme_id=None):
	cursor.execute("""INSERT INTO `campus_programmes` (`campus_id`, `programme_id`)
				   VALUES (%s, %s)""", (campus_id, programme_id))
	db_connector.commit()

def add_school_department(db_connector, cursor, /, *, school_id=None, department=None):
	cursor.execute("""INSERT INTO `school_departments` (`school_id`, `department`)
				   VALUES (%s, %s)""", (school_id, department))
	db_connector.commit()

def add_programme_course(db_connector, cursor, /, *, programme_id=None, course_id=None):
	cursor.execute("""INSERT INTO `programme_courses` (`programme_id`, `course_id`)
				   VALUES (%s, %s)""", (programme_id, course_id))
	db_connector.commit()

def add_class(db_connector,
			  cursor, /, *,
			  id=None,
			  building_id=None,
			  duration=None,
			  room_no=None,
			  capacity=None,
			  is_lab=None):
	cursor.execute("""INSERT INTO `classes` (`id`, `building_id`,
											 `duration`, `room_no`,
											 `capacity`, `is_lab`)
				   VALUES (%s, %s, %s, %s, %s, %s)""", 
				   (id, building_id, duration, room_no, capacity, is_lab))
	db_connector.commit()

def add_section(db_connector,
				 cursor, /, *,
				 id=None,
				 degree=None,
				 stream=None,
				 section=None,
				 year=None):
	cursor.execute("""INSERT INTO `sections` (`id`, `degree`,
											 `stream`, `section`,
											 `year`, `is_lab`)
				   VALUES (%s, %s, %s, %s, %s, %s)""",
				   (id, building_id, duration, room_no, capacity, is_lab))
	db_connector.commit()

def add_faculty(db_connector,
				cursor, /, *,
				id=None,
				name=None,
				campus_id=None,
				department=None,
				join_year=datetime.date.today().year,
				phone=None):
	cursor.execute("""INSERT INTO `faculties` (`id`, `name`, `campus_id`,
											   `department`, `join_year`)
				   VALUES (%s, %s, %s, %s, %s)""",
				   (id, name, campus_id, department, join_year))
	db_connector.commit()

def add_student(db_connector,
				cursor, /, *,
				id=None,
				name=None,
				campus_id=None,
				join_year=datetime.date.today().year,
				programme_id=None,
				roll_no=None,
				phone=None):
	cursor.execute("""INSERT INTO `students` (`id`, `name`,
											  `campus_id`, `join_year`,
											  `programme_id`, `roll_no`,
											  `phone`)
				   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
				   (id, name, campus_id, department, join_year, phone))
	db_connector.commit()
