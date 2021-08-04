#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: couchdb_db_info
short_description: Get information about Couchdb Database.
description:
  - Get information about Couchdb Database.
  - U(https://docs.couchdb.org/en/stable/api/index.html)
version_added: 0.1.1
options:
  scheme:
    description:
      - http scheme for couchdb.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of couchdb.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of couchdb.
    required: false
    type: str
    default: '5984'
  user:
    description:
      - couchdb username.
    required: false
    type: str
    default: 'admin'
  password:
    description:
      - password for couchdb I(user).
    required: false
    type: str
    default: 'password'
  database:
    description:
      - name of the database.
    required: true
    type: str
  get_db_info:
    description:
      - do you want to fetch database info for I(database)?
    required: false
    type: bool
    default: false
  get_db_explain:
    description:
      - do you want to fetch database explain info for I(database)?
    required: false
    type: bool
    default: false
  get_db_security:
    description:
      - do you want to fetch database security info for I(database)?
    required: false
    type: bool
    default: false
  get_db_shards:
    description:
      - do you want to fetch database shard info for I(database)?
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get database info
  community.missing_collection.couchdb_db_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    get_db_info: true
    database: "_users"

- name: get database explain info
  community.missing_collection.couchdb_db_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    get_db_explain: true
    database: "_users"

- name: get database security info
  community.missing_collection.couchdb_db_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    get_db_security: true
    database: "_users"

- name: get database shards info
  community.missing_collection.couchdb_db_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    get_db_shards: true
    database: "_users"
"""

RETURN = """
database:
  description: get database info from couchdb.
  returned: when I(get_db_info) is defined and success.
  type: dict
  sample: {
      "cluster": {
          "n": 3,
          "q": 8,
          "r": 2,
          "w": 2
      },
      "compact_running": false,
      "db_name": "receipts",
      "disk_format_version": 6,
      "doc_count": 6146,
      "doc_del_count": 64637,
      "instance_start_time": "0",
      "props": {},
      "purge_seq": 0,
      "sizes": {
          "active": 65031503,
          "external": 66982448,
          "file": 137433211
      },
      "update_seq": "292786-g1AAAAF..."
  }
explain:
  description: get database explain from couchdb.
  returned: when I(get_db_explain) is defined and success.
  type: dict
  sample: {
      "dbname": "movies",
      "index": {},
      "selector": {},
      "opts": {},
      "limit": 2,
      "skip": 0,
      "fields": [],
      "range": {}
  }
security:
  description: get members and there permissions in database from couchdb.
  returned: when I(get_db_security) is defined and success.
  type: dict
  sample: {
      "admins": {
          "names": [],
          "roles": []
      },
      "members": {
          "names": [],
          "roles": []
      }
  }
shards:
  description: get shard info of database from couchdb.
  returned: when I(get_db_shards) is defined and success.
  type: dict
  sample: {
      "00000000-7fffffff": ["nonode@nohost"],
      "80000000-ffffffff": ["nonode@nohost"]
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="5984"),
        user=dict(default="admin"),
        password=dict(default="password", no_log=True),
        database=dict(),
        get_db_info=dict(type=bool),
        get_db_explain=dict(type=bool),
        get_db_security=dict(type=bool),
        get_db_shards=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_db_info", True, ["database"]),
            ("get_db_explain", True, ["database"]),
            ("get_db_security", True, ["database"]),
            ("get_db_shards", True, ["database"]),
        ),
        mutually_exclusive=[
            (
                "get_db_info",
                "get_db_explain",
                "get_db_security",
                "get_db_shards",
            )
        ]
    )

    _url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/"

    _auth = (
        module.params["user"],
        module.params["password"]
    )

    headers = {"Content-Type": "application/json"}
    if module.params["get_db_info"]:
        r = requests.get(
            _url + module.params["database"],
            auth=_auth,
            headers=headers
        )
        if r.status_code == 200:
            module.exit_json(database=r.json())
        else:
            module.fail_json(msg=r.json())
    elif module.params["get_db_explain"]:
        r = requests.post(
            _url + module.params["database"] + "/_explain",
            auth=_auth,
            data=module.jsonify({"selector": {}}),
            headers=headers
        )
        if r.status_code == 200:
            module.exit_json(explain=r.json())
        else:
            module.fail_json(msg=r.json())
    elif module.params["get_db_security"]:
        r = requests.get(
            _url + module.params["database"] + "/_security",
            auth=_auth,
            headers=headers
        )
        if r.status_code == 200:
            module.exit_json(security=r.json())
        else:
            module.fail_json(msg=r.json())
    elif module.params["get_db_shards"]:
        r = requests.get(
            _url + module.params["database"] + "/_shards",
            auth=_auth,
            headers=headers
        )
        if r.status_code == 200:
            module.exit_json(shards=r.json()["shards"])
        else:
            module.fail_json(msg=r.json())
    else:
        module.fail_json(msg="unknown parameters are passed")


if __name__ == "__main__":
    main()
