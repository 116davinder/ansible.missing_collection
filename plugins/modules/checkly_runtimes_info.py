#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_runtimes_info
short_description: Get information from checkly about Runtimes.
description:
  - Get information from checkly about Runtimes.
  - U(https://www.checklyhq.com/docs/api#tag/Runtimes)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/runtimes/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  id:
    description:
      - runtime id/name.
    required: false
    type: str
  get_one_runtimes:
    description:
      - get the details of all included NPM packages and their version for one specific runtime I(id).
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get details of all checkly runtimes
  community.missing_collection.checkly_runtimes_info:
    api_key: 'a8f0xxxxxxxxxxx00'
  register: __

- name: get details of one specific runtimes
  community.missing_collection.checkly_runtimes_info:
    api_key: 'a8f0xxxxxxxxxxx00'
    id: '{{ __.data[0].name }}'
    get_one_runtimes: true
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict/list
  sample: [
    {
      "name": "string",
      "default": true,
      "description": "string",
      "dependencies": {}
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/runtimes/"),
        api_key=dict(required=True, no_log=True),
        id=dict(),
        get_one_runtimes=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one_runtimes", True, ["id"]),
        ),
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    if module.params["get_one_runtimes"]:
        r = requests.get(module.params["url"] + module.params["id"], headers=headers)
    else:
        r = requests.get(module.params["url"], headers=headers)

    if r.status_code == 200:
        module.exit_json(data=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
