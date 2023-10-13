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
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
import sqlite3
import os

try:
    import sqlite_utils

    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False


class SQLiteDatabaseModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        super(SQLiteDatabaseModule, self).__init__(*args, **kwargs)

        if not HAS_SQLITE_UTILS:
            self.fail_json(
                msg="The sqlite-utils library is required (`pip install sqlite-utils`)"
            )

    def run_sql(self, db_path: str, query, params=None, db_options=None):
        aggregated_results = []
        was_changed = False

        if not os.path.exists(db_path):
            self.fail_json(
                msg=f"Database path {db_path} does not exist or is not accessible."
            )
        elif not os.path.isfile(db_path):
            self.fail_json(msg=f"The path {db_path} is not a file.")
        elif not os.access(db_path, os.R_OK):
            self.fail_json(msg=f"The file at {db_path} is not readable.")

        try:
            db = sqlite_utils.Database(db_path, **(db_options or {}))

            # Check if it's a SELECT query
            if query.strip().upper().startswith("SELECT"):
                results = db.query(query, params)
                return (False, {"rows": list(results)})

            # Handle non-SELECT queries
            cursor = db.execute(query, params)
            changed = cursor.rowcount > 0
            return (changed, {"rows_affected": cursor.rowcount})

        except sqlite3.Error as db_err:
            self.fail_json(msg=f"Database error: {to_text(db_err)}")
        except Exception as e:
            self.fail_json(msg=to_text(e))


def main():
    module = SQLiteDatabaseModule(
        argument_spec=dict(
            db_path=dict(type="str", required=True),
            query=dict(type="str", required=True),
            params=dict(type="raw", required=False, default=None),
            db_options=dict(type="raw", required=False, default=None),
        ),
        supports_check_mode=True,
    )

    db_path = module.params["db_path"]
    query = module.params["query"]
    params = module.params["params"]
    db_options = module.params["db_options"]

    try:
        changed, result = module.run_sql(db_path, query, params, db_options)
        module.exit_json(changed=changed, **result)
    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
