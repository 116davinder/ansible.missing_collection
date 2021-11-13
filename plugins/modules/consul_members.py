#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_members
short_description: Get information from Consul (Members).
description:
  - Get information from Consul (Members).
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
  token:
    description:
      - auth token for consul.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get current memebers list
  consul_members:
"""

RETURN = """
result:
  description: result from the consul api.
  returned: when success.
  type: list
  sample: [{"Name":"server-1","Addr":"172.17.0.2","Port":8301,"Tags":{"acls":"0","bootstrap":"1","build":"1.10.3:c976ffd2","dc":"dc1","ft_fs":"1","ft_si":"1","id":"61f18701-87ca-2e73-891d-16424997022a","port":"8300","raft_vsn":"3","role":"consul","segment":"","vsn":"2","vsn_max":"3","vsn_min":"2","wan_join_port":"8302"},"Status":1,"ProtocolMin":1,"ProtocolMax":5,"ProtocolCur":2,"DelegateMin":2,"DelegateMax":5,"DelegateCur":4}]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="8500"),
        token=dict(),
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
        + "/v1/agent/members"
    )
    headers = {"Content-Type": "application/json"}
    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    resp = requests.get(_url, headers=headers)
    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
