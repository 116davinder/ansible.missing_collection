#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_admin
short_description: Admin Operations of RethinkDB Database/Table.
description:
  - Manual Rebalance of Database/Table Trigger.
  - Reconfigure Shards/Replicas of Database/Table.
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
  command:
    description:
      - name of the admin command.
    required: false
    type: str
    choices: [
      'rebalance',
      'reconfigure'
    ]
  database:
    description:
      - name of the database
    required: true
    type: str
  table:
    description:
      - name of the database table
      - if I(table) is set then I(command) will run on specified table only.
    required: false
    type: str
  replicas:
    description:
      - number of replicas.
      - it can't be more than number of servers in cluster.
    required: false
    type: int
  shards:
    description:
      - number of shards.
      - it can't be more than 64.
      - U(https://rethinkdb.com/api/python/reconfigure)
    required: false
    type: int

author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: rebalance database
  community.missing_collection.rethinkdb_admin:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    command: 'rebalance'
    database: 'database1'

- name: rebalance given table of database only
  community.missing_collection.rethinkdb_admin:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    command: 'rebalance'
    database: 'database1'
    table: 'table1'

- name: reconfigure database
  community.missing_collection.rethinkdb_admin:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    command: 'reconfigure'
    database: 'database2'
    shards: 3
    replicas: 1

- name: reconfigure given table of database only
  community.missing_collection.rethinkdb_admin:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    command: 'reconfigure'
    database: 'database2'
    table: 'table1'
    shards: 4
    replicas: 1
"""

RETURN = """
result:
  description: result of the database admin command.
  returned: when success.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError, ReqlAuthError


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(required=False, type=int, default=28015),
        user=dict(required=False, default="admin"),
        password=dict(required=False, default="", no_log=True),
        ssl=dict(required=False, type=dict, default=None),
        command=dict(required=False, choices=["rebalance", "reconfigure"]),
        database=dict(required=True),
        table=dict(required=False),
        shards=dict(required=False, type=int),
        replicas=dict(required=False, type=int),
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
        "db": "rethinkdb",
    }

    try:
        conn = client.connect(**_params)

        if module.params["command"].lower() == "rebalance":
            if module.params["table"] is None:
                _res = client.db(module.params["database"]).rebalance().run(conn)
            else:
                _res = (
                    client.db(module.params["database"])
                    .table(module.params["table"])
                    .rebalance()
                    .run(conn)
                )
            if "rebalanced" in _res and _res["rebalanced"] > 0:
                module.exit_json(changed=True, result=_res)
            else:
                module.exit_json(result=_res)
        elif module.params["command"].lower() == "reconfigure":
            if module.params["table"] is None:
                _res = (
                    client.db(module.params["database"])
                    .reconfigure(
                        shards=module.params["shards"],
                        replicas=module.params["replicas"],
                    )
                    .run(conn)
                )
            else:
                _res = (
                    client.db(module.params["database"])
                    .table(module.params["table"])
                    .reconfigure(
                        shards=module.params["shards"],
                        replicas=module.params["replicas"],
                    )
                    .run(conn)
                )
            module.exit_json(changed=True, result=_res)

    except (ReqlAuthError, ReqlOpFailedError) as e:
        module.fail_json(msg=e.message)
    finally:
        conn.close(noreply_wait=False)


if __name__ == "__main__":
    main()
