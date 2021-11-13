#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_health
short_description: Get information from Consul (Health).
description:
  - Get information from Consul (Health).
  - U(https://www.consul.io/api-docs/health)
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
  node:
    description:
      - Specifies the name or ID of the node to query.
      - required when I(get_node_health).
    required: false
    type: str
  dc:
    description:
      - datacenter for consul.
    required: false
    type: str
    default: ''
  filter:
    description:
      - Specifies the expression used to filter the queries results prior to returning the data.
    required: false
    type: str
    default: ''
  ns:
    description:
      - Specifies the namespace to list checks.
      - Only works when B(consul enterprise).
    required: false
    type: str
  token:
    description:
      - auth token for consul.
    required: false
    type: str
  get_node_health:
    description:
      - This endpoint returns the checks specific to the node provided on the path.
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get health of given node
  consul_health:
    get_node_health: true
    node: "server-1"
    dc: "dc1"
"""

RETURN = """
result:
  description: result from the consul api.
  returned: when success.
  type: list
  sample: [
    {
        "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
        "Node": "foobar",
        "CheckID": "serfHealth",
        "Name": "Serf Health Status",
        "Status": "passing",
        "Notes": "",
        "Output": "",
        "ServiceID": "",
        "ServiceName": "",
        "ServiceTags": [],
        "Namespace": "default"
    },
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="8500"),
        token=dict(),
        node=dict(),
        dc=dict(default=""),
        filter=dict(default=""),
        ns=dict(),
        get_node_health=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=(("get_node_health", True, ["node"]),)
    )

    _url = (
        module.params["scheme"]
        + "://"
        + module.params["host"]
        + ":"
        + module.params["port"]
        + "/v1/health/"
    )
    params = {
        "dc": module.params["dc"],
        "filter": module.params["filter"],
    }
    headers = {"Content-Type": "application/json"}

    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    if module.params["ns"] is not None:
        params["ns"] = module.params["ns"]

    if module.params["get_node_health"]:
        _url = _url + "/node/" + module.params["node"]
        resp = requests.get(_url, headers=headers, params=params)
    else:
        module.fail_json("unknown options")

    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
