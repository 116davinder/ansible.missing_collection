#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_db
short_description: Create/Delete RethinkDB Database.
description:
  - Create/Delete RethinkDB Database.
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
    type: bool
    default: None
  state:
    description:
      - state of database.
    required: false
    type: str
    choices: ['present', 'absent']
    default: 'present'
  database:
    description:
      - name of the database.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: create database in rethinkdb
  community.missing_collection.rethinkdb_db:
    host: "localhost"
    port: 28015
    user: 'admin'
    password: ''
    state: present
    database: "test1"

- name: delete database in rethinkdb
  community.missing_collection.rethinkdb_db:
    host: "localhost"
    port: 28015
    user: 'admin'
    password: ''
    state: absent
    database: "test1"
"""

RETURN = """
result:
  description: result of create/delete database query.
  returned: when success for state `present/absent`.
  type: dict
  sample: {
    "config_changes": [
      {
        "new_val": null,
        "old_val": {
          "id": "415f922c-a2c0-43af-b7ba-5514b3ebf32c",
          "name": "test1"
        }
      }
    ],
    "dbs_dropped": 1,
    "tables_dropped": 0
  }
error:
  description: error message
  returned: when failure for state `present/absent`.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
import json
from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(required=False, type=int, default=28015),
        user=dict(required=False, default='admin'),
        password=dict(required=False, default=''),
        ssl=dict(required=False, default=None),
        state=dict(
            required=False,
            choices=['present', 'absent'],
            default='present'
        ),
        database=dict(required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    client = RethinkDB()
    conn = client.connect(
        host=module.params['host'],
        port=module.params['port'],
        user=module.params['user'],
        password=module.params['password'],
        ssl=module.params['ssl']
    )
    try:
        if module.params['state'].lower() == 'present':
            _res = client.db_create(module.params['database']).run(conn)
        else:
            _res = client.db_drop(module.params['database']).run(conn)
        module.exit_json(changed=True, result=_res)
    except ReqlOpFailedError as e:
        if module.params['state'].lower() == 'present' and "already exists" in e.message:
            module.exit_json(changed=False, result=e.message)
        elif module.params['state'] == 'absent' and "does not exist" in e.message:
            module.exit_json(changed=False, result=e.message)
        else:
            module.fail_json(error=e.message)
    conn.close(noreply_wait=False)


if __name__ == '__main__':
    main()
