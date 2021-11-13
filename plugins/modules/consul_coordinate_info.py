#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_coordinate_info
short_description: Get information from Consul (Coordinate).
description:
  - Get information from Consul (Coordinate).
  - U(https://www.consul.io/api-docs/coordinate)
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
      - required when I(get_lan_node).
    required: false
    type: str
  dc:
    description:
      - datacenter for consul.
    required: false
    type: str
    default: ''
  segment:
    description:
      - B(Enterprise) Specifies the segment to list members for.
    required: false
    type: str
  token:
    description:
      - auth token for consul.
    required: false
    type: str
  get_wan_datacenter:
    description:
      - This endpoint returns the WAN network coordinates for all Consul servers,
      - organized by datacenter.
    required: false
    type: bool
  get_lan_datacenter:
    description:
      - This endpoint returns the LAN network coordinates for all nodes in a given datacenter.
      - This will default to the datacenter of the agent being queried.
    required: false
    type: bool
  get_lan_node:
    description:
      - This endpoint returns the LAN network coordinates for the given node.
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get wan datacenter coordinates
  community.missing_collection.consul_coordinate_info:
    get_wan_datacenter: true
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"

- name: get lan datacenter coordinates
  community.missing_collection.consul_coordinate_info:
    get_lan_datacenter: true
    dc: "dc1"
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"

- name: get lan node coordinates
  community.missing_collection.consul_coordinate_info:
    get_lan_node: true
    dc: "dc1"
    node: "consul-server1"
    token: "7661077f-3b6b-f763-6330-eedd2c3a442b"
"""

RETURN = """
result:
  description: result from the consul api.
  returned: when success.
  type: list
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
        segment=dict(),
        get_wan_datacenter=dict(type=bool),
        get_lan_datacenter=dict(type=bool),
        get_lan_node=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=(("get_lan_node", True, ["node"]),)
    )

    _url = (
        module.params["scheme"]
        + "://"
        + module.params["host"]
        + ":"
        + module.params["port"]
        + "/v1/coordinate/"
    )
    params = {}
    headers = {"Content-Type": "application/json"}

    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    if module.params["segment"] is not None:
        params["segment"] = module.params["segment"]

    if module.params["get_wan_datacenter"]:
        _url = _url + "datacenters"
    elif module.params["get_lan_datacenter"]:
        params["dc"] = module.params["dc"]
        _url = _url + "nodes"
    elif module.params["get_lan_node"]:
        params["dc"] = module.params["dc"]
        _url = _url + "node/" + module.params["node"]
    else:
        module.fail_json("unknown options are passed")

    resp = requests.get(_url, headers=headers, params=params)
    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
