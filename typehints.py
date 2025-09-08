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


from typing import Dict, List, Literal, Optional, TypeAlias, Union, Tuple, Set
import pymysql
import werkzeug

Connection: TypeAlias = pymysql.connections.Connection
Cursor: TypeAlias = pymysql.cursors.DictCursor

Response: TypeAlias = werkzeug.wrappers.Response
NotFound: TypeAlias = werkzeug.exceptions.NotFound
IntegrityError: TypeAlias = pymysql.err.IntegrityError
FileStorage: TypeAlias = werkzeug.datastructures.file_storage.FileStorage
