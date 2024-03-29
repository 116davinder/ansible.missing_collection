#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: etcd3_info
short_description: Get Information from ETCD Cluster.
description:
  - Get Information from ETCD Cluster.
  - U(https://python-etcd3.readthedocs.io/en/latest/usage.html)
version_added: 0.4.0
options:
  key:
    description:
      - key to lookup in etcd database
    required: false
    type: str
  id:
    description:
      - lease id
    required: false
    type: int
  host:
    description:
      - host/ip of etcd node.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number for etcd node.
    required: true
    type: int
    default: 2379
  user:
    description:
      - username for etcd node if authentication is enabled.
    required: false
    type: str
    default: None
  password:
    description:
      - password for etcd node if authentication is enabled.
    required: false
    type: str
    default: None
  get_value:
    description:
      - get value of given I(key).
    required: false
    type: bool
  get_status:
    description:
      - get status from connected node.
    required: false
    type: bool
  get_lease_status:
    description:
      - get lease status for given I(id).
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - etcd3
"""

EXAMPLES = """
- name: get value of key
  community.missing_collection.etcd3_info:
    host: "localhost"
    port: 2379
    get_value: true
    key: '/Test'

- name: get status of current etcd node
  community.missing_collection.etcd3_info:
    host: "localhost"
    port: 2379
    get_status: true

- name: get lease status of given id
  community.missing_collection.etcd3_info:
    host: "localhost"
    port: 2379
    get_lease_status: true
    id: "7587857742833949726"
"""

RETURN = """
value:
  description: get value of given key
  returned: when I(get_value) and success.
  type: str
  sample: "bar"
status:
  description: get status from etcd node
  returned: when I(get_status) and success.
  type: dict
  sample: {"db_size": 20480, "leader": {"id": 10276657743932975437, "name": "default"}, "raft_index": 11, "version": "3.5.0"}
lease_status:
  description: get status of given lease id
  returned: when I(get_lease_status) and success.
  type: dict
  sample: {"granted_ttl": 1000, "keys": ["/Test4"], "ttl": 655}
"""

from ansible.module_utils.basic import AnsibleModule
import etcd3


def main():
    module = AnsibleModule(
        argument_spec=dict(
            key=dict(),
            id=dict(type=int),
            host=dict(default="localhost"),
            port=dict(type=int, default=2379),
            user=dict(default=None),
            password=dict(default=None, no_log=True),
            get_value=dict(type=bool),
            get_status=dict(type=bool),
            get_lease_status=dict(type=bool),
        ),
        required_together=[["user", "password"]],
        required_if=(
            ("get_value", True, ["key"]),
            ("get_lease_status", True, ["id"]),
        ),
    )

    etcd = etcd3.client(
        host=module.params["host"],
        port=module.params["port"],
        user=module.params["user"],
        password=module.params["password"],
    )

    try:
        if module.params["get_value"]:
            resp = etcd.get(module.params["key"])
            module.exit_json(value=resp[0].decode("utf-8"))
        elif module.params["get_status"]:
            resp = etcd.status()
            module.exit_json(
                status={
                    "db_size": resp.db_size,
                    "version": resp.version,
                    "raft_index": resp.raft_index,
                    "leader": {"id": resp.leader.id, "name": resp.leader.name},
                }
            )
        elif module.params["get_lease_status"]:
            resp = etcd.get_lease_info(module.params["id"])
            module.exit_json(
                lease_status={
                    "ttl": resp.TTL,
                    "granted_ttl": resp.grantedTTL,
                    "keys": [k.decode("utf-8") for k in resp.keys],
                }
            )
        else:
            module.fail_json(msg="unknown parameters")
    except Exception as error:
        module.fail_json(msg=error)
    finally:
        etcd.close()


if __name__ == "__main__":
    main()
