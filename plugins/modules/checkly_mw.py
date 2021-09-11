#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_mw
short_description: Management of the checkly maintenance windows.
description:
  - Management of the checkly maintenance windows.
  - U(https://www.checklyhq.com/docs/api#tag/Environment-variables)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/maintenance-windows/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on maintenance windows.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of maintenance window.
    type: str
  ends_at:
    description:
      - The end date of the maintenance window.
      - example I(2021-09-07T14:30:00.000Z) or I(2021-09-07)
    required: false
    type: str
  name:
    description:
      - The maintenance window name.
    required: false
    type: str
  repeat_unit:
    description:
      - The repeat strategy for the maintenance window.
    required: false
    type: str
    choices: ["DAY", "WEEK", "MONTH"]
  start_at:
    description:
      - The start date of the maintenance window.
      - example I(2021-09-07T14:30:00.000Z) or I(2021-09-07)
    required: false
    type: str
  tags:
    description:
      - The names of the checks and groups maintenance window should apply to.
    required: false
    type: list
    default: []
  repeat_ends_at:
    description:
      - The end date where the maintenance window should stop repeating.
      - example I(2021-09-07T14:30:00.000Z) or I(2021-09-07)
    required: false
    type: str
  repeat_interval:
    description:
      - The repeat interval of the maintenance window from the first occurance.
      - any number >=1.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create maintenance window
  community.missing_collection.checkly_mw:
    api_key: 'f7b0813b3428419d8b9c5ebb86fcca52'
    command: 'create'
    name: 'testMW'
    ends_at: "2021-09-07"
    start_at: "2021-09-06"
    repeat_unit: "DAY"
    repeat_ends_at: "2021-09-24"
    repeat_interval: "1"
    tags:
      - 'api'
  register: __

- name: update maintenance window
  community.missing_collection.checkly_mw:
    api_key: 'f7b0813b3428419d8b9c5ebb86fcca52'
    command: 'update'
    id: "{{ __.result.id }}"
    name: 'testNewMW'
    ends_at: "2021-09-07"
    start_at: "2021-09-06"
    repeat_unit: "DAY"
    repeat_ends_at: "2021-09-28"
    repeat_interval: "2"
    tags:
      - 'api'
      - 'axway'

- name: delete maintenance window
  community.missing_collection.checkly_mw:
    api_key: 'f7b0813b3428419d8b9c5ebb86fcca52'
    command: 'delete'
    id: "{{ __.result.id }}"
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "name": "string",
    "tags": ["string"],
    "startsAt": "2019-08-24",
    "endsAt": "2019-08-24",
    "repeatInterval": 1,
    "repeatUnit": "string",
    "repeatEndsAt": "2019-08-24"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/maintenance-windows/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        ends_at=dict(),
        name=dict(),
        repeat_unit=dict(choices=["DAY", "WEEK", "MONTH"]),
        start_at=dict(),
        tags=dict(type=list, default=[]),
        repeat_ends_at=dict(),
        repeat_interval=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["command"] in ["create", "update"]:
        data = {
            "name": module.params["name"],
            "endsAt": module.params["ends_at"],
            "repeatUnit": module.params["repeat_unit"],
            "startsAt": module.params["start_at"],
            "tags": module.params["tags"]
        }
        if module.params["repeat_ends_at"]:
            data["repeatEndsAt"] = module.params["repeat_ends_at"]
        if module.params["repeat_interval"]:
            data["repeatInterval"] = module.params["repeat_interval"]
    if module.params["command"] == "create":
        r = requests.post(module.params["url"], json=data, headers=headers)
    elif module.params["command"] == "update":
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
