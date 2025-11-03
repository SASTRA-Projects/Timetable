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


from typehints import Connection, Cursor


def create_views(db_connector: Connection, cursor: Cursor) -> None:
    r"""
    Create database views to simplify queries
    and improve data retrieval efficiency.

    This function generates **SQL views**,
    which are stored queries that allow efficient
    access to faculty information, campus departments, and campus buildings.

    Views Created
    =============
    1. **``faculty_view``**: Combines faculty details
                             with their additional info.
        - **Columns**: All columns from `faculties` and `faculty_info`.

    2. **``campus_departments``**: Lists departments available at each campus.
        - **Columns**: `campus_id`, `department`

    3. **``campus_buildings``**: Lists buildings available at each campus.
        - **Columns**: `campus_id`, `building_id`

    4. **``programme_duration``**: Lists duration (in years)
                                   for each programme.
        - **Columns**: `programme_id`, `duration`

    5. **``section_student_details``**: Lists details of section & students.
        - **Columns**: `section_id`, `student_id`, `campus_id`,
                       `degree`, `stream`, `section`, `year`,
                       `name`, `join_year`, `programme_id`, `roll_no`

    Parameters
    ==========
    - **db_connector**: Connection
      The database connection object used to interact with the database.

    - **cursor**: Cursor
      A cursor object for executing SQL commands.

    Examples
    =========
    .. code-block:: python

        >>> from Timetable.mysql_connector import connect

        >>> # Create Connection object and Cursor object
        >>> connector, cursor = connect(
                user="root",
                password="secret_pwd",
                host="localhost"
            )

        >>> create_database(connector, cursor)
        >>> create_relations(connector, cursor)
        >>> create_timetable(connector, cursor)
        >>> create_views(connector, cursor)

    See Also
    ========
    - `create_database()`: Defines the base tables for the database.
    - `create_relations()`: Defines foreign keys and relational constraints.
    - `create_timetable()`: Ensures timetable data is generated,
                            before views are created.
    """
    import timetable
    timetable.create_timetable(db_connector, cursor)

    cursor.execute("""CREATE OR REPLACE VIEW `faculty_view` AS
                   SELECT *
                   FROM `faculties`
                   JOIN `faculty_info`
                   ON `faculties`.`id`=`faculty_info`.`faculty_id`
    """)
    cursor.execute("""CREATE OR REPLACE VIEW `campus_departments` AS
                   SELECT `campuses`.`id` AS `campus_id`,
                   `SD`.`department` AS `department`
                   FROM `school_departments` `SD`
                   INNER JOIN `schools`
                   ON `schools`.`id`=`SD`.`school_id`
                   INNER JOIN `campuses`
                   ON `campuses`.`id`=`schools`.`campus_id`
    """)
    cursor.execute("""CREATE OR REPLACE VIEW `campus_buildings` AS
                   SELECT `campuses`.`id` AS `campus_id`,
                   `buildings`.`id` AS `building_id`,
                   `buildings`.`school_id` AS `school_id`,
                   `buildings`.`rooms` AS `rooms`
                   FROM `buildings`
                   INNER JOIN `schools`
                   ON `schools`.`id`=`buildings`.`school_id`
                   INNER JOIN `campuses`
                   ON `campuses`.`id`=`schools`.`campus_id`
    """)
    cursor.execute("""CREATE OR REPLACE VIEW `programme_duration` AS
                   SELECT `programmes`.`id` AS `programme_id`, `duration`
                   FROM `degrees`
                   INNER JOIN `programmes`
                   ON `degrees`.`name`=`programmes`.`degree`
    """)
    cursor.execute("""CREATE OR REPLACE VIEW `section_student_details` AS
                   SELECT `section_id`, `student_id`,
                   `sections`.`campus_id` AS `campus_id`,
                   `degree`, `stream`, `section`, `year`,
                   `name`, `join_year`, `programme_id`, `roll_no`
                   FROM `section_students`
                   INNER JOIN `sections`
                   ON `sections`.`id`=`section_id`
                   INNER JOIN `students`
                   ON `students`.`id`=`student_id`""")
    db_connector.commit()
