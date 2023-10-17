#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: run_sql
short_description: Execute SQL statements on an SQLite database.
description:
  - This module allows you to execute SQL statements on an SQLite database.
  - For SELECT statements, it fetches and returns the data.
  - For non-SELECT statements, it returns the number of rows affected.
  - Supports only single SQL statements; multiple statements separated by semicolons are not supported.
  - The database file should exist, be a file (not a directory), and be readable.

options:
  db_path:
    description:
      - Path to the SQLite database.
      - This path should point to an existing database file that is readable.
    required: True
    type: str

  query:
    description:
      - SQL query string to execute. Only one statement is supported.
    required: True
    type: str

  params:
    description:
      - Optional parameters for the SQL query. Can be either a list or a dictionary.
      - Helps in preventing SQL injection when used correctly.
    required: False
    type: raw

  db_options:
    description:
      - Additional options passed to the sqlite_utils Database constructor.
      - Useful for advanced database configurations.
    required: False
    type: raw

  sql_method:
    description:
      - Specifies the type of SQL statement to execute.
    required: False
    type: str
    choices: ["query", "execute"]
    default: "query"

author:
  - Tafsir Thiam (@ttafsir)

notes:
  - The sqlite-utils library is required (`pip install sqlite-utils`).
  - It's highly recommended to use the `params` option to avoid SQL injection vulnerabilities.
"""


EXAMPLES = r"""
# Simple SELECT query without parameters
- name: Fetch data from database
  ttafsir.sqlite_utils.run_sql:
    db_path: /path/to/database.db
    query: "SELECT * FROM test;"

# Parameterized SELECT query using a list
- name: Fetch data based on ID
  ttafsir.sqlite_utils.run_sql:
    db_path: /path/to/database.db
    query: "SELECT * FROM test WHERE id = ?;"
    params: [1]

# Parameterized SELECT query using a dictionary
- name: Fetch data based on name and age
  ttafsir.sqlite_utils.run_sql:
    db_path: /path/to/database.db
    query: "SELECT * FROM users WHERE name = :name AND age = :age;"
    params:
      name: "John"
      age: 25

# Update data based on ID
- name: Update data based on ID
  ttafsir.sqlite_utils.run_sql:
    db_path: database.sqlite
    query: "UPDATE emails SET subject = ? WHERE email_id = ?;"
    params: ["Hello World Updated", 1]
  sql_method: execute
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible_collections.ttafsir.sqlite_utils.plugins.module_utils.common import (
    SqliteUtilsModule,
)

import sqlite3


def run_sql(module):
    db_options = module.params["db_options"] or {}
    db = module.get_db(**db_options)

    query = module.params["query"]
    params = module.params["params"]

    try:
        # Check if it's a SELECT query
        if module.params["sql_method"] == "query":
            results = db.query(query, params)
            return (False, {"rows": list(results)})

        # Handle non-SELECT queries
        if module.params["sql_method"] == "execute":
            cursor = db.execute(query, params)
            changed = cursor.rowcount > 0
            return (changed, {"rows_affected": cursor.rowcount})

    except sqlite3.Error as db_err:
        module.fail_json(msg=f"Database error: {to_text(db_err)}")
    except Exception as e:
        module.fail_json(msg=to_text(e))


def main():
    module = SqliteUtilsModule(
        AnsibleModule(
            argument_spec=dict(
                db_path=dict(type="str", required=True),
                query=dict(type="str", required=True),
                params=dict(type="raw", required=False, default=None),
                db_options=dict(type="raw", required=False, default=None),
                sql_method=dict(
                    type="str",
                    required=False,
                    default="query",
                    choices=["query", "execute"],
                ),
            ),
            supports_check_mode=True,
        )
    )

    try:
        changed, result = run_sql(module)
        module.exit_json(changed=changed, **result)
    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
