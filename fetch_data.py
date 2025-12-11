# Copyright 2025 Harikrishna Srinivasan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from argon2 import PasswordHasher, exceptions
from show_data import get_buildings, get_degree_duration, get_programme
from typehints import Cursor, Dict, Optional, Tuple, Union

"""
Shows the data for tables,
for which data will change frequently.
"""


def get_course(cursor: Cursor, /, *,
               code: Optional[str] = None) -> Optional[Dict[str, Union[bool, int, str]]]:
    cursor.execute("""SELECT MAX(`course`) AS `name`,
                   SUM(`hrs`) AS `hrs`,
                   MAX(`is_elective`) AS `is_elective`,
                   MIN(`is_lab`) AS `is_lab`
                   FROM `faculty_section_course`
                   WHERE `course_code` = %s
                   GROUP BY `course_code`""", (code,))
    return cursor.fetchone()


def get_classes(cursor: Cursor, /, *,
                campus_id: Optional[int] = None,
                building_id: Optional[int] = None,
                floor: Optional[int] = None,
                lab: Optional[bool] = None,
                department: Optional[str] = None,
                section_id: Optional[int] = None,
                room_no: Optional[int] = None) -> Tuple[Dict[str, Union[bool, int]], ...]:
    if section_id:
        cursor.execute("""SELECT `classes`.`id` AS `id`,
                       `room_no`, `capacity`, `strength`, `floor`
                       FROM `section_class`
                       JOIN `classes`
                       ON `class_id`=`classes`.`id`
                       AND `section_id`=%s""", (section_id,))
    elif building_id:
        if lab is not None:
            if department:
                cursor.execute("""SELECT `id`, `room_no`,
                               `capacity`, `floor`
                               FROM `classes`
                               WHERE `is_lab`=%s
                               AND `building_id`=%s
                               AND `department`=%s""",
                               (lab, building_id, department))
            else:
                cursor.execute("""SELECT `id`, `room_no`,
                               `capacity`, `department`, `floor`
                               FROM `classes`
                               WHERE `is_lab`=%s
                               AND `building_id`=%s""",
                               (lab, building_id))
        else:
            cursor.execute("""SELECT `id`, `room_no`, `capacity`,
                           `is_lab`, `floor`
                           FROM `classes`
                           WHERE `building_id`=%s""", (building_id,))
    elif campus_id:
        if lab is not None:
            if department:
                cursor.execute("""SELECT `id`, `room_no`,
                               `capacity`, `floor`
                               FROM `classes`
                               NATURAL JOIN `campus_buildings`
                               WHERE `is_lab`=%s
                               AND `campus_id`=%s
                               AND `department`=%s""",
                               (lab, campus_id, department))
            else:
                cursor.execute("""SELECT `id`, `room_no`, `capacity`,
                               `department`, `floor`
                               FROM `classes`
                               NATURAL JOIN `campus_buildings`
                               WHERE `is_lab`=%s
                               AND `campus_id`=%s""",
                               (lab, campus_id))
        else:
            cursor.execute("""SELECT `id`, `room_no`,
                           `capacity`, `is_lab`, `floor`
                           FROM `classes`
                           NATURAL JOIN `campus_buildings`
                           WHERE `campus_id`=%s""", (campus_id,))
    elif lab is not None:
        if department:
            cursor.execute("""SELECT `id`, `building_id`,
                           `room_no`, `capacity`, `floor`
                           FROM `classes`
                           WHERE `is_lab`=%s
                           AND `department`=%s""", (lab, department))
        else:
            cursor.execute("""SELECT `id`, `building_id`, `room_no`,
                           `capacity`, `department`, `floor`
                           FROM `classes`
                           WHERE `is_lab`=%s""", (lab,))
    else:
        cursor.execute("""SELECT * FROM `classes`""")

    res = cursor.fetchall()
    if room_no:
        res = [r for r in res if r.pop("room_no") == room_no]
    if floor is not None: 
        res = [r for r in res if r.pop("floor") == floor]

    return res


