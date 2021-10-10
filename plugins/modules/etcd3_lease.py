#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: etcd3_lease
short_description: Manage Lease in ETCD Cluster.
description:
  - Manage Lease in ETCD Cluster.
  - U(https://python-etcd3.readthedocs.io/en/latest/usage.html)
version_added: 0.4.0
options:
  id:
    description:
      - id of lease.
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
  ttl:
    description:
      - number of seconds for lease.
    required: false
    type: int
    default: 1000
  state:
    description:
      - do you want to create or delete the lease?
    required: false
    type: str
    choices: ["present", "absent"]
    default: "present"
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - etcd3
"""

EXAMPLES = """
- name: create lease in etcd for 1000 seconds
  community.missing_collection.etcd3_lease:
    host: "localhost"
    port: 2379
    ttl: 1000
    state: "present"
  register: __

- name: revoke lease in etcd
  community.missing_collection.etcd3_lease:
    host: "localhost"
    port: 2379
    id: "{{ __.id }}"
    state: "absent"
"""

RETURN = """
id:
  description: id of lease.
  returned: when I(ttl) is defined and I(state) == "present".
  type: int
  sample: 7587857742833949726
hex_id:
  description: hex id of lease.
  returned: when I(ttl) is defined and I(state) == "present".
  type: str
  sample: 694d7c6a37d09c24
"""

from ansible.module_utils.basic import AnsibleModule
import etcd3


def main():
    module = AnsibleModule(
        argument_spec=dict(
            id=dict(type=int),
            host=dict(default="localhost"),
            port=dict(type=int, default=2379),
            user=dict(default=None),
            password=dict(default=None, no_log=True),
            ttl=dict(type=int, default=1000),
            state=dict(choices=["present", "absent"], default="present"),
        ),
        required_together=[["user", "password"]],
    )

    etcd = etcd3.client(
        host=module.params["host"],
        port=module.params["port"],
        user=module.params["user"],
        password=module.params["password"],
    )

    try:
        if module.params["state"].lower() == "present":
            resp = etcd.lease(module.params["ttl"])
            module.exit_json(changed=True, id=resp.id, hex_id=hex(resp.id)[2:])
        elif module.params["state"].lower() == "absent":
            resp = etcd.revoke_lease(module.params["id"])
            module.exit_json(changed=True)
        else:
            module.fail_json(msg="unknown parameters")
    except Exception as error:
        module.fail_json(error=error)
    finally:
        etcd.close()


if __name__ == "__main__":
    main()
