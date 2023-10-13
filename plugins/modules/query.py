#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: sqlite_query
short_description: Query data from an SQLite database.
description:
  - This module allows you to fetch data from an SQLite database.

options:
  db_path:
    description:
      - Path to the SQLite database.
      - Make sure the database file is accessible and readable.
    required: True
    type: str

  query:
    description:
      - SQL query string to fetch data from the database.
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
# Simple select query without parameters
- name: Fetch data from database
  sqlite_query:
    db_path: /path/to/database.db
    query: "SELECT * FROM test;"

# Parameterized select query using a list
- name: Fetch data based on ID
  sqlite_query:
    db_path: /path/to/database.db
    query: "SELECT * FROM test WHERE id = ?;"
    params: [1]

# Parameterized select query using a dictionary
- name: Fetch data based on name and age
  sqlite_query:
    db_path: /path/to/database.db
    query: "SELECT * FROM users WHERE name = :name AND age = :age;"
    params:
      name: "John"
      age: 25

# Querying an in-memory database
- name: Fetch data from in-memory database
  sqlite_query:
    query: "SELECT * FROM temp_data WHERE id = ?;"
    params: [2]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
import os

try:
    import sqlite_utils
    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False

__metaclass__ = type


class SQLiteDatabaseModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        super(SQLiteDatabaseModule, self).__init__(*args, **kwargs)

        if not HAS_SQLITE_UTILS:
            self.fail_json(
                msg="The sqlite-utils library is required (`pip install sqlite-utils`)"
            )

    def run_sql_query(self, db_path, query, params=None, db_options=None):
        try:
            if not os.path.exists(db_path):
                self.fail_json(msg=f"Database path {db_path} does not exist.")
            db = sqlite_utils.Database(db_path, **(db_options or {}))
            results = db.query(query, params)
            return list(results)
        except Exception as e:
            if "'NoneType' object is not iterable" in str(e):
                self.fail_json(msg="Query must be a SELECT statement.")
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
        rows = module.run_sql_query(db_path, query, params, db_options)
        module.exit_json(changed=False, rows=rows)
    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
