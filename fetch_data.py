# These algorithm needs verification

# def break_periods(cursor: Cursor, breaks=True):
# 	cursor.execute("""SELECT `id`, `start_time`, `end_time`
# 							FROM `periods`
# 							WHERE `is_break`=%s""", (breaks,))
# 	return cursor.fetchall()

# def occupied_periods(cursor: Cursor, class_id):
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

# def available_periods(cursor: Cursor, class_id):
# 	return list(set(all_periods()).difference(occupied_periods(class_id)))

# def faculty_department(cursor: Cursor, faculty_id):
# 	cursor.execute("""SELECT `name`, `department`
# 						 	FROM `faculties`
# 						 	WHERE `id`=%s""", (faculty_id,))
# 	return cursor.fetchone()

# def course_faculties(cursor: Cursor, course_id):
# 	cursor.execute("""SELECT `FTC`.`faculty_id`
# 						 	FROM `faculty_teaches_class` `FTC`
# 							JOIN `section_course`
# 						 	ON `section_course`.`id`=`FTC`.`section_course_id`
# 							WHERE `section_course`.`course_id`=%s""", (course_id,))
# 	return cursor.fetchall()

# def periods_split_up(cursor: Cursor, course_id):
# 	cursor.execute("""SELECT `L`, `P`, `T`
# 					   		FROM `courses`
# 						 	WHERE `id`=%s""", (course_id,))
# 	return cursor.fetchone()

from argon2 import PasswordHasher, exceptions
from typehints import *

def get_courses(cursor: Cursor, /, *,
                elective: Optional[bool] = None,
                lab: Optional[bool]) -> Tuple[Dict[str, Union[bool, int, str]], ...]:
    if elective is None and lab is None:
        cursor.execute("""SELECT * FROM `courses`""")
    elif lab is None:
        cursor.execute("""SELECT `code`, `name`,
                       `department`, `credits`,
                       `L`, `P`, `T` FROM `courses`
                       WHERE `is_elective`=%s""", (elective,))
    elif elective is None:
        if lab:
            cursor.execute("""SELECT * FROM `courses`
                           WHERE `P` > %s""", (0,))
        else:
            cursor.execute("""SELECT * FROM `courses`
                           WHERE `P`=%s""", (0,))
    else:
        if lab:
            cursor.execute("""SELECT `code`, `name`,
                           `department`, `credits`,
                           `L`, `P`, `T` FROM `courses`
                           WHERE `P` > %s
                           AND `is_elective`=%s""", (0, elective))
        else:
            cursor.execute("""SELECT `code`, `name`,
                           `department`, `credits`,
                           `L`, `P`, `T` FROM `courses`
                           WHERE `P`=%s
                           AND `is_elective`=%s""", (0, elective))
    return cursor.fetchall()

def get_course(cursor: Cursor, /, *,
               code: Optional[str] = None) -> Optional[Dict[str, Union[bool, int, str]]]:
    cursor.execute("""SELECT `name`, `department`,
                   `credits`, `L`, `P`, `T`,
                   `is_elective` FROM `courses`
                   WHERE `code`=%s""", (code,))
    return cursor.fetchone()

def get_classes(cursor: Cursor, /, *,
                building_id: Optional[int] = None,
                lab: Optional[bool] = None) -> Tuple[Dict[str, Union[bool, int]], ...]:
    if building_id:
        if lab is not None:
            cursor.execute("""SELECT `id`, `room_no`, `capacity`
                           FROM `classes`
                           WHERE `is_lab`=%s
                           AND `building_id`=%s""", (lab, building_id))
        else:
            cursor.execute("""SELECT `id`, `room_no`, `capacity`, `is_lab`
                           FROM `classes`
                           WHERE `building_id`=%s""", (building_id,))
    elif lab is not None:
        cursor.execute("""SELECT `id`, `building_id`, `room_no`, `capacity`
                       FROM `classes`
                       WHERE `is_lab`=%s""", (lab,))
    else:
        cursor.execute("""SELECT * FROM `classes`""")
    return cursor.fetchall()

def get_class(cursor: Cursor, /, *,
              class_id: Optional[int] = None) -> Optional[Dict[str, Union[bool, int]]]:
    cursor.execute("""SELECT `building_id`, `room_no`,
                   `capacity`, `is_lab`
                   FROM `classes`
                   WHERE `id`=%s""", (class_id,))
    return cursor.fetchone()

