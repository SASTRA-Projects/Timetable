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


from typehints import Connection, Cursor, Optional, Union
import datetime


"""
Adds the data to the correspoding tables.
For datas that won't be added frequently,
the functions are defined here.
"""


def add_campus(db_connector: Connection,
               cursor: Cursor, /, *,
               id: Optional[int] = None,
               campus: Optional[str] = None) -> None:
    r"""
    Add a new campus record to the `campuses` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The campus ID (optional; if not provided,
      the database will auto-generate it).
    - **campus** : Optional[str]
      The name of the campus.

    Examples
    ========
    .. code-block:: python

        >>> from SASTRA import *
        >>> connector, cursor = connect(
                user="root",
                password="secret_pwd",
                host="localhost"
            )

        >>> create_views(connector, cursor)
        >>> create_triggers(connector, cursor)
        >>> add_campus(connector, cursor, id=2, campus="SRC")
    """
    cursor.execute("""INSERT INTO `campuses` (`id`, `name`)
                   VALUES (%s, %s)""", (id, campus))
    db_connector.commit()


def add_school(db_connector: Connection,
               cursor: Cursor, /, *,
               id: Optional[int] = None,
               school: Optional[str] = None,
               campus_id: Optional[int] = None) -> None:
    r"""
    Add a new school record to the `schools` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The school ID (optional; if not provided,
      the database will auto-generate it).
    - **school** : Optional[str]
      The name of the school.
    - **campus_id** : Optional[int]
      The ID of the campus where the school is in.

    Examples
    ========
    .. code-block:: python

        >>> campus_id = get_campus_id(cursor, campus="SASTRA")
        >>> add_school(connector, cursor, id=3,
        ...            school="SoC", campus_id=campus_id)

    See Also
    ========
    - :func:`get_campus_id` – To get the ID of the given campus.
    """
    cursor.execute("""INSERT INTO `schools` (`id`, `name`, `campus_id`)
                   VALUES (%s, %s, %s)""", (id, school, campus_id))
    db_connector.commit()


def add_building(db_connector: Connection,
                 cursor: Cursor, /, *,
                 id: Optional[int] = None,
                 school_id: Optional[int] = None,
                 rooms: Optional[int] = None) -> None:
    r"""
    Add a new building record to the `buildings` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The building ID (optional; if not provided,
      the database may auto-generate it).
    - **school_id** : Optional[str]
      The ID of the school to which the building belongs.
    - **rooms** : Optional[int]
      The Number of Rooms (Classrooms + Labs) in that building.

    Examples
    ========
    .. code-block:: python

        >>> school_id = get_school_id(cursor, campus_id=1, school="SoC")
        >>> # building's id is None; auto-generated from 1
        >>> add_school(connector, cursor, school_id=school_id, rooms=63)
        >>> # Assuming, this is the only building record
        >>> print(get_buildings(connector, cursor, school_id=3))
        [{id: 1, school_id: 3, rooms: 63}]

    See Also
    ========
    - :func:`get_school_id` – To get the ID of the given school.
    """
    cursor.execute("""INSERT INTO `buildings` (`id`, `school_id`, `rooms`)
                   VALUES (%s, %s, %s)""", (id, school_id, rooms))
    db_connector.commit()


def add_department(db_connector: Connection,
                   cursor: Cursor, /, *,
                   department: Optional[str] = None) -> None:
    r"""
    Add a new department record to the `departments` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **department** : Optional[str]
      The name of the department.

    Examples
    ========
    .. code-block:: python

        >>> add_department(connector, cursor, department="Mathematics")
    """
    cursor.execute("""INSERT INTO `departments` (`name`)
                   VALUES (%s)""", (department,))
    db_connector.commit()


def add_degree(db_connector: Connection,
               cursor: Cursor, /, *,
               degree: Optional[str] = None,
               duration: Optional[int] = None) -> None:
    r"""
    Add a new degree record to the `degrees` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **degree** : Optional[str]
      The name of the degree.
    - **duration** : Optional[int]
      The duration for the completion of the degree.

    Examples
    ========
    .. code-block:: python

        >>> add_degree(connector, cursor, degree="B.Tech.")
    """
    cursor.execute("""INSERT INTO `degrees` (`name`, `duration`)
                   VALUES (%s, %s)""", (degree, duration))
    db_connector.commit()


