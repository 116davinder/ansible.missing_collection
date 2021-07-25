#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: orientdb_db
short_description: Create/Delete OrientDB 2.x Database.
description:
  - Create/Delete OrientDB 2.x Database.
  - U(https://orientdb.org/docs/3.0.x/pyorient/PyOrient-Client.html)
version_added: 0.1.1
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
  type:
    description:
      - type of the database.
    required: false
    type: str
    choices: ['document', 'graph']
    default: 'document'
  storage_type:
    description:
      - storage type of the database.
    required: false
    type: str
    choices: ['plocal', 'memory']
    default: 'plocal'
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - pyorient
"""

EXAMPLES = """
- name: create database in orientdb
  orientdb_db:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    state: present
    database: 'test1'

- name: create graph database in orientdb
  community.missing_collection.orientdb_db:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    state: present
    database: 'test2'
    type: 'graph'
    storage_type: 'memory'

- name: delete database in orientdb
  community.missing_collection.orientdb_db:
    host: 'localhost'
    port: 2424
    user: 'root'
    password: 'root'
    state: absent
    database: '{{ item }}'
  loop:
    - 'test1'
    - 'test2'
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
from pyorient import OrientDB
from pyorient.exceptions import PyOrientDatabaseException
from pyorient.exceptions import PyOrientCommandException


def main():
    argument_spec = dict(
        host=dict(required=True),
        port=dict(required=False, type=int, default=2424),
        user=dict(required=False, default="root"),
        password=dict(required=False, default="root"),
        state=dict(required=False, choices=["present", "absent"], default="present"),
        database=dict(required=True),
        type=dict(choices=["document", "graph"], default="document"),
        storage_type=dict(choices=["plocal", "memory"], default="plocal")
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    client = OrientDB(
        host=module.params["host"],
        port=module.params["port"]
    )

    try:
        session_id = client.connect(
            user=module.params["user"],
            password=module.params["password"]
        )

        if module.params["state"].lower() == "present":
            client.db_create(
                name=module.params["database"],
                type=module.params["type"],
                storage=module.params["storage_type"]
            )
        else:
            client.db_drop(module.params["database"])
        module.exit_json(changed=True)
    except PyOrientDatabaseException as e:
        if "already exists" in str(e):
            module.exit_json(changed=False, result=str(e))
    except PyOrientCommandException as e:
        if "does not exist" in str(e):
            module.exit_json(changed=False, result=str(e))
    finally:
        client.db_close()


if __name__ == "__main__":
    main()
