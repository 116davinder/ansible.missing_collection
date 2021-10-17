#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_status
short_description: Get information from Consul (Status).
description:
  - Get information from Consul (Status).
  - U(https://www.consul.io/api-docs/status)
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
  dc:
    description:
      - datacenter for consul.
    required: false
    type: str
    default: ''
  token:
    description:
      - auth token for consul.
    required: false
    type: str
  get_leader:
    description:
      - get information about current leader.
    required: false
    type: bool
  get_peers:
    description:
      - get information about all the peers.
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get current leader information
  consul_status:
    get_leader: true

- name: get current perrs information
  consul_status:
    get_peers: true
"""

RETURN = """
result:
  description: result from the consul api.
  returned: when success.
  type: str/list
  sample: "10.1.10.12:8300"
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="8500"),
        token=dict(),
        dc=dict(default=""),
        get_leader=dict(type=bool),
        get_peers=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    _url = (
        module.params["scheme"]
        + "://"
        + module.params["host"]
        + ":"
        + module.params["port"]
        + "/v1/status/"
    )
    params = {"dc": module.params["dc"]}
    headers = {"Content-Type": "application/json"}
    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    if module.params["get_leader"]:
        resp = requests.get(_url + "leader", headers=headers, params=params)
    elif module.params["get_peers"]:
        resp = requests.get(_url + "peers", headers=headers, params=params)
    else:
        module.fail_json("unknown options")
    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
