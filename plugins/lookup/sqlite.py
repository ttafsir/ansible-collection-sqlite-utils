# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
name: sqlite
author: Tafsir Thiam (@ttafsir)
short_description: Query SQLite databases using the sqlite-utils package
description:
    - The sqlite lookup plugin allows querying SQLite databases using the sqlite-utils package.
    - Features include filtering rows, selecting specific columns, ordering results, and counting rows.
options:
    db_path:
        description:
            - Path to the SQLite database.
            - Defaults to the SQLITE_DB_PATH environment variable.
        type: str
    table_name:
        description: Name of the table to query.
        required: yes
        type: str
    where:
        description: Optional WHERE clause.
        type: str
    where_args:
        description: Optional arguments for the WHERE clause.
        type: raw  # raw because it can be list or dictionary
    select:
        description: Columns to select. Default is '*'.
        type: str
    order_by:
        description: Order results by specified column(s).
        type: str
    limit:
        description: Limit the number of returned results.
        type: int
    offset:
        description: Offset for returned results.
        type: int
    count:
        description: Return count of rows instead of rows themselves.
        type: bool
requirements:
    - sqlite-utils
"""

EXAMPLES = r"""
- name: Fetch all rows from SQLite
  debug:
    msg: "{{ lookup('ttafsir.sqlite_utils.sqlite', table='emails', db_path='database.db') }}"

- name: Fetch single column from SQLite
  debug:
    msg: "{{ lookup('ttafsir.sqlite_utils.sqlite', table='emails', db_path='database.db', select='email_id') }}"

- name: Fetch two columns from SQLite
  debug:
    msg: "{{ lookup('ttafsir.sqlite_utils.sqlite', table='emails', db_path='database.db', select='email_id, subject') }}"

- name: Fetch single row using a WHERE clause
  debug:
    msg: "{{ lookup('ttafsir.sqlite_utils.sqlite', table='emails', db_path='database.db', where='subject = :subject', where_args={'subject': 'Peek #4'}) }}"

- name: Loop through all rows and display a specific column
  debug:
    msg: "{{ item.subject }}"
  loop: "{{ lookup('ttafsir.sqlite_utils.sqlite', table='emails', db_path='database.db') }}"
"""
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import os

try:
    import sqlite_utils

    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False


def run_sqlite_lookup(terms, variables=None, **kwargs):
    db_path = os.environ.get("SQLITE_DB_PATH", None) or kwargs.get("db_path")
    table_name = kwargs.get("table")

    where = kwargs.get("where", None)
    where_args = kwargs.get("where_args", [])

    select = kwargs.get("select", "*")
    order_by = kwargs.get("order_by", None)
    limit = kwargs.get("limit", None)
    offset = kwargs.get("offset", None)
    count = kwargs.get("count", False)

    if not db_path or not table_name:
        raise AnsibleError("db_path and table_name are required parameters")

    db = sqlite_utils.Database(db_path)
    table = db[table_name]

    if count:
        return [table.count_where(where, where_args)]

    if where is None:
        return list(table.rows)

    return list(
        table.rows_where(
            where,
            where_args,
            select=select,
            order_by=order_by,
            limit=limit,
            offset=offset,
        )
    )


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if not HAS_SQLITE_UTILS:
            raise AnsibleError("sqlite-utils is required for this module")

        return run_sqlite_lookup(terms, variables, **kwargs)
