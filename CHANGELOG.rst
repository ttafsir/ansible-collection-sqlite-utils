==================================
ttafsir.sqlite_utils Release Notes
==================================

.. contents:: Topics

v1.4.0:
========

Release Summary
---------------

This release adds new modules to database and table creation and for loading data into tables.

New Modules
-----------
* `ttafsir.sqlite_utils.create`
* `ttafsir.sqlite_utils.insert`
* `ttafsir.sqlite_utils.insert_json`

Minor Changes
--------------
* move common boilerplate to module_utils to simplify current modules and make it easier to add new modules
* adds new parameter to `ttafsir.sqlite_utils.run_sql` to switch between `query` and `execute` methods

v1.3.0:
========

Release Summary
---------------

This release adds the ttafsir.sqlite_utils.run_sql module to wrap sqlite-util's `query` and `execute` methods.


v1.2.1:
========

Release Summary
---------------

This release is a maintenance release.

Minor Changes
--------------

-  updates README and examples to use the fqcn for the lookup module
