#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: zookeeper_info
short_description: Get Information about Zookeeper Instance.
description:
  - Get Information about Zookeeper Instance using Admin Server Rest API.
version_added: 0.2.0
options:
  url:
    description:
      - url of zookeeper admin server.
      - example: http://localhost:8080
    required: true
    type: string
  command:
    description:
      - zookeeper admin server command to fetch metrics.
      - example: stats
    required: false
    type: string
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
'''

EXAMPLES = '''
- name: fetch list of zookeeper commands
  community.missing_collection.zookeeper_info:
    url: http://localhost:8080

- name: fetch stats of zookeeper
  community.missing_collection.zookeeper_info:
    url: http://localhost:8080
    command: stats
'''

RETURN = """
commands:
  description: list of zookeeper admin server commands.
  returned: when no args and success.
  type: str
output:
  description: output of given zookeeper admin server command.
  returned: when I(command) is defined and success.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():

    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type='str', required=True),
            command=dict(type='str', default=None, required=False),
        )
    )

    if module.params['command'] is None:
        complete_url = module.params['url'] + "/commands"
    else:
        complete_url = module.params['url'] + "/commands/" + module.params['command']

    r = requests.get(complete_url)

    if r.status_code == 200:
        if module.params['command'] is None:
            module.exit_json(commands=r.text)
        else:
            module.exit_json(output=r.json())
    else:
        module.fail_json(msg=r.json())


if __name__ == '__main__':
    main()
