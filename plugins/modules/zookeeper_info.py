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
version_added: 0.1.1
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
import json


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

    (resp, info) = fetch_url(module, complete_url)

    if info['status'] != 200:
        module.fail_json(msg="Something Failed")
    elif info['status'] == 200:
        if module.params['command'] is None:
            module.exit_json(output=resp.read())
        else:
            module.exit_json(output=json.loads(resp.read()), changed=True)


if __name__ == '__main__':
    main()
