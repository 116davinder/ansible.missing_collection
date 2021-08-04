#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: couchdb_db
short_description: Create/Delete Couchdb Database.
description:
  - Create/Delete Couchdb Database.
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
  state:
    description:
      - state of the database.
    required: false
    type: str
    choices: ['present', 'absent']
    default: 'present'
  database:
    description:
      - name of the database.
    required: true
    type: str
  shards:
    description:
      - number of shards for I(database).
    required: false
    type: int
    default: 8
  replicas:
    description:
      - number of replicas for I(database).
    required: false
    type: int
    default: 3
  partitioned:
    description:
      - do you want to create partitioned database?
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create database in couchdb
  community.missing_collection.couchdb_db:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    state: 'present'
    database: 'test1'

- name: delete database in couchdb
  community.missing_collection.couchdb_db:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    state: 'absent'
    database: 'test1'
"""

RETURN = """
result:
  description: result of the api request.
  returned: when success.
  type: dict
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
        state=dict(choices=["present", "absent"], default="present"),
        database=dict(required=True),
        shards=dict(type=int, default=8),
        replicas=dict(type=int, default=3),
        partitioned=dict(type=bool, default=False)
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    _auth = (
        module.params["user"],
        module.params["password"]
    )

    _url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/" + module.params["database"]

    headers = {"Content-Type": "application/json"}
    if module.params["state"].lower() == "present":
        _params = {
            "q": module.params["shards"],
            "n": module.params["replicas"]
        }
        if module.params["partitioned"]:
            _params["partitioned"] = "true"
        r = requests.put(
            _url,
            auth=_auth,
            params=_params,
            headers=headers
        )
        if r.status_code == 201:
            module.exit_json(changed=True, result=r.json())
        elif r.status_code == 412:
            module.exit_json(changed=False, result=r.json())
        else:
            module.fail_json(msg=r.json())
    else:
        r = requests.delete(
            _url,
            auth=_auth,
            headers=headers
        )
        if r.status_code == 200:
            module.exit_json(changed=True, result=r.json())
        elif r.status_code == 404:
            module.exit_json(changed=False, result=r.json())
        else:
            module.fail_json(msg=r.json())


if __name__ == "__main__":
    main()
