# Ansible Collection - ttafsir.sqlite_utils

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml/badge.svg)](https://github.com/ttafsir/ansible-collection-sqlite-utils/actions/workflows/ci.yml)

A collection of Ansible plugins to manage SQLite databases leveraging the `sqlite-utils` Python package.

## Requirements

- Ansible 2.9 or later
-  `sqlite-utils` package


You can install the collection from Ansible Galaxy:

```bash
ansible-galaxy collection install ttafsir.sqlite_utils
```

### From Source

Clone the repository from GitHub:

```bash
git clone https://github.com/ttafsir/ansible-collection-sqlite-utils.git
cd ansible-sqlite-utils
ansible-galaxy collection build
ansible-galaxy collection install ./ttafsir-sqlite_utils-*.tar.gz
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/ttafsir/ansible-collection-sqlite-utils/blob/main/LICENSE) file for details.

## Links

- [sqlite-utils Python package](https://pypi.org/project/sqlite-utils/)
