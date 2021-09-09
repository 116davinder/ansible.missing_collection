#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_checks_info
short_description: Get information about checkly checks.
description:
  - Get information about checkly checks.
  - U(https://www.checklyhq.com/docs/api#tag/Checks)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/checks/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  id:
    description:
      - id of alert channel.
    required: false
    type: str
  api_check_url_filter_pattern:
    description:
      - Filters the results by a string contained in the URL of an API check.
      - for instance a domain like B(www.myapp.com).
      - Only returns API checks.
    required: false
    type: str
  limit:
    description:
      - number of checks in one call.
    required: false
    type: int
    default: 100
  page:
    description:
      - page number of retrieve call.
    required: false
    type: int
    default: 1
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all checks from checkly
  community.missing_collection.checkly_checks_info:
    api_key: 'a8f08873c494445ba156e572e1324300'

- name: get one check from checkly
  community.missing_collection.checkly_checks_info:
    api_key: 'a8f08873c494445ba156e572e1324300'
    id: '39308'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when success.
  type: list/dict
  sample: [
    {
      "id": "string",
      "name": "string",
      "checkType": "BROWSER",
      "frequency": 10,
      "frequencyOffset": 1,
      "activated": true,
      "muted": false,
      "doubleCheck": true,
      "sslCheck": true,
      "shouldFail": true,
      "locations": [],
      "request": { },
      "script": "string",
      "environmentVariables": [],
      "tags": [],
      "setupSnippetId": 0,
      "tearDownSnippetId": 0,
      "localSetupScript": "string",
      "localTearDownScript": "string",
      "alertSettings": {},
      "useGlobalAlertSettings": true,
      "degradedResponseTime": 10000,
      "maxResponseTime": 20000,
      "groupId": 0,
      "groupOrder": 0,
      "runtimeId": "2021.06",
      "alertChannelSubscriptions": [],
      "alertChannels": {},
      "created_at": "2019-08-24",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/checks/"),
        api_key=dict(required=True, no_log=True),
        id=dict(),
        api_check_url_filter_pattern=dict(),
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
        if module.params["api_check_url_filter_pattern"]:
            data["apiCheckUrlFilterPattern"] = module.params["api_check_url_filter_pattern"]
        r = requests.get(module.params["url"], data=data, headers=headers)
    else:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )

    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
