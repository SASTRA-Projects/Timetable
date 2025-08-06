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


import importlib
import sys
import os

sys.path.append(os.path.dirname(__file__))

__version__ = "1.0.0b1"

__all__ = [
    "add_data",
    "app",
    "delete_data",
    "fetch_data",
    "index",
    "insert_data",
    "mysql_connector",
    "show_data",
    "triggers",
    "typehints",
    "views"
]


def __getattr__(name):
    if name in __all__:
        module = importlib.import_module(f".{name}", __name__)
        sys.modules[f"{__name__}.{name}"] = module
        return module
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return __all__