def add_stream(db_connector: Connection,
               cursor: Cursor, /, *,
               stream: Optional[str] = None,
               department: Optional[str] = None) -> None:
    r"""
    Add a new stream record to the `streams` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **stream** : Optional[str]
      The name of the stream.
    - **department** : Optional[str]
      The department under which the stream is in.

    Examples
    ========
    .. code-block:: python

        >>> add_stream(connector, cursor,
        ...            stream="Artificial Intelligence and Data Science",
        ...            department="Computer Science")
    """
    cursor.execute("""INSERT INTO `streams` (`name`, `department`)
                   VALUES (%s, %s)""", (stream, department))
    db_connector.commit()


def add_programme(db_connector: Connection,
                  cursor: Cursor, /, *,
                  id: Optional[int] = None,
                  degree: Optional[str] = None,
                  stream: Optional[str] = None) -> None:
    r"""
    Add a new programme record to the `programmes` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The programme ID (optional; if not provided,
      the database will auto-generate it).
    - **degree** : Optional[str]
      The name of the degree.
    - **stream** : Optional[str]
      The name of the stream.

    Examples
    ========
    .. code-block:: python

        >>> add_programme(connector, cursor, id=7, degree="B.Tech.",
        ...               stream="Artificial Intelligence and Data Science")
    """
    cursor.execute("""INSERT INTO `programmes` (`id`, `degree`, `stream`)
                   VALUES (%s, %s, %s)""", (id, degree, stream))
    db_connector.commit()

def add_campus_programme(db_connector: Connection,
                         cursor: Cursor, /, *,
                         campus_id: Optional[int] = None,
                         programme_id: Optional[int] = None) -> None:
    r"""
    Add a new campus-programme record to the `campus_programmes` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **campus_id** : Optional[int]
      The campus ID (Programme offering campus).
    - **programme_id** : Optional[int]
      The programme ID.

    Examples
    ========
    .. code-block:: python

        >>> campus_id = get_campus_id(cursor, "SRC")
        >>> # returns only the ID
        >>> programme_id = get_programme_id(cursor, degree="B.Sc.",
        ...                                 stream="Nuclear Physics")
        >>> add_campus_programme(connector, cursor, campus_id=campus_id,
        ...                      programme_id=programme_id)

    See Also
    ========
    - :func:`get_programme_id` – To get the programme details.
    """
    cursor.execute("""INSERT INTO `campus_programmes`
                   (`campus_id`, `programme_id`)
                   VALUES (%s, %s)""", (campus_id, programme_id))
    db_connector.commit()


def add_school_department(db_connector: Connection,
                          cursor: Cursor, /, *,
                          school_id: Optional[int] = None,
                          department: Optional[str] = None) -> None:
    r"""
    Add a new school-department record to the `school_departments` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **school_id** : Optional[int]
      The school ID (School having the Department).
    - **department** : Optional[str]
      The name of the department.

    Examples
    ========
    .. code-block:: python

        >>> school_id = get_school_id(cursor, campus_id=1, school="SoC")
        >>> add_school_department(connector, cursor, school_id=school_id,
        ...                       department="Computer Science")

    See Also
    ========
    - :func:`get_school_id` – To get the school ID of the given campus
                              and name of the school.
    """
    cursor.execute("""INSERT INTO `school_departments`
                   (`school_id`, `department`)
                   VALUES (%s, %s)""", (school_id, department))
    db_connector.commit()


