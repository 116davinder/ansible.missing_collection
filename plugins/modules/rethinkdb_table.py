#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_table
short_description: Create/Delete RethinkDB Table.
description:
  - Create/Delete RethinkDB Table.
  - U(https://rethinkdb.com/api/python/)
version_added: 0.2.0
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
    choices: ['present', 'absent']
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
  primary_key:
    description:
      - name of the primary key.
    required: false
    type: str
    default: 'id'
  durability:
    description:
      - if set to soft, writes will be acknowledged by the server immediately and flushed to disk in the background.
      - The default is hard: acknowledgment of writes happens after data has been written to disk.
    required: false
    type: str
    choices: ['soft', 'hard']
    default: 'hard'
  shards:
    description:
      - number of shards.
    required: false
    type: int
    default: 1
  replicas:
    description:
      - number of replicas.
    required: false
    type: int
    default: 1
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: create table in rethinkdb
  community.missing_collection.rethinkdb_table:
    host: "localhost"
    port: 28015
    user: 'admin'
    password: ''
    state: present
    database: 'database1'
    table: 'table1'

- name: delete table in rethinkdb
  community.missing_collection.rethinkdb_table:
    host: "localhost"
    port: 28015
    user: 'admin'
    password: ''
    state: absent
    database: 'database1'
    table: 'table1'
"""

RETURN = """
result:
  description: result of create/delete table query.
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
        password=dict(default="", no_log=True),
        ssl=dict(type=dict, default=None),
        state=dict(choices=["present", "absent"], default="present"),
        database=dict(required=True),
        table=dict(required=True),
        primary_key=dict(default="id"),
        durability=dict(choices=["soft", "hard"], default="hard"),
        shards=dict(type=int, default=1),
        replicas=dict(type=int, default=1),
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
                .table_create(
                    module.params["table"],
                    primary_key=module.params["primary_key"],
                    durability=module.params["durability"],
                    shards=module.params["shards"],
                    replicas=module.params["replicas"],
                )
                .run(conn)
            )
        else:
            _res = (
                client.db(module.params["database"])
                .table_drop(module.params["table"])
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
