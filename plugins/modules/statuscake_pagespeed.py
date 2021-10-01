#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_pagespeed
short_description: Management of the Status Cake (Pagespeed).
description:
  - Management of the Status Cake (Pagespeed).
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
  command:
    description:
      - type of operation on pagespeed.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of pagespeed test.
      - required only for `delete` and `update`.
    required: false
    type: str
  name:
    description:
      - name of the pagespeed test.
      - required only for `create` and `update`.
    required: false
    type: str
  website_url:
    description:
      - URL or IP address of the website under test.
      - I(example): https://www.google.com
      - required only for `create` and `update`.
    required: false
    type: str
  location_iso:
    description:
      - Testing location
      - Enum "AU" "CA" "DE" "IN" "NL" "SG" "UK" "US" "PRIVATE".
    required: false
    type: str
  check_rate:
    description:
      - Number of minutes between tests
    required: false
    type: int
    default: 5
  alert_bigger:
    description:
      - An alert will be sent if the size of the page is larger than this value (kb).
      - A value of 0 prevents alerts being sent.
    required: false
    type: int
    default: 0
  alert_slower:
    description:
      - An alert will be sent if the load time of the page exceeds this value (ms).
      - A value of 0 prevents alerts being sent.
    required: false
    type: int
    default: 0
  alert_smaller:
    description:
      - An alert will be sent if the size of the page is smaller than this value (kb).
      - A value of 0 prevents alerts being sent.
    required: false
    type: int
    default: 0
  contact_groups_csv:
    description:
      - Comma separated list of contact group IDs.
    required: false
    type: str
    default: ""
  paused:
    description:
      - Whether the test should be run.
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create pagespeed test
  community.missing_collection.statuscake_pagespeed:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'create'
    website_url: 'https://www.google.com'
    location_iso: 'US'
    name: 'google_test'
  register: __id

- name: rename pagespeed test
  community.missing_collection.statuscake_pagespeed:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'update'
    id: '{{ __id.id }}'
    name: 'google_test_new'

- name: delete pagespeed test
  community.missing_collection.statuscake_pagespeed:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'delete'
    id: '{{ __id.id }}'
"""

RETURN = """
id:
  description: id of pagespeed test.
  returned: when command is `create` and success.
  type: str
  sample: 88175
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/pagespeed/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        name=dict(),
        website_url=dict(),
        location_iso=dict(),
        check_rate=dict(type=int, default=5),
        alert_bigger=dict(type=int, default=0),
        alert_slower=dict(type=int, default=0),
        alert_smaller=dict(type=int, default=0),
        contact_groups_csv=dict(default=""),
        paused=dict(type=bool, default=False),
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
            "website_url": module.params["website_url"],
            "location_iso": module.params["location_iso"],
            "check_rate": module.params["check_rate"],
            "alert_bigger": module.params["alert_bigger"],
            "alert_slower": module.params["alert_slower"],
            "alert_smaller": module.params["alert_smaller"],
            "contact_groups_csv": module.params["contact_groups_csv"],
            "paused": module.params["paused"],
        }
        r = requests.post(module.params["url"], data=data, headers=headers)
    elif module.params["command"] == "update":
        data = {
            "name": module.params["name"],
            "location_iso": module.params["location_iso"],
            "check_rate": module.params["check_rate"],
            "alert_bigger": module.params["alert_bigger"],
            "alert_slower": module.params["alert_slower"],
            "alert_smaller": module.params["alert_smaller"],
            "contact_groups_csv": module.params["contact_groups_csv"],
            "paused": module.params["paused"],
        }
        r = requests.put(
            module.params["url"] + module.params["id"],
            data=data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    if r.status_code == 201 and module.params["command"] == "create":
        module.exit_json(changed=True, id=r.json()["data"]["new_id"])
    elif r.status_code == 204 and module.params["command"] in ["update", "delete"]:
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