def add_class(db_connector: Connection,
              cursor: Cursor, /, *,
              id: Optional[int] = None,
              building_id: Optional[int] = None,
              room_no: Optional[int] = None,
              floor: Optional[int] = None,
              capacity: Optional[int] = None,
              is_lab: bool = False,
              department: Optional[str] = None) -> None:
    r"""
    Add a new class record to the `classes` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The class ID.
    - **building_id** : Optional[int]
      The building ID where the classroom is in.
    - **room_no** : Optional[int]
      The room number within the building.
    - **floot** : Optional[int]
      The floor number number within the building.
    - **capacity** : Optional[int]
      The capacity of the class.
    - **is_lab** : bool
      True if classroom is lab, False otherwise (False by default).

    Examples
    ========
    .. code-block:: python

        >>> building = get_buildings(cursor, school_id=5)[0]
        >>> add_class(connector, cursor, id=1, building_id=building["id"],
        ...           room_no=107, floor_no=1, capacity=60)

    See Also
    ========
    - `get_buildings()` – To get the building details for the given school ID.
    """
    if is_lab and not department:
        raise ValueError("Lab Classes must have a department")
    cursor.execute("""INSERT INTO `classes`
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                   (id, building_id, room_no, floor, capacity, is_lab, department))
    db_connector.commit()


def add_section(db_connector: Connection,
                cursor: Cursor, /, *,
                id: Optional[int] = None,
                campus_id: Optional[int] = None,
                degree: Optional[str] = None,
                stream: Optional[str] = None,
                section: Optional[str] = None,
                year: Optional[str] = None) -> None:
    r"""
    Add a new section record to the `sections` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The section ID.
    - **campus_id** : Optional[int]
      The campus ID where the section is in.
    - **degree** : Optional[str]
      The degree pursued by student in the section.
    - **stream** : Optional[str]
      The stream chosen by student in the section.
      (If many stream students, then None)
    - **year** : Optional[int]
      The year of study (of the students under the degree-stream).
    - **section** : Optional[str]
      The section name - usually one letter (can also be 2, like "A1", "B", ...).

    Examples
    ========
    .. code-block:: python

        >>> campus_id = get_campus_id(cursor, campus="SRC")
        >>> add_class(connector, cursor, id=1, campus_id=campus_id,
        ...           degree="B.Tech.", year=1, section="A")  # stream is None, here

    See Also
    ========
    - `get_campus_id()` – To get the ID of the given campus.
    """
    cursor.execute("""INSERT INTO `sections`
                   (`id`, `campus_id`, `degree`, `stream`, `section`, `year`)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (id, campus_id, degree, stream, section, year))
    db_connector.commit()


def add_faculty(db_connector: Connection,
                cursor: Cursor, /, *,
                id: Optional[str] = None,
                name: Optional[str] = None,
                campus_id: Optional[int] = None,
                join_year: Optional[int] = None) -> None:
    r"""
    Add a new faculty record to the `faculties` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The faculty ID (optional; if not provided,
      the database will auto-generate it).
    - **name** : Optional[str]
      The name of the faculty member.
    - **campus_id** : Optional[int]
      The campus ID where the faculty is assigned.
    - **join_year** : Optional[int]
      The year the faculty joined (optional).

    Examples
    ========
    .. code-block:: python

        >>> campus_id = get_campus_id(cursor, campus="SRC")
        >>> add_faculty(connector, cursor, id="C1495",
                        name="T. Muthukumar",
                        campus_id=campus_id
            )

    See Also
    ========
    - :func:`get_campus_id` – To get the campus ID based on the campus name.
    """
    cursor.execute("""INSERT INTO `faculties`
                   (`id`, `name`, `campus_id`, `join_year`)
                   VALUES (%s, %s, %s, %s)""",
                   (id, name, campus_id, join_year))
    db_connector.commit()


def add_student(db_connector: Connection,
                cursor: Cursor, /, *,
                id: Optional[int] = None,
                name: Optional[str] = None,
                campus_id: Optional[int] = None,
                join_year: int = datetime.date.today().year,
                programme_id: Optional[int] = None,
                roll_no: Optional[int] = None) -> None:
    r"""
    Add a new student record to the `students` table.

    Parameters
    ==========
    - **db_connector** : Connection
      The database connection object used to interact with the database.
    - **cursor** : Cursor
      Cursor object for executing SQL commands.
    - **id** : Optional[int]
      The student ID (optional; if not provided,
      the database will auto-generate it).
    - **name** : Optional[str]
      The name of the student.
    - **campus_id** : Optional[int]
      The campus ID where the student is enrolled.
    - **join_year** : int
      The year the student joined (defaults to the current year).
    - **programme_id** : Optional[int]
      The ID of the programme the student is enrolled in.
    - **roll_no** : Optional[int]
      The roll number assigned to the student (optional; if not provided,
      the database will auto-generate it).
    Examples
    ========
    .. code-block:: python

        >>> programme_id = get_programme_id(
                cursor,
                degree="B.Tech.",
                stream="Artificial intelligence and data science"
            )
        >>> add_student(connector, cursor, id=233, name="Sarvesh. S",
                        campus_id=1, join_year=2023, programme_id=programme_id,
                        roll_no=None)

    See Also
    ========
    - :func:`get_programme_id` – To get the programme ID for
                                 a given degree and stream.
    """
    cursor.execute("""INSERT INTO `students`
                   (`id`, `name`, `campus_id`, `join_year`,
                   `programme_id`, `roll_no`)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                   (id, name, campus_id, join_year,
                    programme_id, roll_no))
    db_connector.commit()
