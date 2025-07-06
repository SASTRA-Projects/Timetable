from argon2 import PasswordHasher, exceptions
from typehints import *
import show_data
import csv

def get_courses(cursor: Cursor, /, *,
                programme_id: Optional[int] = None,
                elective: Optional[bool] = None,
                lab: Optional[bool] = None) -> Tuple[Dict[str, Union[bool, int, str]], ...]:
    if programme_id:
        if elective is None and lab is None:
            cursor.execute("""SELECT `code`, `name`,
                           `department`, `credits`,
                           `L`, `P`, `T`, `is_elective`
                           FROM `courses`
                           JOIN `programme_courses`
                           ON `code`=`course_code`
                           AND `programme_id`=%s""", (programme_id,))
        elif lab is None:
            cursor.execute("""SELECT `code`, `name`,
                           `department`, `credits`,
                           `L`, `P`, `T`
                           FROM `courses`
                           JOIN `programme_courses`
                           ON `code`=`course_code`
                           AND `programme_id`=%s
                           AND `is_elective`=%s""", (programme_id, elective,))
        elif elective is None:
            cursor.execute("""SELECT *
                           FROM `courses`
                           JOIN `programme_courses`
                           ON `code`=`course_code`
                           AND `programme_id`=%s
                           AND `P` > %s
                           AND `P` < %s""", ((programme_id,) + ((0, 256) if lab else (-1, 1))))
        else:
            cursor.execute("""SELECT `code`, `name`,
                           `department`, `credits`,
                           `L`, `P`, `T`
                           FROM `courses`
                           JOIN `programme_courses`
                           ON `code`=`course_code`
                           AND `programme_id`=%s
                           AND `P` > %s
                           AND `P` < %s
                           AND `is_elective`=%s""", ((programme_id,) + ((0, 256) if lab else (-1, 1)) + (elective,)))
    else:
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
        elif lab:
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

def get_programme_courses(cursor: Cursor, /, *,
                          campus_id: Optional[int] = None,
                          programme_id: Optional[int] = None,
                          course_code: Optional[str] = None) -> Union[Tuple[Dict[str, Union[str, int]]], bool]:
    if campus_id:
        if programme_id:
            if course_code:
                cursor.execute("""SELECT 1
                               FROM `programme_courses` `PC`
                               JOIN `programmes`
                               ON `programmes`.`id`=`PC`.`programme_id`
                               AND `campus_id`=%s
                               AND `programme_id`=%s
                               AND `course_code`=%s
                               LIMIT 1""",
                               (campus_id, programme_id, course_code))
                return True if cursor.fetchone() else False
            else:
                cursor.execute("""SELECT `course_code`
                               FROM `programme_courses` `PC`
                               JOIN `programmes`
                               ON `programmes`.`id`=`PC`.`programme_id`
                               AND `campus_id`=%s
                               AND `programme_id`=%s""",
                               (campus_id, programme_id))
        elif course_code:
            cursor.execute("""SELECT `programme_id`
                           FROM `programme_courses` `PC`
                           JOIN `programmes`
                           ON `programmes`.`id`=`PC`.`programme_id`
                           AND `campus_id`=%s
                           AND `course_code`=%s""",
                           (campus_id, course_code))
        else:
            cursor.execute("""SELECT `programme_id`, `course_code`
                           FROM `programme_courses` `PC`
                           JOIN `programmes`
                           ON `programmes`.`id`=`PC`.`programme_id`
                           AND `campus_id`=%s""",
                           (campus_id,))
    elif programme_id:
        if course_code:
            cursor.execute("""SELECT 1
                          FROM `programme_courses`
                          AND `programme_id`=%s
                          AND `course_code`=%s
                          LIMIT 1""",
                          (programme_id, course_code))
            return True if cursor.fetchone() else False
        else:
            cursor.execute("""SELECT `course_code`
                           FROM `programme_courses`
                           WHERE `programme_id`=%s""", (programme_id,))
    elif course_code:
        cursor.execute("""SELECT `programme_id`
                       FROM `programme_courses`
                       WHERE `course_code`=%s""", (course_code,))
    else:
        cursor.execute("""SELECT * FROM `programme_courses`""")
    return cursor.fetchall()