def get_class(cursor: Cursor, /, *,
              class_id: Optional[int] = None,
              building_id: Optional[int] = None,
              room_no: Optional[int] = None) -> Optional[Dict[str, Union[bool, int]]]:
    if class_id:
        cursor.execute("""SELECT `building_id`, `room_no`,
                       `capacity`, `is_lab`, `department`, `floor`
                       FROM `classes`
                       WHERE `id`=%s""", (class_id,))
    elif building_id and room_no:
        cursor.execute("""SELECT `id`, `capacity`,
                       `is_lab`, `department`, `floor`
                       FROM `classes`
                       WHERE `building_id`=%s
                       AND `room_no`=%s""",
                       (building_id, room_no))
    else:
        return None
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
                                   AND (`stream`=%s OR `stream` IS NULL)
                                   AND `year`=%s""",
                                   (campus_id, degree, stream, year))
                else:
                    cursor.execute("""SELECT `id`, `year`, `section`
                                   FROM `sections`
                                   WHERE `campus_id`=%s
                                   AND `degree`=%s
                                   AND (`stream`=%s OR `stream` IS NULL)""",
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
                               AND (`stream`=%s OR `stream` IS NULL)
                               AND `year`=%s""",
                               (campus_id, stream, year))
            else:
                cursor.execute("""SELECT `id`, `degree`, `year`, `section`
                               FROM `sections`
                               WHERE `campus_id`=%s
                               AND (`stream`=%s OR `stream` IS NULL)""",
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
                               AND (`stream`=%s OR `stream` IS NULL)
                               AND `year`=%s""",
                               (degree, stream, year))
            else:
                cursor.execute("""SELECT `id`, `campus_id`,
                               `year`, `section`
                               FROM `sections`
                               WHERE `degree`=%s
                               AND (`stream`=%s OR `stream` IS NULL)""",
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
                           WHERE (`stream`=%s OR `stream` IS NULL)
                           AND `year`=%s""",
                           (stream, year))
        else:
            cursor.execute("""SELECT `id`, `campus_id`,
                           `degree`, `year`, `section`
                           FROM `sections`
                           WHERE (`stream`=%s OR `stream` IS NULL)""",
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
                   `year`, `section`, `class_id`, `strength`
                   FROM `sections`
                   JOIN `section_class`
                   ON `section_id`=`id`
                   WHERE `id`=%s""", (section_id,))
    return cursor.fetchone()


def get_section_id(cursor: Cursor, /, *,
                   campus_id: Optional[int] = None,
                   degree: Optional[str] = None,
                   stream: Optional[str] = None,
                   year: Optional[int] = None,
                   section: Optional[str] = None) -> Optional[int]:
    sections = get_sections(cursor, campus_id=campus_id,
                            degree=degree, stream=stream, year=year)
    if not (sections and campus_id and degree and year and section):
        return None

    for s in sections:
        if s["section"] == section and isinstance(s["id"], int):
            return s["id"]
    return None


def get_section_classes(cursor: Cursor, /, *,
                        section_id: Optional[int] = None,
                        class_id: Optional[int] = None) -> Union[bool, Tuple[Dict[str, Union[int, str]], ...]]:
    if section_id:
        if class_id:
            cursor.execute("""SELECT 1
                           FROM `section_class`
                           WHERE `section_id`=%s
                           AND `class_id`=%s
                           LIMIT 1""", (section_id, class_id))
            return cursor.fetchone() is not None

        else:
            cursor.execute("""SELECT `class_id`, `strength`
                           FROM `section_class`
                           WHERE `section_id`=%s
                           LIMIT 1""", (section_id,))
    elif class_id:
        cursor.execute("""SELECT `section_id`, `strength`
                       FROM `section_class`
                       WHERE `class_id`=%s""", (class_id,))
    else:
        cursor.execute("""SELECT * FROM `section_class`""")
    return cursor.fetchall()

def get_electives(cursor: Cursor, /, *,
                  degree: Optional[str] = None) -> Tuple[Dict[str, Union[bool, int, str]], ...]:
    if degree:
        cursor.execute("""SELECT *
                       FROM `faculty_section_course` `FSC`
                       JOIN `sections`
                       ON `sections`.`id`=`FSC`.`section_id`
                       AND `is_elective`
                       AND `degree`=%s""", (degree,))
        return cursor.fetchall()

    cursor.execute("""SELECT *
                   FROM `faculty_section_course`
                   WHERE `is_elective`""")
    return cursor.fetchall()


def is_elective(cursor: Cursor, /, *,
                course_code: Optional[str] = None,
                programme_id: Optional[int] = None,
                section_id: Optional[int] = None) -> bool:
    if section_id and course_code:
        cursor.execute("""SELECT `is_elective`
                       FROM `faculty_section_course`
                       WHERE `section_id`=%s
                       AND `course_code`=%s
                       LIMIT 1""", (section_id, course_code))
    else:
        pass ### yet to implement
    res = cursor.fetchone()
    return bool(res["is_elective"]) if res else False


def get_faculties(cursor: Cursor, /, *,
                  campus_id: Optional[int] = None) -> Tuple[Dict[str, Union[int, str]], ...]:
    if campus_id:
        cursor.execute("""SELECT `id`, `name`, `join_year`
                       FROM `faculties`
                       WHERE `campus_id`=%s""", (campus_id,))
    else:
        cursor.execute("""SELECT * FROM `faculties`""")
    return cursor.fetchall()


def get_faculty_name(cursor: Cursor, /, *,
                     id: Optional[str] = None) -> Optional[str]:
    cursor.execute("""SELECT `name` FROM `faculties`
                   WHERE `id`=%s
                   LIMIT 1""", (id,))
    faculty = cursor.fetchone()
    return faculty["name"] if faculty else None


def get_faculty_id(cursor: Cursor, /, *,
                   campus_id: Optional[int] = None,
                   name: Optional[str] = None,
                   join_year: Optional[int] = None,
                   section_id: Optional[int] = None,
                   course_code: Optional[str] = None,
                   faculty_section_course_id: Optional[int] = None) -> Optional[Tuple[str]]:
    if section_id and course_code:
        cursor.execute("""SELECT `faculty_id` AS `id`
                       FROM `faculty_section_course`
                       WHERE `section_id`=%s
                       AND `course_code`=%s""", (section_id, course_code))
    elif faculty_section_course_id:
        cursor.execute("""SELECT `faculty_id` AS `id`
                       FROM `faculty_section_course` `FSC`
                       WHERE `FSc`.`id`=%s""", (faculty_section_course_id,))
    elif campus_id:
        if name:
            if join_year:
                cursor.execute("""SELECT `id`
                               FROM `faculties`
                               WHERE `campus_id`=%s
                               AND `name`=%s
                               AND `join_year`<=>%s""",
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
                           AND `join_year`<=>%s""",
                           (campus_id, join_year))
        else:
            cursor.execute("""SELECT `id`
                           FROM `faculties`
                           WHERE `campus_id`=%s""",
                           (campus_id,))
    elif name:
        if join_year:
            cursor.execute("""SELECT `id`
                           FROM `faculties`
                           WHERE `name`=%s
                           AND `join_year`<=>%s""",
                           (name, join_year))
        else:
            cursor.execute("""SELECT `id`
                           FROM `faculties`
                           WHERE `name`=%s""",
                           (name,))
    elif join_year:
        cursor.execute("""SELECT `id`
                       FROM `faculties`
                       WHERE `join_year`<=>%s""",
                       (join_year,))
    else:
        cursor.execute("""SELECT `id` FROM `faculties`""")
    faculties = cursor.fetchall()
    if not faculties:
        return None
    return tuple(faculty["id"] for faculty in faculties)


