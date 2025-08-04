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


from typehints import Connection, Cursor, Optional

"""Delete rows from tables.
"""
def delete_timetable(db_connector: Connection,
					 cursor: Cursor, /, *,
					 day: Optional[str] = None,
					 period_id: Optional[int] = None,
					 faculty_section_course_id: Optional[int] = None,
					 class_id: Optional[int] = None) -> None:
	cursor.execute("""DELETE FROM `timetables`
				   WHERE `day`=%s
				   AND `period_id`=%s
				   AND `faculty_section_course_id`=%s
				   AND `class_id`=%s""", (day, period_id, faculty_section_course_id, class_id))
	db_connector.commit()
