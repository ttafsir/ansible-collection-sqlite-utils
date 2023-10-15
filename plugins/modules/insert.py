#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: insert
short_description: Insert a single record into an SQLite database table.
description:
  - This module inserts a single record into an SQLite database table.
  - It uses the sqlite-utils Python library to perform the operation.
  - The table will be created or modified as necessary based on the parameters provided.

options:
  db_path:
    description:
      - Path to the SQLite database.
      - Ensure the database file is accessible and writable.
    required: True
    type: str

  table:
    description:
      - Name of the table to insert data into.
    required: True
    type: str

  records:
    description:
      - The record to insert into the table, represented as a dictionary.
    required: True
    type: raw

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

  hash_id:
    description:
      - Name of a column to create and use as a primary key, with its value derived as a SHA1 hash of other column values in the record.
    type: str

  alter:
    description:
      - If set, missing columns will be added automatically.
    type: bool
    default: False

  ignore:
    description:
      - If a record with the same primary key already exists, the insertion will be ignored.
    type: bool
    default: False

  replace:
    description:
      - If a record with the same primary key already exists, it will be replaced.
    type: bool
    default: False

  extracts:
    description:
      - List of columns to extract to other tables, or a dictionary that maps column names to other table names.
    type: raw

  conversions:
    description:
      - Dictionary specifying SQL conversion functions to apply to data during insertion.
    type: dict

  columns:
    description:
      - Dictionary overriding the detected types used for columns.
    type: dict

author:
  - Tafsir Thiam (@ttafsir)
"""

EXAMPLES = r"""
# Insert a single record into the 'cats' table
- name: Insert record into cats table
  ttafs:
    db_path: /path/to/database.db
    table: cats
    records:
      name: 'Whiskers'
      breed: 'Tabby'
      age: 5

- name: Insert record into cats table
  ttafs:
    db_path: /path/to/database.db
    table: cats
    records:
      - name: 'Whiskers'
        breed: 'Tabby'
        age: 5
      - name: 'Fluffy'
        breed: 'Persian'
        age: 3
"""
from ansible.module_utils.basic import AnsibleModule

try:
    from sqlite_utils import Database

    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False


def insert_records(table, records, module):
    if isinstance(records, list):
        table.insert_all(
            records,
            pk=module.params["pk"],
            column_order=module.params["column_order"],
            not_null=module.params["not_null"],
            defaults=module.params["defaults"],
            hash_id=module.params["hash_id"],
            alter=module.params["alter"],
            ignore=module.params["ignore"],
            replace=module.params["replace"],
            extracts=module.params["extracts"],
            conversions=module.params["conversions"],
            columns=module.params["columns"],
        )
    else:
        # Insert the record
        insert_result = table.insert(
            record=module.params["records"],
            pk=module.params["pk"],
            column_order=module.params["column_order"],
            not_null=module.params["not_null"],
            defaults=module.params["defaults"],
            hash_id=module.params["hash_id"],
            alter=module.params["alter"],
            ignore=module.params["ignore"],
            replace=module.params["replace"],
            extracts=module.params["extracts"],
            conversions=module.params["conversions"],
            columns=module.params["columns"],
        )

    return insert_result


def run_module():
    module_args = dict(
        db_path=dict(type="str", required=True),
        table=dict(type="str", required=True),
        records=dict(type="raw", required=True),
        pk=dict(type="str", default=None),
        column_order=dict(type="list", elements="raw", default=None),
        not_null=dict(type="list", elements="raw", default=None),
        defaults=dict(type="dict", default=None),
        hash_id=dict(type="str", default=None),
        alter=dict(type="bool", default=False),
        ignore=dict(type="bool", default=False),
        replace=dict(type="bool", default=False),
        extracts=dict(type="raw", default=None),
        conversions=dict(type="dict", default=None),
        columns=dict(type="dict", default=None),
    )

    result = dict(changed=False, message="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        return result

    try:
        db = Database(module.params["db_path"])
        table = db[module.params["table"]]
        records = module.params["records"]

        before_count = table.count
        insert_result = insert_records(table, records, module)

        result["changed"] = table.count > before_count
        result["rows"] = table.count
        result["message"] = "Data inserted successfully"
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Failed to insert data. Error: {str(e)}")


def main():
    run_module()


if __name__ == "__main__":
    main()