def get_students(cursor: Cursor, /, *,
                 campus_id: Optional[int] = None,
                 programme_id: Optional[int] = None,
                 section_id: Optional[int] = None) -> Tuple[Dict[str, Union[int, str]], ...]:
    if campus_id:
        if programme_id:
            cursor.execute("""SELECT `id`, `name`, `join_year`,
                           `roll_no`, `phone`,
                           CONCAT(
                            `campus_id`,
                            LPAD(MOD((`join_year` + `PD`.`duration`),
                                 100), 2, '0'),
                            LPAD(`PD`.`programme_id`, 3, '0'),
                            LPAD(`roll_no`, 3, '0')
                           ) AS `reg_no`
                           FROM `students`
                           JOIN `programme_duration` AS `PD`
                           ON `PD`.`programme_id`=`students`.`programme_id`
                           AND `campus_id`=%s
                           AND `PD`.`programme_id`=%s""",
                           (campus_id, programme_id))
        else:
            cursor.execute("""SELECT `id`, `name`,
                           `PD`.`programme_id`, `join_year`,
                           `roll_no`, `phone`,
                           CONCAT(
                            `campus_id`,
                            LPAD(MOD((`join_year` + `PD`.`duration`),
                                 100), 2, '0'),
                            LPAD(`PD`.`programme_id`, 3, '0'),
                            LPAD(`roll_no`, 3, '0')
                           ) AS `reg_no`
                           FROM `students`
                           JOIN `programme_duration` AS `PD`
                           ON `PD`.`programme_id`=`students`.`programme_id`
                           AND `campus_id`=%s""", (campus_id,))
    elif programme_id:
        cursor.execute("""SELECT  `id`, `name`,
                       `campus_id`, `join_year`,
                       `roll_no`, `phone`,
                       CONCAT(
                        `campus_id`,
                        LPAD(MOD((`join_year` + `PD`.`duration`),
                             100), 2, '0'),
                        LPAD(`PD`.`programme_id`, 3, '0'),
                        LPAD(`roll_no`, 3, '0')
                       ) AS `reg_no`
                       FROM `students`
                       JOIN `programme_duration` AS `PD`
                       ON `PD`.`programme_id`=`students`.`programme_id`
                       AND `PD`.`programme_id`=%s""", (programme_id,))
    else:
        cursor.execute("""SELECT *,
                       CONCAT(
                        `campus_id`,
                        LPAD(MOD((`join_year` + `PD`.`duration`),
                             100), 2, '0'),
                        LPAD(`PD`.`programme_id`, 3, '0'),
                        LPAD(`roll_no`, 3, '0')
                       ) AS `reg_no`
                       FROM `students`
                       JOIN `programme_duration` AS `PD`
                       ON `PD`.`programme_id`=`students`.`programme_id`""")
    if section_id:
        students = cursor.fetchall()
        section_students = {student["student_id"]
                            for student in get_section_students(
                                cursor, section_id=section_id)}
        return tuple(student for student in students
                     if student["id"] in section_students)
    return cursor.fetchall()


