#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_policy_info
short_description: Get information from Consul (ACL Policy).
description:
  - Get information from Consul (ACL Policy).
  - U(https://www.consul.io/api-docs/acl/policies)
version_added: 0.4.0
options:
  scheme:
    description:
      - http scheme for consul.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of consul.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of consul.
    required: false
    type: str
    default: '8500'
  name:
    description:
      - the name of the acl policy.
    required: false
    type: str
  id:
    description:
      - id of the acl policy.
    required: false
    type: str
  ns:
    description:
      - B(Enterprise) the namespace to lookup the policy.
    required: false
    type: str
  token:
    description:
      - auth token for consul.
    required: false
    type: str
  get_all_policies:
    description:
      - This endpoint lists all the ACL policies.
    required: false
    type: bool
  get_policy:
    description:
      - This endpoint reads an ACL policy with the given I(id) or I(name).
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all policies
  community.missing_collection.consul_policy_info:
    get_all_policies: true
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"

- name: get policy by name
  community.missing_collection.consul_policy_info:
    get_policy: true
    name: "global-management"
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"

- name: get policy by id
  community.missing_collection.consul_policy_info:
    get_policy: true
    id: "00000000-0000-0000-0000-000000000001"
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"
"""

RETURN = """
result:
  description: result from the consul api.
  returned: when success.
  type: list/dict
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="8500"),
        token=dict(),
        name=dict(),
        id=dict(),
        ns=dict(),
        get_all_policies=dict(type=bool),
        get_policy=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ("name", "id"),
        ],
    )

    _url = (
        module.params["scheme"]
        + "://"
        + module.params["host"]
        + ":"
        + module.params["port"]
        + "/v1/acl/"
    )
    params = {}
    headers = {"Content-Type": "application/json"}

    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    if module.params["ns"] is not None:
        params["ns"] = module.params["ns"]

    if module.params["get_all_policies"]:
        _url = _url + "policies"
    elif module.params["get_policy"]:
        if module.params["name"] is not None:
            _url = _url + "policy/name/" + module.params["name"]
        else:
            _url = _url + "policy/" + module.params["id"]
    else:
        module.fail_json("unknown options are passed")

    resp = requests.get(_url, headers=headers, params=params)
    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