def get_classes(cursor: Cursor, /, *,
                campus_id: Optional[int] = None,
                building_id: Optional[int] = None,
                lab: Optional[bool] = None,
                department: Optional[str] = None) -> Tuple[Dict[str, Union[bool, int]], ...]:
    if building_id:
        if lab is not None:
            if department:
                cursor.execute("""SELECT `id`, `room_no`, `capacity`
                               FROM `classes`
                               WHERE `is_lab`=%s
                               AND `building_id`=%s
                               AND `department`=%s""",
                               (lab, building_id, department))
            else:
                cursor.execute("""SELECT `id`, `room_no`, `capacity`, `department`
                               FROM `classes`
                               WHERE `is_lab`=%s
                               AND `building_id`=%s""",
                               (lab, building_id))
        else:
            cursor.execute("""SELECT `id`, `room_no`, `capacity`, `is_lab`
                           FROM `classes`
                           WHERE `building_id`=%s""", (building_id,))
    elif campus_id:
        if lab is not None:
            if department:
                cursor.execute("""SELECT `id`, `room_no`, `capacity`
                               FROM `classes`
                               NATURAL JOIN `campus_buildings`
                               WHERE `is_lab`=%s
                               AND `campus_id`=%s
                               AND `department`=%s""",
                               (lab, campus_id, department))
            else:
                cursor.execute("""SELECT `id`, `room_no`, `capacity`, `department`
                               FROM `classes`
                               NATURAL JOIN `campus_buildings`
                               WHERE `is_lab`=%s
                               AND `campus_id`=%s""",
                               (lab, campus_id))
        else:
            cursor.execute("""SELECT `id`, `room_no`, `capacity`, `is_lab`
                           FROM `classes`
                           NATURAL JOIN `campus_buildings`
                           WHERE `campus_id`=%s""", (campus_id,))
    elif lab is not None:
        if department:
            cursor.execute("""SELECT `id`, `building_id`, `room_no`, `capacity`
                        FROM `classes`
                        WHERE `is_lab`=%s
                        AND `department`=%s""", (lab, department))
        else:
            cursor.execute("""SELECT `id`, `building_id`,
                        `room_no`, `capacity`, `department`
                        FROM `classes`
                        WHERE `is_lab`=%s""", (lab,))
    else:
        cursor.execute("""SELECT * FROM `classes`""")
    return cursor.fetchall()

def get_class(cursor: Cursor, /, *,
              class_id: Optional[int] = None) -> Optional[Dict[str, Union[bool, int]]]:
    cursor.execute("""SELECT `building_id`, `room_no`,
                   `capacity`, `is_lab`, `department`
                   FROM `classes`
                   WHERE `id`=%s""", (class_id,))
    return cursor.fetchone()

def get_courses_by_degree_stream_year(cursor, degree: str, stream: str, year: int) -> list[dict]:
	programme_id = show_data.get_programme_id(cursor, degree=degree, stream=stream)
	assert programme_id is not None, "Invalid programme"
	query = """
    SELECT name AS course_name, code AS course_code, L, T, P, credits AS credit
    FROM courses
    JOIN programme_courses ON code = course_code
    WHERE programme_id = %s
    """
	cursor.execute(query, (programme_id,))
	cols = [col[0] for col in cursor.description]
	return [dict(zip(cols, row)) for row in cursor.fetchall()]

def get_sections_from_file(*,
                           campus_id: Optional[int] = None,
                           degree: Optional[str] = None,
                           stream: Optional[str] = None,
                           year: Optional[int] = None) -> List[str]:
    sections = []
    with open("data/sections.csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (
                (not campus_id or int(row["campus_id"]) == campus_id)
                and (not degree or row["degree"] == degree)
                and (not stream or row["stream"] == stream)
                and (not year or int(row["year"]) == year)
            ):
                sections.append(row["section"])
    return sections

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