def get_student(cursor: Cursor, /, *,
                id: Optional[int] = None,
                campus_id=None,
                join_year=None,
                programme_id=None,
                roll_no: Optional[int] = None,
                reg_no: Optional[Union[int, str]] = None) -> Optional[Dict[str, Union[int, str]]]:
    if id:
        cursor.execute("""SELECT `name`,
                       CONCAT(
                        `campus_id`,
                        LPAD(MOD((`join_year` + `PD`.`duration`),
                             100), 2, '0'),
                        LPAD(`PD`.`programme_id`, 3, '0'),
                        LPAD(`roll_no`, 3, '0')
                       ) AS `reg_no`
                       FROM `students`
                       JOIN `programme_duration` AS `PD`
                       ON `PD`.`programme_id`=`students`.`programme_id`
                       AND `id`=%s""", (id,))
    elif campus_id and join_year and programme_id and roll_no:
        cursor.execute("""SELECT `id`, `name`,
                       CONCAT(
                        `campus_id`,
                        LPAD(MOD((`join_year` + `PD`.`duration`),
                             100), 2, '0'),
                        LPAD(`PD`.`programme_id`, 3, '0'),
                        LPAD(`roll_no`, 3, '0')
                       ) AS `reg_no`
                       FROM `students`
                       JOIN `programme_duration` AS `PD`
                       ON `PD`.`programme_id`=`students`.`programme_id`
                       AND `campus_id`=%s
                       AND `join_year`=%s
                       AND `PD`.`programme_id`=%s
                       AND `roll_no`=%s""",
                       (campus_id, join_year, programme_id, roll_no))

    if res := cursor.fetchone() and reg_no:
        reg_no = str(reg_no)
        res = res if str(res.pop("reg_no")) == reg_no else None

    return res


