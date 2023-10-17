# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Tafsir Thiam (@ttafsir) <ttafsir@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type


import traceback
from ansible.module_utils.basic import missing_required_lib
from pathlib import Path


IMPORT_ERROR = None
try:
    from sqlite_utils import Database
    from sqlite_utils.cli import insert_upsert_implementation

    HAS_SQLITE_UTILS = True
except ImportError:
    HAS_SQLITE_UTILS = False
    IMPORT_ERROR = traceback.format_exc()


def insert_arg_spec():
    return dict(
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


def file_insert_arg_spec():
    return dict(
        db_path=dict(type="str", required=True),
        table=dict(type="str", required=True),
        file_path=dict(type="str", required=True),
        pk=dict(type="str", default=None),
        empty_null=dict(type="bool", default=False),
        lines=dict(type="bool", default=False),
        text=dict(type="bool", default=False),
        convert=dict(type="dict", default=None),
        imports=dict(type="list", elements="raw", default=None),
        batch_size=dict(type="int", default=100),
        stop_after=dict(type="int", default=None),
        alter=dict(type="bool", default=False),
        upsert=dict(type="bool", default=False),
        ignore=dict(type="bool", default=False),
        replace=dict(type="bool", default=False),
        truncate=dict(type="bool", default=False),
        not_null=dict(type="list", elements="raw", default=None),
        analyze=dict(type="bool", default=False),
        silent=dict(type="bool", default=False),
    )


class SqliteUtilsModule:
    def __init__(self, module):
        self.module = module
        self.result = dict(changed=False, message="")
        self.params = module.params

        if not HAS_SQLITE_UTILS:
            module.fail_json(
                msg=missing_required_lib("sqlite-utils"), exception=IMPORT_ERROR
            )

    def exit_json(self, **kwargs):
        self.result.update(**kwargs)
        self.module.exit_json(**self.result)

    def fail_json(self, msg, **kwargs):
        self.result.update(**kwargs)
        self.module.fail_json(msg=msg, **self.result)

    def get_db(self, **kwargs):
        return Database(self.params["db_path"], **kwargs)


class SqliteUtilsInsertModule(SqliteUtilsModule):
    def __init__(self, module):
        super(SqliteUtilsInsertModule, self).__init__(module)

        file_path = module.params["file_path"]
        if not Path(file_path).exists():
            module.fail_json(
                msg=f"File path {file_path} does not exist or is not accessible."
            )
        self.file = Path(file_path)

    def insert_upsert(self, *args, **kwargs):
        return insert_upsert_implementation(*args, **kwargs)
