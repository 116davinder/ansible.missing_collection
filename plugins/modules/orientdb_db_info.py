#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: orientdb_db_info
short_description: Get information from OrientDB Database.
description:
  - Get information from OrientDB Database.
  - U(https://orientdb.org/docs/3.0.x/pyorient/PyOrient-Client.html)
version_added: 0.2.0
options:
  host:
    description:
      - hostname of orientdb.
    required: true
    type: str
  port:
    description:
      - port number of orientdb.
    required: false
    type: int
    default: 2424
  user:
    description:
      - orientdb username.
    required: false
    type: str
    default: 'root'
  password:
    description:
      - password for orientdb I(user).
    required: false
    type: str
    default: 'root'
  database:
    description:
      - name of the database.
    required: false
    type: str
  storage_type:
    description:
      - storage type of the database.
    required: false
    type: str
    choices: ['plocal', 'memory']
  db_list:
    description:
      - do you want to fetch names of all the databases?
    required: false
    type: bool
  db_size:
    description:
      - do you want to fetch size of I(database)?
    required: false
    type: bool
  db_exists:
    description:
      - do you want to check existence of I(database)?
    required: false
    type: bool
  db_count_records:
    description:
      - do you want to fetch number of records from I(database)?
    required: false
    type: bool
  check_default_credentials:
    description:
      - do you want to check if any database is enabled with default credentials?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - pyorient
"""

EXAMPLES = """
- name: list all orientdb databases
  community.missing_collection.orientdb_db_info:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    db_list: true

- name: get database size in orientdb
  community.missing_collection.orientdb_db_info:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    db_size: 'true'
    database: 'test2'

- name: check database existence in orientdb
  community.missing_collection.orientdb_db_info:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    db_exists: true
    database: 'test2'
    type: 'plocal'

- name: get total number of records in orientdb database
  community.missing_collection.orientdb_db_info:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    db_count_records: true
    database: 'test2'

- name: get list of database with default credentials
  community.missing_collection.orientdb_db_info:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    check_default_credentials: true
"""

RETURN = """
databases:
  description: name of all the databases.
  returned: when I(db_list) is defined and success.
  type: dict
  sample: {
    "test1": "plocal:/orientdb/databases/test1",
    "test2": "memory:test2"
  }
size:
  description: size of the database.
  returned: when I(db_size) is defined and success.
  type: int
  sample: 12311
exist:
  description: check database existence.
  returned: when I(db_exists) is defined and success.
  type: bool
  sample: true
count:
  description: get number of records in database.
  returned: when I(db_count_records) is defined and success.
  type: int
  sample: 9
default_credential_dbs:
  description: check if any database exists with default credentials.
  returned: when I(check_default_credentials) is defined and success.
  type: list
  sample: ["test2"]
"""

from ansible.module_utils.basic import AnsibleModule
from pyorient import OrientDB


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(type=int, default=2424),
        user=dict(default="root"),
        password=dict(default="root", no_log=True),
        database=dict(),
        storage_type=dict(choices=["plocal", "memory"]),
        db_list=dict(type=bool),
        db_size=dict(type=bool),
        db_exists=dict(type=bool),
        db_count_records=dict(type=bool),
        check_default_credentials=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("db_size", True, ["database"]),
            ("db_exists", True, ["database", "storage_type"]),
            ("db_count_records", True, ["database"]),
        ),
        mutually_exclusive=[
            (
                "db_list",
                "db_size",
                "db_exists",
                "db_count_records",
                "check_default_credentials",
            )
        ]
    )

    client = OrientDB(
        host=module.params["host"],
        port=module.params["port"]
    )

    try:
        client.connect(
            user=module.params["user"],
            password=module.params["password"]
        )

        if module.params["db_list"]:
            module.exit_json(databases=client.db_list().__getattr__('databases'))
        elif module.params["db_size"]:
            client.db_open(
                module.params["database"],
                module.params["user"],
                module.params["password"]
            )
            module.exit_json(size=client.db_size())
        elif module.params["db_exists"]:
            module.exit_json(
                exist=client.db_exists(
                    module.params["database"],
                    type=module.params["storage_type"]
                ))
        elif module.params["db_count_records"]:
            client.db_open(
                module.params["database"],
                module.params["user"],
                module.params["password"]
            )
            module.exit_json(count=client.db_count_records())
        elif module.params["check_default_credentials"]:
            _db_list = list()
            # Check for Default Login
            for i in client.db_list().__getattr__("databases"):
                try:
                    client.db_open(i, "admin", "admin")
                    _db_list.append(i)
                    client.db_close()
                except:   # nopep8 #nosec
                    pass
            module.exit_json(default_credential_dbs=_db_list)
        else:
            module.fail_json(msg="unknown options are passed")
    except Exception as e:
        module.fail_json(msg=str(e))
    finally:
        client.db_close()


if __name__ == "__main__":
    main()