def decompose_reg_no(cursor: Cursor, /, *,
                     reg_no: Optional[Union[int, str]] = None):
    _reg_no = str(reg_no)
    campus_id = int(_reg_no[0])
    programme_id = int(_reg_no[3:6])
    degree = get_programme(cursor, programme_id=programme_id)["degree"]
    duration = get_degree_duration(cursor, degree=degree)
    join_year = 2000 + int(_reg_no[1:3]) - duration % 100
    roll_no = int(_reg_no[6:9])
    return (campus_id, programme_id, join_year, roll_no)


def get_reg_no(cursor: Cursor, /, *,
               id: Optional[int] = None,
               campus_id=None,
               join_year=None,
               programme_id=None,
               roll_no: Optional[int] = None) -> Optional[str]:
    if get_student(cursor, id=id, campus_id=campus_id,
                   join_year=join_year, programme_id=programme_id,
                   roll_no=roll_no):
        degree = get_programme(cursor, programme_id=programme_id)["degree"]
        duration = get_degree_duration(cursor, degree=degree)
        final_year = (join_year + duration) % 100
        return f"{campus_id}{final_year}{programme_id:03}{roll_no:03}"
    return None


def get_faculty_details(cursor: Cursor, /, *,
                        id: Optional[str] = None,
                        password: Optional[str] = None) -> Optional[Dict[str, Union[float, int, str]]]:
    try:
        if isinstance(password, str) and password:
            cursor.execute("""SELECT * FROM `faculty_view`
                           WHERE `id`=%s""", (id,))
            faculty = cursor.fetchone()
            pwd: Union[float, int, str] = 0
            if faculty:
                pwd = faculty["password"]

            ph = PasswordHasher()
            ph.verify(pwd, password)
        else:
            raise ValueError("Password must be a non-empty string")
    except exceptions.VerifyMismatchError:
        if faculty and pwd:
            raise AssertionError("Incorrect Password")
    return faculty


def get_section_students(cursor: Cursor, /, *,
                         section_id: Optional[int] = None,
                         student_id: Optional[int] = None) -> Tuple[Dict[str, int], ...]:
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
                                faculty_id: Optional[str] = None,
                                section_id: Optional[int] = None,
                                class_id: Optional[int] = None,
                                course_code: Optional[str] = None,
                                is_lab: Optional[bool] = None,
                                is_elective: Optional[bool] = None,
                                full_batch: Optional[bool] = None,
                                section_details: Optional[bool] = None) -> list[Dict[str, Union[int, str]], ...]:
    all_columns = {
        "id", "faculty_id", "section_id", "course_code", "course",
        "hrs", "class_id", "is_lab", "is_elective", "full_batch"
    }

    filters, params, exclude = [], [], set()

    for col, val in {
        "faculty_id": faculty_id,
        "section_id": section_id,
        "course_code": course_code,
        "class_id": class_id,
        "is_lab": is_lab,
        "is_elective": is_elective,
        "full_batch": full_batch
    }.items():
        if val is not None:
            exclude.add(col)
            filters.append(f"`{col}`=%s")
            params.append(val)

    select_clause = ", ".join(f"`{col}`" for col in (all_columns - exclude))
    query = f"SELECT {select_clause} FROM `faculty_section_course`"

    if filters:
        query += " WHERE " + " AND ".join(filters)

    cursor.execute(query, params)
    res = cursor.fetchall()

    if section_details:
        for r in res:
            sid = r["section_id"]
            if sid:
                r.update(get_section(cursor, section_id=sid))
    return list(res)


def get_faculty_section_course(cursor: Cursor, /, *,
                               faculty_section_course_id: Optional[int] = None) -> Optional[Dict[str, Union[int, str]]]:
    cursor.execute("""SELECT *
                   FROM `faculty_section_course`
                   WHERE `id`=%s""", (faculty_section_course_id,))
    return cursor.fetchone()


def get_student_electives(cursor: Cursor, /, *,
                          student_id: Optional[int] = None,
                          course_code: Optional[str] = None,
                          student_details: bool = False) -> Union[bool, Tuple[Dict[str, Union[int, str]], ...]]:
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

    if student_details:
        student_lookup = {s["id"]: s for s in get_students(cursor)}
        return tuple(
            ({**r, **student_lookup[r["student_id"]]})
            for r in cursor.fetchall()
            if r["student_id"] in student_lookup
        )
 
    return cursor.fetchall()


