#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_snippets
short_description: Management of the checkly Snippets.
description:
  - Management of the checkly Snippets
  - U(https://www.checklyhq.com/docs/api#tag/Snippets)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/snippets/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on snippets.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of snippet.
    required: false
    type: str
  name:
    description:
      - name of snippet.
    type: str
    required: false
  script:
    description:
      - raw string of script code.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create snippet
  community.missing_collection.checkly_snippets:
    api_key: 'b8155af5c45a476fb60c294c33ff549e'
    command: 'create'
    name: 'consoleTest'
    script: "console.log('test');"

- name: update snippet code
  community.missing_collection.checkly_snippets:
    api_key: 'b8155af5c45a476fb60c294c33ff549e'
    command: 'update'
    id: '1704'
    name: 'consoleTest'
    script: "console.log('test1');"

- name: delete snippet
  community.missing_collection.checkly_snippets:
    api_key: 'b8155af5c45a476fb60c294c33ff549e'
    command: 'delete'
    id: '1704'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "created_at": "2021-09-05T21:51:23.164Z",
    "id": 1705,
    "name": "consoleTest",
    "script": "console.log('test');"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/snippets/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        name=dict(),
        script=dict(),
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
            "name": module.params["name"],
            "script": module.params["script"],
        }
        r = requests.post(module.params["url"], json=data, headers=headers)
    elif module.params["command"] == "update":
        data = {
            "name": module.params["name"],
            "script": module.params["script"],
        }
        r = requests.put(
            module.params["url"] + module.params["id"],
            json=data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    if r.status_code in [200, 201] and module.params["command"] in ["create", "update"]:
        module.exit_json(changed=True, result=r.json())
    elif r.status_code == 204 and module.params["command"] == "delete":
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
