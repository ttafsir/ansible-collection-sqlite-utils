#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: insert_json
short_description: Insert data from a file into an SQLite database table.
description:
  - This module inserts data from various file formats (like JSON, CSV) into an SQLite database table.
  - It uses the sqlite-utils Python library to handle the operations.
  - The table will be created or modified as necessary based on the parameters provided.
  - It's designed for bulk insertions and supports various optional parameters for data transformation and control.

options:
  db_path:
    description: Path to the SQLite database.
    required: True
    type: str

  table:
    description: Name of the table to insert data into.
    required: True
    type: str

  file_path:
    description: Path to the file containing the data to insert.
    required: True
    type: str

  pk:
    description: Specifies which column should be the primary key when creating the table.
    type: str

  nl:
    description: Specifies if the file uses newlines as a delimiter.
    type: bool
    default: False

  flatten:
    description: Flatten nested structures in JSON/CSV into individual rows.
    type: bool
    default: False

  empty_null:
    description: Convert empty strings to NULL.
    type: bool
    default: False

  lines:
    description: Indicates if the JSON file has one record per line.
    type: bool
    default: False

  text:
    description: Treat all values in CSV/TSV as text.
    type: bool
    default: False

  convert:
    description: Dictionary specifying SQL conversion functions to apply to data during insertion.
    type: dict

  imports:
    description: Python modules to import when using --convert.
    type: list
    elements: raw

  batch_size:
    description: Batch size for bulk inserts.
    type: int
    default: 100

  stop_after:
    description: Stop after inserting this many rows.
    type: int

  alter:
    description: If set, missing columns will be added automatically.
    type: bool
    default: False

  upsert:
    description: If set, the existing rows will be updated.
    type: bool
    default: False

  ignore:
    description: If a record with the same primary key already exists, the insertion will be ignored.
    type: bool
    default: False

  replace:
    description: If a record with the same primary key already exists, it will be replaced.
    type: bool
    default: False

  truncate:
    description: If set, the table will be truncated before inserting the new data.
    type: bool
    default: False

  not_null:
    description: Specifies columns that should be NOT NULL.
    type: list
    elements: raw

  analyze:
    description: Analyze the table after inserting data.
    type: bool
    default: False

  silent:
    description: Do not show progress bar or any other output.
    type: bool
    default: False

author:
  - Tafsir Thiam (@ttafsir)
"""

EXAMPLES = r"""
- name: Insert from json file
  ttafsir.sqlite_utils.insert_json:
    db_path: network.db
    table: interfaces
    file_path: interfaces.json
    flatten: true
    alter: true
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ttafsir.sqlite_utils.plugins.module_utils.common import (
    SqliteUtilsInsertModule,
    file_insert_arg_spec,
)


def run_module():
    module_args = file_insert_arg_spec()
    module_args.update(
        dict(
            nl=dict(type="bool", default=False),
            flatten=dict(type="bool", default=False),
        )
    )

    module = SqliteUtilsInsertModule(
        AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    )

    try:
        module.insert_upsert(
            module.params["db_path"],
            table=module.params["table"],
            file=module.file.open("rb"),
            pk=module.params["pk"],
            flatten=module.params["flatten"],
            nl=module.params["nl"],
            csv=False,
            tsv=False,
            delimiter=None,
            quotechar=None,
            sniff=False,
            no_headers=False,
            encoding=None,
            empty_null=module.params["empty_null"],
            lines=module.params["lines"],
            text=module.params["text"],
            convert=module.params["convert"],
            imports=module.params["imports"],
            batch_size=module.params["batch_size"],
            stop_after=module.params["stop_after"],
            alter=module.params["alter"],
            upsert=module.params["upsert"],
            ignore=module.params["ignore"],
            replace=module.params["replace"],
            truncate=module.params["truncate"],
            not_null=module.params["not_null"],
            analyze=module.params["analyze"],
            silent=module.params["silent"],
        )
        module.result["changed"] = True
        module.result["message"] = "Data inserted successfully from file"
        module.exit_json(**module.result)

    except Exception as e:
        module.fail_json(msg=f"Failed to insert data from file. Error: {str(e)}")


def main():
    run_module()


if __name__ == "__main__":
    main()
