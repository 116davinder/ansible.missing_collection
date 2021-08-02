#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_table_info
short_description: Get information about RethinkDB Table.
description:
  - Get information about RethinkDB Table.
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
    required: true
    type: str
  table:
    description:
      - name of the table.
    required: true
    type: str
  index_name:
    description:
      - name of the secondard index.
      - can be used together with I(index_status).
    required: true
    type: str
    default: None
  index_list:
    description:
      - do you want to get list of indexes for given I(table)?
    required: false
    type: bool
  index_status:
    description:
      - do you want to get information of the index for given I(table)?
    required: false
    type: bool
  get_write_hook:
    description:
      - do you want to get information for given I(table)?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: get secondary indexes list in rethinkdb
  community.missing_collection.rethinkdb_table_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    database: 'test'
    table: 'test1'
    index_list: true

- name: get status of all secondary index in rethinkdb
  community.missing_collection.rethinkdb_table_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    database: 'test'
    table: 'test1'
    index_status: true

- name: get status of given secondary index in rethinkdb
  community.missing_collection.rethinkdb_table_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    database: 'test'
    table: 'test1'
    index_status: true
    index_name: 'test_id'

- name: get write hook details in rethinkdb
  community.missing_collection.rethinkdb_table_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    database: 'test'
    table: 'test1'
    get_write_hook: true
"""

RETURN = """
indexes:
  description: list of all secondary indexes.
  returned: when `index_list` is defined.
  type: list
  sample: ["sec_id", "test_id"]
statuses:
  description: status of all secondary indexes.
  returned: when `index_status` is defined.
  type: list
  sample: [
    {
      "function": "xxxxxxx",
      "geo": false,
      "index": "sec_id",
      "multi": false,
      "outdated": false,
      "query": "indexCreate(xxx)",
      "ready": true
    },
    {
      "function": "xxxxx",
      "geo": false,
      "index": "test_id",
      "multi": false,
      "outdated": false,
      "query": "indexCreate(xxx)",
      "ready": true
    }
  ]
status:
  description: status of given secondary index.
  returned: when `index_status` and `index_name` is defined.
  type: dict
  sample: {
    "function": <binary>,
    "geo": false,
    "index": "test_id",
    "multi": false,
    "outdated": false,
    "query": "indexCreate(xxx)",
    "ready": true
  }
write_hook:
  description: status of write_hook of given table.
  returned: when `get_write_hook` is defined.
  type: dict
  sample: {
    "function": <binary>,
    "query": "setWriteHook(xxxxx)",
  }
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
        database=dict(required=True),
        table=dict(required=True),
        index_name=dict(required=False, default=None),
        index_list=dict(type=bool),
        index_status=dict(type=bool),
        get_write_hook=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            (
                'index_list',
                'index_status',
                'get_write_hook'
            )
        ],
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
        if module.params["index_list"]:
            _res = (
                client.db(module.params["database"])
                .table(module.params["table"])
                .index_list()
                .run(conn)
            )
            module.exit_json(indexes=_res)
        elif module.params["index_status"]:
            if module.params['index_name'] is None:
                _res = (
                    client.db(module.params["database"])
                    .table(module.params["table"])
                    .index_status()
                    .run(conn)
                )
                module.exit_json(statuses=_res)
            else:
                _res = (
                    client.db(module.params["database"])
                    .table(module.params["table"])
                    .index_status(module.params["index_name"])
                    .run(conn)
                )
            module.exit_json(status=_res)
        else:
            _res = (
                client.db(module.params["database"])
                .table(module.params["table"])
                .get_write_hook()
                .run(conn)
            )
            if _res is None:
                _res = {}
            module.exit_json(write_hook=_res)
    except ReqlOpFailedError as e:
        module.fail_json(msg=e.message)
    except ReqlAuthError as e:
        module.fail_json(msg=e.message)
    finally:
        conn.close(noreply_wait=False)


if __name__ == "__main__":
    main()
