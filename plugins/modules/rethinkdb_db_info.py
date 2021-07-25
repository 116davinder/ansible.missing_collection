#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_db_info
short_description: Get information about RethinkDB Database.
description:
  - Get information about RethinkDB Database.
  - U(https://rethinkdb.com/api/python/)
version_added: 0.1.1
options:
  host:
    description:
      - hostname of rethinkdb.
    required: true
    type: str
  port:
    description:
      - port number of rethinkdb.
    required: false
    type: int
    default: 28015
  user:
    description:
      - rethinkdb username.
    required: false
    type: str
    default: 'admin'
  password:
    description:
      - password for rethinkdb I(user).
    required: false
    type: str
    default: ''
  ssl:
    description:
      - use SSL for rethinkdb connection.
      - may not work!.
    required: false
    type: dict
    default: None
  database:
    description:
      - name of the database.
    required: false
    type: str
  list_databases:
    description:
      - do you want to fetch list of all databases?
    required: false
    type: bool
  list_database_config:
    description:
      - do you want to fetch I(database) config?
    required: false
    type: bool
  list_tables:
    description:
      - do you want to fetch list tables from from I(database)?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: list all database in rethinkdb cluster
  community.missing_collection.rethinkdb_db_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    list_databases: true

- name: get information about given rethinkdb database
  community.missing_collection.rethinkdb_db_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    list_database_config: true
    database: 'database1'

- name: get list of tables of given rethinkdb database
  community.missing_collection.rethinkdb_db_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    list_tables: true
    database: 'database1'
"""

RETURN = """
databases:
  description: list of all the database rethinkdb cluster.
  returned: when success and defined I(list_databases).
  type: list
  sample: ["database1", "rethinkdb", "test"]
database_config:
  description: database configuration.
  returned: when success and defined I(list_database_config).
  type: dict
  sample: {"id": "5eed5253-4267-4014-9434-50c78a8c0d0d", "name": "database1"}
tables:
  description: list of all the tables rethinkdb database.
  returned: when success and defined I(tables).
  type: list
  sample: ["table1", "table2"]
"""

from ansible.module_utils.basic import AnsibleModule
from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError, ReqlAuthError


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(required=False, type=int, default=28015),
        user=dict(required=False, default="admin"),
        password=dict(required=False, default=""),
        ssl=dict(required=False, type=dict, default=None),
        database=dict(required=False),
        list_databases=dict(required=False, type=bool),
        list_database_config=dict(required=False, type=bool),
        list_tables=dict(required=False, type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("list_database_config", True, ["database"]),
            ("list_tables", True, ["database"]),
        ),
        mutually_exclusive=[("list_databases", "list_database_config", "list_tables")],
    )

    client = RethinkDB()
    _params = {
        "host": module.params["host"],
        "port": module.params["port"],
        "user": module.params["user"],
        "password": module.params["password"],
        "ssl": module.params["ssl"],
        "db": "rethinkdb",
    }

    try:
        conn = client.connect(**_params)
        if module.params["list_databases"]:
            _res = client.db_list().run(conn)
            module.exit_json(databases=_res)
        elif module.params["list_database_config"]:
            _res = client.db(module.params["database"]).config().run(conn)
            module.exit_json(database_config=_res)
        elif module.params["list_tables"]:
            _res = client.db(module.params["database"]).table_list().run(conn)
            module.exit_json(tables=_res)
        else:
            module.fail_json("unknown options")
    except (ReqlAuthError, ReqlOpFailedError) as e:
        module.fail_json(msg=e.message)
    finally:
        conn.close(noreply_wait=False)


if __name__ == "__main__":
    main()
