#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_table_index
short_description: Create/Delete RethinkDB Table Secondary Index.
description:
  - Create/Delete RethinkDB Table Secondary Index.
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
  state:
    description:
      - state of database.
    required: false
    type: str
    choices: ['present', 'absent', 'rename']
    default: 'present'
  database:
    description:
      - name of the database.
    required: true
    type: str
  table:
    description:
      - name of the table.
    required: true
    type: str
  key:
    description:
      - name of the secondard index key.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: create table secondary index in rethinkdb
  community.missing_collection.rethinkdb_table_index:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    state: present
    database: 'test'
    table: 'test1'
    key: 'test_id'

- name: rename table secondary index named test_id in rethinkdb
  community.missing_collection.rethinkdb_table_index:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    state: rename
    database: 'test'
    table: 'test1'
    key: 'test_id'
    new_key: 'test_new_key'

- name: delete table secondary index named test_id in rethinkdb
  community.missing_collection.rethinkdb_table_index:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    state: absent
    database: 'test'
    table: 'test1'
    key: 'test_new_key'
"""

RETURN = """
result:
  description: result of create/delete table index query.
  returned: when success for state `present/absent`.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError, ReqlAuthError


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(type=int, default=28015),
        user=dict(default="admin"),
        password=dict(default=""),
        ssl=dict(type=dict, default=None),
        state=dict(choices=["present", "absent", "rename"], default="present"),
        database=dict(required=True),
        table=dict(required=True),
        key=dict(required=True),
        new_key=dict(required=False)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    client = RethinkDB()
    _params = {
        "host": module.params["host"],
        "port": module.params["port"],
        "user": module.params["user"],
        "password": module.params["password"],
        "ssl": module.params["ssl"],
    }

    try:
        conn = client.connect(**_params)
        if module.params["state"].lower() == "present":
            _res = (
                client.db(module.params["database"])
                .table(module.params["table"])
                .index_create(module.params["key"])
                .run(conn)
            )
        elif module.params["state"].lower() == "rename":
            _res = (
                client.db(module.params["database"])
                .table(module.params["table"])
                .index_rename(module.params["key"], module.params['new_key'])
                .run(conn)
            )
        else:
            _res = (
                client.db(module.params["database"])
                .table(module.params["table"])
                .index_drop(module.params["key"])
                .run(conn)
            )
        module.exit_json(changed=True, result=_res)
    except ReqlOpFailedError as e:
        if module.params["state"].lower() == "present" and "already exists" in e.message:
            module.exit_json(changed=False, result=e.message)
        elif module.params["state"] == "absent" and "does not exist" in e.message:
            module.exit_json(changed=False, result=e.message)
        else:
            module.fail_json(msg=e.message)
    except ReqlAuthError as e:
        module.fail_json(msg=e.message)
    finally:
        conn.close(noreply_wait=False)


if __name__ == "__main__":
    main()
