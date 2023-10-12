# Ansible Collection - ttafsir.sqlite_utils

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml)

A collection of Ansible plugins to manage SQLite databases leveraging the `sqlite-utils` Python package.

## Requirements

- Ansible 2.9 or later
-  `sqlite-utils` package


## Collection contents

### Plugins

#### Lookup Plugins

* `ttafsir.sqlite_utils.sqlite`: A lookup plugin that returns query results from a sqlite database using the `rows_where` method.


## Usage Examples

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