def get_faculty_id(cursor: Cursor, /, *,
                   campus_id: Optional[int] = None,
                   department: Optional[str] = None,
                   name: Optional[str] = None,
                   join_year: Optional[int] = None,
                   section_id: Optional[int] = None,
                   course_code: Optional[str] = None,
                   faculty_section_course_code: Optional[str] = None) -> Optional[List[int]]:
    if section_id and course_code:
        cursor.execute("""SELECT `faculty_id` AS `id`
                       FROM `faculty_section_course`
                       WHERE `section_id`=%s
                       AND `course_code`=%s""", (section_id, course_code))
    elif faculty_section_course_code:
        cursor.execute("""SELECT `faculty_id` AS `id`
                       FROM `faculty_section_course` `FTC`
                       WHERE `FTC`.`id`=%s""", (faculty_section_course_code,))
    elif campus_id:
        if department:
            if name:
                if join_year:
                    cursor.execute("""SELECT `id`
                                   FROM `faculties`
                                   WHERE `campus_id`=%s
                                   AND `department`=%s
                                   AND `name`=%s
                                   AND `join_year`=%s""",
                                   (campus_id, department, name, join_year))
                else:
                    cursor.execute("""SELECT `id`
                                   FROM `faculties`
                                   WHERE `campus_id`=%s
                                   AND `department`=%s
                                   AND `name`=%s""",
                                   (campus_id, department, name))
            elif join_year:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `campus_id`=%s
                                AND `department`=%s
                                AND `join_year`=%s""",
                                (campus_id, department, join_year))
            else:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `campus_id`=%s
                                AND `department`=%s""",
                                (campus_id, department))
        elif name:
            if join_year:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `campus_id`=%s
                                AND `name`=%s
                                AND `join_year`=%s""",
                                (campus_id, name, join_year))
            else:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `campus_id`=%s
                                AND `name`=%s""",
                                (campus_id, name))
        elif join_year:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `campus_id`=%s
                            AND `join_year`=%s""",
                            (campus_id, join_year))
        else:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `campus_id`=%s""",
                            (campus_id,))
    elif department:
        if name:
            if join_year:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `department`=%s
                                AND `name`=%s
                                AND `join_year`=%s""",
                                (department, name, join_year))
            else:
                cursor.execute("""SELECT `id`
                                FROM `faculties`
                                WHERE `department`=%s
                                AND `name`=%s""",
                                (department, name))
        elif join_year:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `department`=%s
                            AND `join_year`=%s""",
                            (department, join_year))
        else:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `department`=%s""",
                            (department,))
    elif name:
        if join_year:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `name`=%s
                            AND `join_year`=%s""",
                            (name, join_year))
        else:
            cursor.execute("""SELECT `id`
                            FROM `faculties`
                            WHERE `name`=%s""",
                            (name,))
    elif join_year:
        cursor.execute("""SELECT `id`
                        FROM `faculties`
                        WHERE `join_year`=%s""",
                        (join_year,))
    else:
        cursor.execute("""SELECT `id` FROM `faculties`""")
    faculties: Tuple[Dict[str, int], ...] = cursor.fetchall()
    if not faculties:
        return None
    return [faculty["id"] for faculty in faculties]

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
        if isinstance(password, str) and password:
            cursor.execute("""SELECT * FROM `faculty_view`
                           WHERE `id`=%s""", (id,))
            faculty: Optional[Dict[str, Union[float, int, str]]] = cursor.fetchone()
            if faculty:
                pwd: Union[float, int, str] = faculty["password"]
        
            PasswordHasher().verify(pwd, password)
        else:
            raise ValueError("Password must be a non-empty string")

    except exceptions.VerifyMismatchError:
        if faculty and pwd:
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

