#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: rethinkdb_admin_info
short_description: Get information from RethinkDB Database.
description:
  - Get information from RethinkDB Database.
  - U(https://rethinkdb.com/docs/system-tables/#overview)
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
  table:
    description:
      - name of the system table.
    required: false
    type: str
    choices: [
      'table_config',
      'server_config',
      'db_config',
      'cluster_config',
      'table_status',
      'server_status',
      'current_issues',
      'users',
      'permissions',
      'jobs',
      'stats',
      'logs'
    ]
    default: 'server_status'
  limit:
    description:
      - limit number of results to fetch.
    required: true
    type: int
    default: 10
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - rethinkdb
"""

EXAMPLES = """
- name: get server status from rethinkdb
  community.missing_collection.rethinkdb_admin_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    table: 'server_status'

- name: get user list from rethinkdb
  community.missing_collection.rethinkdb_admin_info:
    host: 'localhost'
    port: 28015
    user: 'admin'
    password: ''
    table: 'users'
"""

RETURN = """
result:
  description: result of the database query.
  returned: when success.
  type: list
  sample: [{
    "id": "f3389b47-3a78-4108-b85e-45cd06bcc69a",
    "name": "555e32d208e5_mgu",
    "network": {
      "canonical_addresses": [{
        "host": "127.0.0.1",
        "port": 29015
      }, {
        "host": "172.17.0.2",
        "port": 29015
      }],
      "cluster_port": 29015,
      "connected_to": {},
      "hostname": "555e32d208e5",
      "http_admin_port": 8080,
      "reql_port": 28015,
      "time_connected": "2021-07-20T16:35:58.725000+00:00"
    },
    "process": {
      "argv": ["rethinkdb", "--bind", "all"],
      "cache_size_mb": 11712.3125,
      "pid": 1,
      "time_started": "2021-07-20T16:35:58.723000+00:00",
      "version": "rethinkdb 2.4.1~0buster (CLANG 7.0.1 (tags/RELEASE_701/final))"
    }
  }]
"""

from ansible.module_utils.basic import AnsibleModule
import json
from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError, ReqlAuthError
from rethinkdb.net import DefaultCursorEmpty


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(required=False, type=int, default=28015),
        user=dict(required=False, default='admin'),
        password=dict(required=False, default=''),
        ssl=dict(required=False, type=dict, default=None),
        table=dict(
            required=False,
            choices=[
                'table_config',
                'server_config',
                'db_config',
                'cluster_config',
                'table_status',
                'server_status',
                'current_issues',
                'users',
                'permissions',
                'jobs',
                'stats',
                'logs'
            ],
            default='server_status'
        ),
        limit=dict(required=False, type=int, default=10)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    client = RethinkDB()
    _params = {
        'host': module.params['host'],
        'port': module.params['port'],
        'user': module.params['user'],
        'password': module.params['password'],
        'ssl': module.params['ssl'],
        'db': 'rethinkdb'
    }
    __res = []

    try:
        conn = client.connect(**_params)
        _res = client.table(module.params['table']).limit(module.params['limit']).run(conn)
        while True:
            try:
                __res.append(_res.next())
            except DefaultCursorEmpty as e:
                break
        module.exit_json(result=__res)
    except (ReqlAuthError, ReqlOpFailedError) as e:
        module.fail_json(msg=e.message)
    finally:
        conn.close(noreply_wait=False)


if __name__ == '__main__':
    main()
