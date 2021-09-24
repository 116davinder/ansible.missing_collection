#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_pagespeed_info
short_description: Get information from Status Cake (Pagespeed).
description:
  - Get information from Status Cake (Pagespeed).
  - U(https://www.statuscake.com/api/v1/#tag/pagespeed)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake pagespeed api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/pagespeed/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
  id:
    description:
      - id of pagespeed test.
    required: false
    type: str
  get_all_tests:
    description:
      - get list of all pagespeed tests.
    required: false
    type: bool
  get_one_test:
    description:
      - fetch info about one specific test I(id).
    required: false
    type: bool
  get_test_histroy:
    description:
      - fetch history info about one specific test I(id).
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all pagespeed tests
  community.missing_collection.statuscake_pagespeed_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    get_all_tests: true
  register: __tests

- name: get info about one pagespeed test
  community.missing_collection.statuscake_pagespeed_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    get_one_test: true
    id: '{{ __tests.data[0].id }}'

- name: get history about one pagespeed test
  community.missing_collection.statuscake_pagespeed_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    get_test_histroy: true
    id: '{{ __tests.data[0].id }}'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict/list
  sample: [
    {
      "alert_bigger": 0,
      "alert_slower": 0,
      "alert_smaller": 0,
      "check_rate": 1440,
      "contact_groups": [],
      "id": "88176",
      "latest_stats": {
        "filesize_kb": 251.284,
        "has_issue": false,
        "latest_issue": "",
        "loadtime_ms": 344,
        "requests": 6
      },
      "location": "PAGESPD-US4",
      "location_iso": "US",
      "name": "google_test_new",
      "paused": false,
      "website_url": "https://www.google.com"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/pagespeed/"),
        id=dict(),
        api_key=dict(required=True, no_log=True),
        get_all_tests=dict(type=bool),
        get_one_test=dict(type=bool),
        get_test_histroy=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one_test", True, ["id"]),
            ("get_test_histroy", True, ["id"]),
        ),
        mutually_exclusive=[
            (
                "get_all_tests",
                "get_one_test",
                "get_test_histroy"
            )
        ]
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["get_all_tests"]:
        r = requests.get(module.params["url"], headers=headers)
    elif module.params["get_one_test"]:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    else:
        r = requests.get(
            module.params["url"] + module.params["id"] + "/history",
            headers=headers
        )
    if r.status_code == 200:
        module.exit_json(data=r.json()["data"])
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
