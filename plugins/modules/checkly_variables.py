#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_variables
short_description: Management of the checkly environment variables.
description:
  - Management of the checkly environment variables.
  - U(https://www.checklyhq.com/docs/api#tag/Environment-variables)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/variables/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on environment variables.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  key:
    description:
      - environment key.
    type: str
    required: true
  value:
    description:
      - environment value.
    required: false
    type: str
    default: ""
  locked:
    description:
      - Used only in the UI to hide the value like a password.
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create environment key-pair
  community.missing_collection.checkly_variables:
    api_key: '95e3814891ef433298150a539750076e'
    command: 'create'
    key: 'GITHUB_TOKEN'
    value: '95e3814891ef43329815'

- name: update value of key and locked
  community.missing_collection.checkly_variables:
    api_key: '95e3814891ef433298150a539750076e'
    command: 'update'
    key: 'GITHUB_TOKEN'
    value: '33298150a539750076e'
    locked: true

- name: delete key
  community.missing_collection.checkly_variables:
    api_key: '95e3814891ef433298150a539750076e'
    command: 'delete'
    key: 'GITHUB_TOKEN'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "key": "GITHUB_TOKEN",
    "locked": false,
    "value": "95e3814891ef43329815"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/variables/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        key=dict(required=True),
        value=dict(default=""),
        locked=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["command"] == "create":
        data = {
            "key": module.params["key"],
            "value": module.params["value"],
            "locked": module.params["locked"],
        }
        r = requests.post(module.params["url"], json=data, headers=headers)
    elif module.params["command"] == "update":
        data = {
            "key": module.params["key"],
            "value": module.params["value"],
            "locked": module.params["locked"],
        }
        r = requests.put(
            module.params["url"] + module.params["key"],
            json=data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["key"],
            headers=headers
        )
    if r.status_code in [200, 201] and module.params["command"] in ["create", "update"]:
        module.exit_json(changed=True, result=r.json())
    elif r.status_code == 204 and module.params["command"] == "delete":
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
