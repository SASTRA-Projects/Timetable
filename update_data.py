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


from insert_data import add_faculty_info
from typehints import Connection, Cursor, Optional, Union

"""
Updates data in tables.
"""


def update_faculty_info(db_connector: Connection,
                        cursor: Cursor, /, *,
                        faculty_id: Optional[int] = None,
                        phone: Optional[Union[int, str]] = None,
                        salary: Optional[float] = None,
                        password: Optional[str] = None,
                        verbose: bool = True) -> None:
    if not password:
        raise ValueError("Password is missing")

    cursor.execute("""DELETE FROM `faculty_info`
                   WHERE `faculty_id`=%s
                   AND `phone`=%s
                   AND `salary`=%s""",
                   (faculty_id, phone, salary))
    db_connector.commit()

    add_faculty_info(db_connector, cursor,
                     faculty_id=faculty_id, phone=phone,
                     salary=salary, password=password, verbose=verbose)
