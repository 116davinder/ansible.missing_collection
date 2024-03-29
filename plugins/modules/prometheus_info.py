#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: prometheus_info
short_description: Get information from Prometheus.
description:
  - Get information from Prometheus.
  - U(https://prometheus.io/docs/prometheus/latest/management_api/)
version_added: 0.3.0
options:
  scheme:
    description:
      - http scheme for prometheus.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of prometheus.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of prometheus.
    required: false
    type: str
    default: '9090'
  user:
    description:
      - prometheus username.
      - dont define I(user) & I(password) if prometheus have authentication.
    required: false
    type: str
    default: ''
  password:
    description:
      - password for prometheus I(user).
      - dont define I(user) & I(password) if prometheus have authentication.
    required: false
    type: str
    default: ''
  command:
    description:
      - management command to run.
    required: false
    type: str
    choices: ['healthy', 'ready']
    default: 'healthy'
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get health of prometheus
  community.missing_collection.prometheus_info:
    scheme: 'http'
    host: 'localhost'
    port: '9090'
    command: 'healthy'

- name: get ready of prometheus
  community.missing_collection.prometheus_info:
    scheme: 'http'
    host: 'localhost'
    port: '9090'
    command: 'ready'
"""

RETURN = """
result:
  description: result of the api request.
  returned: when success.
  type: str
  sample: "Prometheus is Healthy."
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="9090"),
        user=dict(default=""),
        password=dict(default="", no_log=True),
        command=dict(choices=["healthy", "ready"], default="healthy"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    if module.params["user"] != "" and module.params["password"] != "":
        _auth = (
            module.params["user"],
            module.params["password"]
        )
    else:
        _auth = None

    _url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/-/" + module.params["command"]

    r = requests.get(_url, auth=_auth)
    if r.status_code == 200:
        module.exit_json(result=r.text)
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
