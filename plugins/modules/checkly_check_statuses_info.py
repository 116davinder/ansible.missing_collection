#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_check_statuses_info
short_description: Get information from checkly about check status.
description:
  - Get information from checkly about check status.
  - U(https://www.checklyhq.com/docs/api#tag/Check-status)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/check-statuses/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  id:
    description:
      - check id.
    required: false
    type: str
  get_one_check:
    description:
      - get the current status information for a specific check I(id).
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get details of all checkly check statuses
  community.missing_collection.checkly_check_statuses_info:
    api_key: 'a8f0xxxxxxxxxxx00'
  register: __

- name: get details of one specific check statuses
  community.missing_collection.checkly_check_statuses_info:
    api_key: 'a8f0xxxxxxxxxxx00'
    id: '{{ __.data[0].checkId }}'
    get_one_check: true
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict/list
  sample: [
    {
      "name": "string",
      "checkId": "string",
      "hasFailures": true,
      "hasErrors": true,
      "isDegraded": true,
      "longestRun": 0,
      "shortestRun": 0,
      "lastRunLocation": "string",
      "lastCheckRunId": "string",
      "sslDaysRemaining": 0,
      "created_at": "2019-08-24",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/check-statuses/"),
        api_key=dict(required=True, no_log=True),
        id=dict(),
        get_one_check=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one_check", True, ["id"]),
        ),
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    if module.params["get_one_check"]:
        r = requests.get(module.params["url"] + module.params["id"], headers=headers)
    else:
        r = requests.get(module.params["url"], headers=headers)

    if r.status_code == 200:
        module.exit_json(data=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