def get_periods(cursor: Cursor, /, *,
                period_id: Optional[int] = None) -> Tuple[Dict[str, Union[bool, int, str]]]:
    def format(tdelta):
        total_minutes = tdelta.total_seconds() // 60
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{hours:2d}:{minutes:02d}"

    if period_id:
        cursor.execute("""SELECT `start_time`, `end_time`, `is_break`
                       FROM `periods`
                       WHERE `id`=%s""", (period_id,))
    else:
        cursor.execute("""SELECT * FROM `periods`""")

    periods = cursor.fetchall()
    for period in periods:
        period["start_time"] = format(period["start_time"])
        period["end_time"] = format(period["end_time"])

    return periods


def get_timetables(cursor: Cursor, /, *,
                   faculty_section_course_id: Optional[int] = None,
                   campus_id: Optional[int] = None,
                   faculty_id: Optional[str] = None,
                   section_id: Optional[int] = None,
                   course_code: Optional[str] = None,
                   class_id: Optional[int] = None,
                   day: Optional[str] = None,
                   period_id: Optional[int] = None) -> tuple[dict[str, Union[bool, int, str]]]:
    if faculty_section_course_id:
        cursor.execute("""SELECT * FROM `timetables`
                       WHERE `faculty_section_course_id`=%s""",
                       (faculty_section_course_id,))
        return cursor.fetchall()
    if class_id:
        cursor.execute("""SELECT `day`, `period_id`, `faculty_id`,
                       `section_id`, `course_code`,
                       `faculty_section_course_id`, `floor`,
                       `building_id`, `room_no`, `capacity`,
                       `classes`.`is_lab`, `department`, `is_elective`
                       FROM `timetables`
                       JOIN `faculty_section_course` `FSC`
                       ON `FSC`.`id`=`faculty_section_course_id`
                       JOIN `classes`
                       ON `class_id`=`classes`.`id`
                       AND `class_id`=%s""",
                       (class_id,))
    else:
        cursor.execute("""SELECT `day`, `period_id`, `faculty_id`,
                       `section_id`, `course_code`, `floor`,
                       `faculty_section_course_id`, `class_id`,
                       `building_id`, `room_no`, `capacity`,
                       `classes`.`is_lab`, `department`, `is_elective`
                       FROM `timetables`
                       JOIN `faculty_section_course` `FSC`
                       ON `FSC`.`id`=`faculty_section_course_id`
                       JOIN `classes`
                       ON `class_id`=`classes`.`id`""")

    timetables = cursor.fetchall()
    if day:
        timetables = tuple(t for t in timetables if t["day"] == day)
    if period_id:
        timetables = tuple(t for t in timetables if t["period_id"] == period_id)
    if campus_id:
        buildings = {b["id"]
                     for b in get_buildings(cursor, campus_id=campus_id)}
        timetables = tuple(t for t in timetables if t["building_id"] in buildings)

    if faculty_id:
        timetables = tuple(t for t in timetables if t["faculty_id"] == faculty_id)
    if section_id:
        timetables = tuple(t for t in timetables if t["section_id"] == section_id)
    if course_code:
        timetables = tuple(t for t in timetables if t["course_code"] == course_code)

    return timetables


def get_free_faculties(cursor: Cursor, /, *,
                       campus_id: int,
                       period_ids: Tuple[int],
                       day: Optional[str] = None) -> Tuple[str, ...]:
    cursor.execute("""SELECT `id`, `faculty_id`
                   FROM `faculty_section_course`""")
    fsc = cursor.fetchall()
    faculties: dict[int, list[int]] = {}
    for f in fsc:
        faculties.setdefault(f["faculty_id"], []).append(f["id"])

    timetables = get_timetables(cursor, campus_id=campus_id, day=day)
    timetables = [t for t in timetables if t["period_id"] in period_ids]
    return tuple(f_id
                 for f_id, fsc_ids in faculties.items()
                 if not any(fid in timetables for fid in fsc_ids))
