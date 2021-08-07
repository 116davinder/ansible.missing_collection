#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: alertmanager
short_description: Management of the Alertmanager.
description:
  - Management of the Alertmanager.
  - U(https://alertmanager.io/docs/alertmanager/latest/management_api/)
version_added: 0.3.0
options:
  scheme:
    description:
      - http scheme for alertmanager.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of alertmanager.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of alertmanager.
    required: false
    type: str
    default: '9093'
  command:
    description:
      - management command to run.
    required: false
    type: str
    choices: ['reload']
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: reload alertmanager config
  community.missing_collection.alertmanager:
    scheme: 'http'
    host: 'localhost'
    port: '9093'
    command: 'reload'
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="9093"),
        command=dict(choices=["reload"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    _url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/-/" + module.params["command"]

    r = requests.post(_url)
    if r.status_code == 200:
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
