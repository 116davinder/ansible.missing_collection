#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: consul_namespaces_info
short_description: Get information from Consul Enterprise (Namespaces).
description:
  - Get information from Consul Enterprise (Namespaces).
  - U(https://www.consul.io/api-docs/namespaces)
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
  namespace:
    description:
      - name of consul namespace.
    required: false
    type: str
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
- name: get list of namespaces
  community.missing_collection.consul_namespaces_info:

- name: get details of given namespace
  community.missing_collection.consul_namespaces_info:
    namespace: "default"
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
        namespace=dict(aliases=["ns"]),
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
        + "/v1/"
    )
    headers = {"Content-Type": "application/json"}

    if module.params["token"] is not None:
        headers["Authorization"] = f"Bearer {module.params['token']}"
    if module.params["namespace"] is None:
        _url = _url + "namespaces"
    else:
        _url = _url + "namespace/" + module.params["namespace"]

    resp = requests.get(_url, headers=headers)
    if resp.status_code == 200:
        module.exit_json(result=resp.json())
    else:
        module.fail_json(msg=resp.text, code=resp.status_code)


if __name__ == "__main__":
    main()
