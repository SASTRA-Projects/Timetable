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


def create_indexes(db_connector: Connection, cursor: Cursor) -> None:
    cursor.execute("""CREATE INDEX `TIMETABLES_DAY_PERIOD`
                   ON `timetables` (`day`, `period_id`)
    """)

    cursor.execute("""CREATE INDEX `TIMETABLES_FSC_ID`
                   ON `timetables` (`faculty_section_course_id`)
    """)

    cursor.execute("""CREATE INDEX `FSC_SECTION_COURSE`
                   ON `faculty_section_course`
                   (`section_id`, `course_code`, `class_id`, `faculty_id`)
    """)

    cursor.execute("""CREATE INDEX `SECTION_CLS_STRENGTH`
                   ON `section_class` (`section_id`, `strength`)""")

    cursor.execute("""CREATE INDEX `SECTION_STUDENTS`
                   ON `section_students` (`student_id`, `section_id`)
    """)

    cursor.execute("""CREATE INDEX `STUDENT_ELECTIVES`
                   ON `student_electives` (`course_code`, `student_id`)
    """)
    db_connector.commit()
