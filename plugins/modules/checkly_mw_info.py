#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_mw_info
short_description: Get information about checkly Maintenance windows.
description:
  - Get information about checkly Maintenance windows.
  - U(https://www.checklyhq.com/docs/api#tag/Maintenance-windows)
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
  id:
    description:
      - id of maintenance window.
    required: false
    type: str
  limit:
    description:
      - number of maintenance windows retrieved in one call.
    required: false
    type: int
    default: 100
  page:
    description:
      - page number of maintenance window retrieve call.
    required: false
    type: int
    default: 1
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all maintenance windows from checkly
  community.missing_collection.checkly_maintenance_windows_info:
    api_key: 'a8f08873c494445ba156e572e1324300'

- name: get one maintenance window from checkly
  community.missing_collection.checkly_maintenance_windows_info:
    api_key: 'a8f08873c494445ba156e572e1324300'
    id: '426'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when success.
  type: list/dict
  sample: [
    {
      "id": 0,
      "name": "string",
      "tags": [],
      "startsAt": "2019-08-24",
      "endsAt": "2019-08-24",
      "repeatInterval": 1,
      "repeatUnit": "string",
      "repeatEndsAt": "2019-08-24",
      "created_at": "2019-08-24",
      "updated_at": "2019-08-24"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/maintenance-windows/"),
        api_key=dict(required=True, no_log=True),
        id=dict(),
        limit=dict(type=int, default=100),
        page=dict(type=int, default=1),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if not module.params["id"]:
        data = {
            "page": module.params["page"],
            "limit": module.params["limit"]
        }
        r = requests.get(module.params["url"], data=data, headers=headers)
    else:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