def get_sections(cursor: Cursor, /, *,
                 campus_id: Optional[int] = None,
                 degree: Optional[str] = None,
                 stream: Optional[str] = None,
                 year: Optional[int] = None) -> Tuple[Dict[str, Union[int, str]], ...]:
    if campus_id:
        if degree:
            if stream:
                if year:
                    cursor.execute("""SELECT `id`, `section`
                                   FROM `sections`
                                   WHERE `campus_id`=%s
                                   AND `degree`=%s
                                   AND `stream`=%s
                                   AND `year`=%s""",
                                   (campus_id, degree, stream, year))
                else:
                    cursor.execute("""SELECT `id`, `year`, `section`
                                   FROM `sections`
                                   WHERE `campus_id`=%s
                                   AND `degree`=%s
                                   AND `stream`=%s""",
                                   (campus_id, degree, stream))
            elif year:
                cursor.execute("""SELECT `id`, `stream`, `section`
                               FROM `sections`
                               WHERE `campus_id`=%s
                               AND `degree`=%s
                               AND `year`=%s""",
                               (campus_id, degree, year))
            else:
                cursor.execute("""SELECT `id`, `stream`, `year`, `section`
                               FROM `sections`
                               WHERE `campus_id`=%s
                               AND `degree`=%s""",
                               (campus_id, degree))
        elif stream:
            if year:
                cursor.execute("""SELECT `id`, `degree`, `section`
                               FROM `sections`
                               WHERE `campus_id`=%s
                               AND `stream`=%s
                               AND `year`=%s""",
                               (campus_id, stream, year))
            else:
                cursor.execute("""SELECT `id`, `degree`, `year`, `section`
                               FROM `sections`
                               WHERE `campus_id`=%s
                               AND `stream`=%s""",
                               (campus_id, stream))
        elif year:
            cursor.execute("""SELECT `id`, `degree`, `stream`, `section`
                           FROM `sections`
                           WHERE `campus_id`=%s
                           AND `year`=%s""",
                           (campus_id, year))
        else:
            cursor.execute("""SELECT `id`, `degree`,
                           `stream`, `year`, `section`
                           FROM `sections`
                           WHERE `campus_id`=%s""",
                           (campus_id,))
    elif degree:
        if stream:
            if year:
                cursor.execute("""SELECT `id`, `campus_id`, `section`
                               FROM `sections`
                               WHERE `degree`=%s
                               AND `stream`=%s
                               AND `year`=%s""",
                               (degree, stream, year))
            else:
                cursor.execute("""SELECT `id`, `campus_id`,
                               `year`, `section`
                               FROM `sections`
                               WHERE `degree`=%s
                               AND `stream`=%s""",
                               (degree, stream))
        elif year:
            cursor.execute("""SELECT `id`, `campus_id`,
                           `stream`, `section`
                           FROM `sections`
                           WHERE `degree`=%s
                           AND `year`=%s""",
                           (degree, year))
        else:
            cursor.execute("""SELECT `id`, `campus_id`,
                           `stream`, `year`, `section`
                           FROM `sections`
                           WHERE `degree`=%s""",
                           (degree,))
    elif stream:
        if year:
            cursor.execute("""SELECT `id`, `campus_id`,
                           `degree`, `section`
                           FROM `sections`
                           WHERE `stream`=%s
                           AND `year`=%s""",
                           (stream, year))
        else:
            cursor.execute("""SELECT `id`, `campus_id`,
                           `degree`, `year`, `section`
                           FROM `sections`
                           WHERE `stream`=%s""",
                           (stream,))
    elif year:
        cursor.execute("""SELECT `id`, `campus_id`,
                       `degree`, `stream`, `section`
                       FROM `sections`
                       WHERE `year`=%s""",
                       (year,))
    else:
        cursor.execute("""SELECT * FROM `sections`""")
    return cursor.fetchall()

def get_section(cursor: Cursor, /, *,
                section_id: Optional[int] = None) -> Optional[Dict[str, Union[bool, int]]]:
    cursor.execute("""SELECT `campus_id`, `degree`, `stream`,
                   `year`, `section`
                   FROM `sections`
                   WHERE `id`=%s""", (section_id,))
    return cursor.fetchone()

def get_section_id(cursor: Cursor, /, *,
                   campus_id: Optional[int] = None,
                   degree: Optional[str] = None,
                   stream: Optional[str] = None,
                   year: Optional[int] = None,
                   section: Optional[str] = None) -> Optional[int]:
    sections: Tuple[Dict[str, Union[int, str]], ...] = get_sections(cursor, campus_id=campus_id, degree=degree, stream=stream, year=year)
    if not (sections and campus_id and degree and stream and year and section):
        return None

    for s in sections:
        if s["section"] == section and isinstance(s["id"], int):
            return s["id"]
    return None