def get_section_students(cursor: Cursor, /, *,
                         section_id: Optional[int] = None,
                         student_id: Optional[int] = None):
    if section_id:
        cursor.execute("""SELECT `student_id`
                       FROM `section_students`
                       WHERE `section_id`=%s""", (section_id,))
    elif student_id:
        cursor.execute("""SELECT `section_id`
                       FROM `section_students`
                       WHERE `student_id`=%s""", (student_id,))
    else:
        cursor.execute("""SELECT * FROM `section_students`""")
    return cursor.fetchall()

def get_faculty_section_courses(cursor: Cursor, /, *,
                               faculty_id: Optional[int] = None,
                               section_id: Optional[int] = None,
                               course_code: Optional[str] = None,) -> Tuple[Dict[str, Union[int, str]], ...]:
    if faculty_id and section_id and course_code:
        cursor.execute("""SELECT `id`, `section_id`, `course_code`
                       FROM `faculty_section_course`
                       WHERE `faculty_id`=%s
                       AND `section_id`=%s
                       AND `course_code`=%s""",
                       (faculty_id, section_id, course_code))
    elif faculty_id and section_id:
        cursor.execute("""SELECT `id`, `course_code`
                       FROM `faculty_section_course`
                       WHERE `faculty_id`=%s
                       AND `section_id`=%s""",
                       (faculty_id, section_id))
    elif faculty_id and course_code:
        cursor.execute("""SELECT `id`, `section_id`
                       FROM `faculty_section_course`
                       WHERE `faculty_id`=%s
                       AND `course_code`=%s""",
                       (faculty_id, course_code))
    elif section_id and course_code:
        cursor.execute("""SELECT `id`, `faculty_id`
                       FROM `faculty_section_course`
                       WHERE `section_id`=%s
                       AND `course_code`=%s""",
                       (section_id, course_code))
    elif faculty_id:
        cursor.execute("""SELECT `id`, `section_id`, `course_code`
                       FROM `faculty_section_course`
                       WHERE `faculty_id`=%s""", (faculty_id,))
    elif section_id:
        cursor.execute("""SELECT `id`, `faculty_id`, `course_code`
                       FROM `faculty_section_course`
                       WHERE `section_id`=%s""", (section_id,))
    elif course_code:
        cursor.execute("""SELECT `id`, `faculty_id`, `section_id`
                       FROM `faculty_section_course`
                       WHERE `course_code`=%s""", (course_code,))
    else:
        cursor.execute("""SELECT * FROM `faculty_section_course`""")
    return cursor.fetchall()

def get_student_electives(cursor: Cursor, /, *,
                          student_id: Optional[int] = None,
                          course_code: Optional[str] = None):
    if student_id:
        if course_code:
            cursor.execute("""SELECT 1
                           FROM `student_electives`
                           WHERE `student_id`=%s
                           AND `course_code`=%s
                           LIMIT 1""", (student_id, course_code))
            return True if cursor.fetchone() else False
        else:
            cursor.execute("""SELECT `course_code`
                           FROM `student_electives`
                           WHERE `student_id`=%s""", (student_id,))
    elif course_code:
        cursor.execute("""SELECT `student_id`
                       FROM `student_electives`
                       WHERE `course_code`=%s""", (course_code,))
    else:
        cursor.execute("""SELECT * FROM `student_electives`""")
    return cursor.fetchall()

def get_timetable(cursor: Cursor, /,
                  degree: str,
                  stream: str,
                  year: str,
                  campus: str,
                  section: str) -> Optional[Tuple[Dict[str, Union[int, str]], ...]]:
    cursor.execute("""
        SELECT day, hour, course_code, room_no, building_id, faculty_id
        FROM timetable_view
        WHERE degree = %s
          AND stream = %s
          AND year = %s
          AND campus = %s
          AND section = %s
    """, (degree, stream, year, campus, section))
    return cursor.fetchall()
