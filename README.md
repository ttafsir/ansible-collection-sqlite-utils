# Ansible Collection - ttafsir.sqlite_utils

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml)

A collection of Ansible plugins to manage SQLite databases leveraging the `sqlite-utils` Python package.

## Requirements

- Ansible 2.9 or later
-  `sqlite-utils` package


## Collection contents

### Plugins

### Modules

* `ttafsir.sqlite_utils.run_sql`: Ansible module to query a sqlite database and return list of dictionaries.

#### Lookup Plugins

* `ttafsir.sqlite_utils.sqlite`: A lookup plugin that returns query results from a sqlite database using the sqlite-utils library.


## Usage Examples

### `query` module

```yaml
- name: Fetch data from database
  ttafsir.sqlite_utils.run_sql:
    db_path: database.sqlite
    query: "SELECT * FROM emails ORDER BY email_id"
  register: query_1

- debug: var=query_1.rows

- name: Fetch data based on ID
  ttafsir.sqlite_utils.run_sql:
    db_path: database.sqlite
    query: "SELECT * FROM emails WHERE email_id = ?;"
    params: [3]
  register: query_2

- debug: var=query_2.rows

- name: Fetch data based on name and age
  ttafsir.sqlite_utils.run_sql:
    db_path: database.sqlite
    query: |-
      SELECT * FROM emails
      WHERE subject = :subject
      AND email_id = :email_id
    params:
      subject: "Hello World"
      email_id: 1
  register: query_3

- debug: var=query_3.rows

- name: Update data based on ID
  ttafsir.sqlite_utils.run_sql:
    db_path: database.sqlite
    query: "UPDATE emails SET subject = ? WHERE email_id = ?;"
    params: ["Hello World Updated", 1]
  register: update_result

- debug: var=query_3.rows_affected
```

###  Lookup

```yaml
---
- hosts: localhost
  gather_facts: no
  vars:
    where_arg: {"subject": "Peek #4"}

  tasks:

    - name: Fetch two columns from SQLite
      debug:
        msg: "{{
          lookup(
            'ttafsir.sqlite_utils.sqlite',
            table='emails',
            db_path=database,
            select='email_id, subject')
        }}"

    - name: Fetch row from SQLite where email subject matches
      debug:
        msg: "{{
          lookup(
            'ttafsir.sqlite_utils.sqlite',
            table='emails',
            db_path='database.sqlite',
            where='subject = :subject',
            where_args=where_arg
          )
        }}"
```

See the lookup plugin documentation for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ttafsir/ansible-collection-sqlite-utils/blob/main/LICENSE) file for details.

## Links

- [sqlite-utils Python package](https://pypi.org/project/sqlite-utils/)
