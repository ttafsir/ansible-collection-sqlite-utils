#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: create
short_description: Create a table in an SQLite database.
description:
  - This module allows you to create a table in an SQLite database.
  - It uses the sqlite-utils Python library to handle the operations.
  - The database file is created if it doesn't exist.

options:
  db_path:
    description:
      - Path to the SQLite database.
      - Make sure the database file is accessible and writable.
    required: True
    type: str

  table:
    description:
      - Name of the table to create.
    required: True
    type: str

  columns:
    description:
      - Columns for the table in the form of a dictionary, where the key is the column name and the value is the column type.
      - Supported Python types are "str", "float", "int", "bool", "bytes", "datetime", "date", and "time".
    required: True
    type: dict

  replace:
    description:
      - If set to True, drops the table if it exists and creates a new one.
    type: bool
    default: False

  ignore:
    description:
      - If set to True and table already exists, silently ignores the operation.
    type: bool
    default: False

  pk:
    description:
      - Specifies which column should be the primary key when creating the table.
    type: str

  column_order:
    description:
      - Specifies a full or partial column order to use when creating the table.
    type: list
    elements: raw

  not_null:
    description:
      - Specifies columns that should be NOT NULL.
    type: list
    elements: raw

  defaults:
    description:
      - Specifies default values for specific columns.
    type: dict

  if_not_exists:
    description:
      - If set to True, does nothing if table already exists.
    type: bool
    default: False

author:
  - Tafsir Thiam (@ttafsir)
"""

EXAMPLES = r"""
# Create a simple table
- name: Create a table
  ttafsir.sqlite_utils.create:
    db_path: /path/to/database.db
    table: cats
    columns:
      name: str
      breed: str
      weight: float

# Create a table with additional configurations
- name: Create a table with a primary key and default values
  ttafsir.sqlite_utils.create:
    db_path: /path/to/database.db
    table: cats
    columns:
      id: int
      name: str
      breed: str
      weight: float
    pk: id
    defaults:
      breed: "Unknown"
"""
from ansible.module_utils.basic import AnsibleModule

try:
    from sqlite_utils import Database

    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Updated type mapping
TYPE_MAPPING = {
    "str": "TEXT",
    "float": "FLOAT",
    "int": "INTEGER",
    "bool": "INTEGER",
    "bytes": "BLOB",
    "datetime": "TEXT",
    "date": "TEXT",
    "time": "TEXT",
}

if HAS_NUMPY:
    NUMPY_TYPE_MAPPING = {
        np.int8: "INTEGER",
        np.int16: "INTEGER",
        np.int32: "INTEGER",
        np.int64: "INTEGER",
        np.uint8: "INTEGER",
        np.uint16: "INTEGER",
        np.uint32: "INTEGER",
        np.uint64: "INTEGER",
        np.float16: "FLOAT",
        np.float32: "FLOAT",
        np.float64: "FLOAT",
    }
    TYPE_MAPPING.update(NUMPY_TYPE_MAPPING)


def try_cast(value: str):
    """Attempts to cast a string value to its equivalent Python type.

    Tries to convert the string to a type based on a mapping of known types.
    Returns the original string if unable to
    """
    try:
        return TYPE_MAPPING[value]
    except KeyError:
        return value


def create_sqlite_table(module, result):
    user_columns = module.params["columns"]
    converted_columns = {key: try_cast(value) for key, value in user_columns.items()}

    db = Database(module.params["db_path"])
    table_name = module.params["table"]

    return db[table_name].create(
        converted_columns,
        replace=module.params["replace"],
        if_not_exists=module.params["if_not_exists"],
        ignore=module.params["ignore"],
        pk=module.params["pk"],
        column_order=module.params["column_order"],
        not_null=module.params["not_null"],
        defaults=module.params["defaults"],
    )


def run_module():
    module_args = dict(
        db_path=dict(type="str", required=True),
        table=dict(type="str", required=True),
        columns=dict(type="dict", required=True),
        pk=dict(type="str", default=None),
        column_order=dict(type="list", elements="raw", default=None),
        not_null=dict(type="list", elements="raw", default=None),
        defaults=dict(type="dict", default=None),
        if_not_exists=dict(type="bool", default=False),
        replace=dict(type="bool", default=False),
        ignore=dict(type="bool", default=False),
    )
    result = dict(changed=False, original_message="", message="")
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        return result

    if not HAS_SQLITE_UTILS:
        module.fail_json("sqlite-utils is required for this module")

    try:
        resp = create_sqlite_table(module, result)
        result["changed"] = resp is not None
        result["original_message"] = str(resp)
        result["message"] = "Table created successfully"
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=f"Failed to create table. Error: {str(e)}")


def main():
    run_module()


if __name__ == "__main__":
    main()
