#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_uptime_info
short_description: Get information from Status Cake (Uptime).
description:
  - Get information from Status Cake (Uptime).
  - U(https://www.statuscake.com/api/v1/#tag/uptime)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake Uptime api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/uptime/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
  id:
    description:
      - id of uptime test.
    required: false
    type: str
  status:
    description:
      - status of uptime test.
    required: false
    type: str
    choices: ["up", "down"]
    default: "up"
  page:
    description:
      - id of page for which you want to fetch results.
    required: false
    type: int
    default: 1
  limit:
    description:
      - number of results per page.
    required: false
    type: int
    default: 5000
  get_all_tests:
    description:
      - get list of all Uptime tests.
    required: false
    type: bool
  get_one:
    description:
      - fetch info about one specific test I(id).
    required: false
    type: bool
  get_histroy:
    description:
      - fetch history info about one specific test I(id).
    required: false
    type: bool
  get_all_periods:
    description:
      - fetch test periods info about one specific test I(id).
    required: false
    type: bool
  get_all_alerts:
    description:
      - fetch alerts info about one specific test I(id).
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all uptime tests
  community.missing_collection.statuscake_uptime_info:
    api_key: 'sxxxxxxxxxxxx6y'
    get_all_tests: true
  register: __tests

- name: get info about one uptime test
  community.missing_collection.statuscake_uptime_info:
    api_key: 'sxxxxxxxxxxxx6y'
    get_one: true
    id: '{{ __tests.data[0].id }}'

- name: get history about one uptime test
  community.missing_collection.statuscake_uptime_info:
    api_key: 'sxxxxxxxxxxxx6y'
    get_histroy: true
    id: '{{ __tests.data[0].id }}'

- name: get all periods about one uptime test
  community.missing_collection.statuscake_uptime_info:
    api_key: 'sxxxxxxxxxxxx6y'
    get_all_periods: true
    id: '{{ __tests.data[0].id }}'

- name: get all alerts about one uptime test
  community.missing_collection.statuscake_uptime_info:
    api_key: 'sxxxxxxxxxxxx6y'
    get_all_alerts: true
    id: '{{ __tests.data[0].id }}'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict/list
  sample: [
    {
      "check_rate": 300,
      "contact_groups": [],
      "host": "",
      "id": "6086154",
      "name": "google_http_check-79",
      "paused": false,
      "status": "up",
      "tags": [],
      "test_type": "HTTP",
      "uptime": 100,
      "website_url": "https://www.google.com"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/uptime/"),
        id=dict(),
        status=dict(choices=["up", "down"], default="up"),
        page=dict(type=int, default=1),
        limit=dict(type=int, default=5000),
        api_key=dict(required=True, no_log=True),
        get_all_tests=dict(type=bool),
        get_one=dict(type=bool),
        get_histroy=dict(type=bool),
        get_all_periods=dict(type=bool),
        get_all_alerts=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one", True, ["id"]),
            ("get_histroy", True, ["id"]),
            ("get_all_periods", True, ["id"]),
            ("get_all_alerts", True, ["id"]),
        ),
        mutually_exclusive=[
            (
                "get_all_tests",
                "get_one",
                "get_histroy",
                "get_all_periods",
                "get_all_alerts",
            )
        ]
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["get_all_tests"]:
        params = {
            "status": module.params["status"],
            "page": module.params["page"],
            "limit": module.params["limit"]
        }
        r = requests.get(module.params["url"], params=params, headers=headers)
    elif module.params["get_one"]:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    elif module.params["get_histroy"]:
        r = requests.get(
            module.params["url"] + module.params["id"] + "/history",
            headers=headers
        )
    elif module.params["get_all_periods"]:
        r = requests.get(
            module.params["url"] + module.params["id"] + "/periods",
            headers=headers
        )
    else:
        r = requests.get(
            module.params["url"] + module.params["id"] + "/alerts",
            headers=headers
        )
    if r.status_code == 200:
        module.exit_json(data=r.json()["data"])
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
