from typehints import *
import datetime

def add_campus(db_connector: Connection,
			   cursor: Cursor, /, *,
			   id: Optional[int] = None,
			   campus: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `campuses` (`id`, `name`)
				   VALUES (%s, %s)""", (id, campus))
	db_connector.commit()

def add_school(db_connector: Connection,
			   cursor: Cursor, /, *,
			   id: Optional[int] = None,
			   school: Optional[str] = None,
			   campus_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `schools` (`id`, `name`, `campus_id`)
				   VALUES (%s, %s, %s)""", (id, school, campus_id))
	db_connector.commit()

def add_building(db_connector: Connection,
				 cursor: Cursor, /, *,
				 id: Optional[int] = None,
				 school_id: Optional[int] = None,
				 no_of_rooms: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `buildings` (`id`, `school_id`, `no_of_rooms`)
				   VALUES (%s, %s, %s)""", (id, school_id, no_of_rooms))
	db_connector.commit()

def add_department(db_connector: Connection,
				   cursor: Cursor, /, *,
				   department: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `departments` (`name`)
				   VALUES (%s)""", (department,))
	db_connector.commit()

def add_degree(db_connector: Connection,
			   cursor: Cursor, /, *,
			   degree: Optional[str] = None,
			   duration: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `degrees` (`name`, `duration`)
				   VALUES (%s, %s)""", (degree, duration))
	db_connector.commit()

def add_stream(db_connector: Connection,
			   cursor: Cursor, /, *,
			   stream: Optional[str] = None,
			   department: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `streams` (`name`, `department`)
				   VALUES (%s, %s)""", (stream, department))
	db_connector.commit()

def add_programme(db_connector: Connection,
				  cursor: Cursor, /, *,
				  id: Optional[int] = None,
				  degree: Optional[str] = None,
				  stream: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `programmes` (`id`, `degree`, `stream`)
				   VALUES (%s, %s, %s)""", (id, degree, stream))
	db_connector.commit()

def add_course(db_connector: Connection,
			   cursor: Cursor, /, *,
			   code: Optional[str] = None,
			   course: Optional[str] = None,
			   department: Optional[str] = None,
			   credits: Optional[int] = None,
			   L: Optional[int] = None,
			   P: Optional[int] = None,
			   T: Optional[int] = None,
			   is_elective: bool = False) -> None:
	cursor.execute("""INSERT INTO `courses` (`code`, `name`,
											 `department`, `credits`,
											 `L`, `P`, `T`,
											 `is_elective`)
				
				   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
				   (code, course, department, credits, L, P, T, is_elective))
	db_connector.commit()

def add_campus_programme(db_connector: Connection,
						 cursor: Cursor, /, *,
						 campus_id: Optional[int] = None,
						 programme_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `campus_programmes` (`campus_id`, `programme_id`)
				   VALUES (%s, %s)""", (campus_id, programme_id))
	db_connector.commit()

def add_school_department(db_connector: Connection,
						  cursor: Cursor, /, *,
						  school_id: Optional[int] = None,
						  department: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `school_departments` (`school_id`, `department`)
				   VALUES (%s, %s)""", (school_id, department))
	db_connector.commit()

def add_programme_course(db_connector: Connection,
						 cursor: Cursor, /, *,
						 programme_id: Optional[int] = None,
						 course_id: Optional[int] = None) -> None:
	cursor.execute("""INSERT INTO `programme_courses` (`programme_id`, `course_id`)
				   VALUES (%s, %s)""", (programme_id, course_id))
	db_connector.commit()

def add_class(db_connector: Connection,
			  cursor: Cursor, /, *,
			  id: Optional[int] = None,
			  building_id: Optional[int] = None,
			  duration: Optional[int] = None,
			  room_no: Optional[int] = None,
			  capacity: Optional[int] = None,
			  is_lab: bool = False) -> None:
	cursor.execute("""INSERT INTO `classes` (`id`, `building_id`,
											 `duration`, `room_no`,
											 `capacity`, `is_lab`)
				   VALUES (%s, %s, %s, %s, %s, %s)""", 
				   (id, building_id, duration, room_no, capacity, is_lab))
	db_connector.commit()

def add_section(db_connector: Connection,
				cursor: Cursor, /, *,
				id: Optional[int] = None,
				campus_id: Optional[int] = None,
				degree: Optional[str] = None,
				stream: Optional[str] = None,
				section: Optional[str] = None,
				year: Optional[str] = None) -> None:
	cursor.execute("""INSERT INTO `sections` (`id`, `campus_id`,
											 `degree`, `stream`,
											 `section`, `year`)
				   VALUES (%s, %s, %s, %s, %s, %s)""",
				   (id, campus_id, degree, stream, section, year))
	db_connector.commit()

def add_faculty(db_connector: Connection,
				cursor: Cursor, /, *,
				id: Optional[int] = None,
				name: Optional[str] = None,
				campus_id: Optional[int] = None,
				department: Optional[str] = None,
				join_year: int = datetime.date.today().year) -> None:
	cursor.execute("""INSERT INTO `faculties` (`id`, `name`, `campus_id`,
											   `department`, `join_year`)
				   VALUES (%s, %s, %s, %s, %s)""",
				   (id, name, campus_id, department, join_year))
	db_connector.commit()

def add_student(db_connector: Connection,
				cursor: Cursor, /, *,
				id: Optional[int] = None,
				name: Optional[str] = None,
				campus_id: Optional[int] = None,
				join_year: int = datetime.date.today().year,
				programme_id: Optional[int] = None,
				roll_no: Optional[int] = None,
				phone: Optional[Union[int, str]] = None) -> None:
	cursor.execute("""INSERT INTO `students` (`id`, `name`,
											  `campus_id`, `join_year`,
											  `programme_id`, `roll_no`,
											  `phone`)
				   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
				   (id, name, campus_id, join_year, programme_id, roll_no, phone))
	db_connector.commit()