def get_faculties(cursor: Cursor, /, *,
                  campus_id: Optional[int] = None,
                  department: Optional[str] = None) -> Tuple[Dict[str, Union[int, str]], ...]:
    if campus_id:
        if department:
            cursor.execute("""SELECT `id`, `name`, `join_year`
                           FROM `faculties`
                           WHERE `campus_id`=%s
                           AND `department`=%s""", (campus_id, department))
        else:
            cursor.execute("""SELECT `id`, `name`, `department`, `join_year`
                           FROM `faculties`
                           WHERE `campus_id`=%s""", (campus_id,))
    elif department:
        cursor.execute("""SELECT  `id`, `name`, `campus_id`, `join_year`
                       FROM `faculties`
                       WHERE `department`=%s""", (department,))
    else:
        cursor.execute("""SELECT * FROM `faculties`""")
    return cursor.fetchall()

def get_faculty(cursor: Cursor, /, *,
                id: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
	cursor.execute("""SELECT `name` FROM `faculties`
				   WHERE `id`=%s""", (id,))
	return cursor.fetchone()

def faculty_id(cursor: Cursor, /, *,
               faculty_teaches_class_id: Optional[int] = None,
               campus_id: Optional[int] = None,
               department: Optional[str] = None,
               name: Optional[str] = None,
               join_year: Optional[int] = None) -> Tuple[Dict[str, int], ...]:
    if faculty_teaches_class_id:
        cursor.execute("""SELECT `id` AS faculty_id`
                       FROM `faculty_teaches_class`
                       WHERE `id`=%s""", (faculty_teaches_class_id,))
    elif campus_id and department and name and join_year:
        cursor.execute("""SELECT `id``
                       FROM `faculties`
                       WHERE `campus_id`=%s
                       AND `department`=%s
                       AND `name`=%s
                       AND `join_year`=%s""",
                       (campus_id, department, name, join_year))
    return cursor.fetchall()

def get_students(cursor: Cursor, /, *,
                 campus_id: Optional[int] = None,
                 programme_id: Optional[int] = None) -> Tuple[Dict[str, Union[int, str]], ...]:
    if campus_id:
        if programme_id:
            cursor.execute("""SELECT `id`, `name`, `join_year`, `phone`
                           FROM `students`
                           WHERE `campus_id`=%s
                           AND `programme_id`=%s""", (campus_id, programme_id))
        else:
            cursor.execute("""SELECT `id`, `name`, `programme_id`, `join_year`, `phone`
                           FROM `students`
                           WHERE `campus_id`=%s""", (campus_id,))
    elif programme_id:
        cursor.execute("""SELECT  `id`, `name`, `campus_id`, `join_year`, `phone`
                       FROM `students`
                       WHERE `programme_id`=%s""", (programme_id,))
    cursor.execute("""SELECT * FROM `students`""")
    return cursor.fetchall()

def get_student(cursor: Cursor, /, *,
                id: Optional[int] = None,
                campus_id=None,
                join_year=None,
                programme_id=None,
                roll_no: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
    if id:
        cursor.execute("""SELECT `name` FROM `students`
				       WHERE `id`=%s""", (id,))
    else:
    	cursor.execute("""SELECT `name` FROM `students`
                       WHERE `campus_id`=%s
                       AND `join_id`=%s
                       AND `programme_id`=%s
                       AND `roll_no`=%s""",
                       (campus_id, join_year, programme_id, roll_no))
    return cursor.fetchone()

def get_faculty_details(cursor: Cursor, /, *,
                        id: Optional[int] = None,
                        password: Optional[str] = None) -> Optional[Dict[str, Union[float, int, str]]]:
    try:
        cursor.execute("""SELECT * FROM `faculty_view`
                       WHERE `id`=%s""", (id,))
        faculty: Optional[Dict[str, Union[float, int, str]]] = cursor.fetchone()
        if faculty:
            pwd: Union[float, int, str] = faculty["password"]

        if isinstance(pwd, str) and password:
            ph: PasswordHasher = PasswordHasher()
            ph.verify(pwd, password)

    except exceptions.VerifyMismatchError:
        if faculty and isinstance(pwd, str):
            cursor.execute("""UPDATE `faculty_info`
                           SET `password`=%s""", ph.hash(pwd))
            raise AssertionError("Incorrect Password")
    return faculty

def get_student_details(cursor: Cursor, /, *, 
                        campus_id: Optional[int] = None,
                        join_year: Optional[int] = None,
                        programme_id: Optional[int] = None,
                        roll_no: Optional[int] = None) -> None:
    # TODO: ...
    ...
