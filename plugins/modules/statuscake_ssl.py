#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_ssl
short_description: Management of the Status Cake (SSL).
description:
  - Management of the Status Cake (SSL).
  - U(https://www.statuscake.com/api/v1/#tag/ssl)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake ssl api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/ssl/'
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
      - id of ssl test.
      - required only for `delete` and `update`.
    required: false
    type: str
  website_url:
    description:
      - URL or IP address of the website under test.
      - I(example): https://www.google.com
    required: false
    type: str
  check_rate:
    description:
      - Number of seconds between tests.
      - I(Example) 300 600 1800 3600 86400 2073600
    required: false
    type: int
    default: 3600
  alert_at_csv:
    description:
      - Comma separated list representing when alerts should be sent (days).
      - Must be exactly 3 numerical values
    required: false
    type: str
    default: "30,7,1"
  alert_reminder:
    description:
      - Whether to enable alert reminders.
    required: false
    type: bool
    default: false
  alert_expiry:
    description:
      - Whether to enable alerts when the SSL certificate is to expire.
    required: false
    type: bool
    default: false
  alert_broken:
    description:
      - Whether to enable alerts when SSL certificate issues are found.
    required: false
    type: bool
    default: false
  alert_mixed:
    description:
      - Whether to enable alerts when mixed content is found.
    required: false
    type: bool
    default: false
  follow_redirects:
    description:
      - Whether to follow redirects when testing.
    required: false
    type: bool
    default: false
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
  hostname:
    description:
      - Hostname of the server under test.
      - required only for `create` and `update`.
    required: false
    type: str
    default: ""
  user_agent:
    description:
      - Custom user agent string set when testing.
      - required only for `create` and `update`.
    required: false
    type: str
    default: ""
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create ssl test
  community.missing_collection.statuscake_ssl:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'create'
    website_url: 'https://www.google.com'
    alert_at_csv: "30,7,1"
  register: __id

- name: update ssl test check rate
  community.missing_collection.statuscake_ssl:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'update'
    id: '{{ __id.id }}'
    check_rate: 86400

- name: delete ssl test
  community.missing_collection.statuscake_ssl:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'delete'
    id: '{{ __id.id }}'
"""

RETURN = """
id:
  description: id of ssl test.
  returned: when command is `create` and success.
  type: str
  sample: 88175
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/ssl/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        website_url=dict(),
        check_rate=dict(type=int, default=3600),
        contact_groups_csv=dict(default=""),
        alert_at_csv=dict(default="30,7,1"),
        alert_reminder=dict(type=bool, default=False),
        alert_expiry=dict(type=bool, default=False),
        alert_broken=dict(type=bool, default=False),
        alert_mixed=dict(type=bool, default=False),
        follow_redirects=dict(type=bool, default=False),
        paused=dict(type=bool, default=False),
        hostname=dict(default=""),
        user_agent=dict(default=""),
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
            "website_url": module.params["website_url"],
            "check_rate": module.params["check_rate"],
            "alert_reminder": module.params["alert_reminder"],
            "alert_expiry": module.params["alert_expiry"],
            "alert_broken": module.params["alert_broken"],
            "alert_mixed": module.params["alert_mixed"],
            "follow_redirects": module.params["follow_redirects"],
            "alert_at_csv": module.params["alert_at_csv"],
            "contact_groups_csv": module.params["contact_groups_csv"],
            "paused": module.params["paused"],
            "hostname": module.params["hostname"],
            "user_agent": module.params["user_agent"],
        }
        r = requests.post(module.params["url"], data=data, headers=headers)
    elif module.params["command"] == "update":
        data = {
            "check_rate": module.params["check_rate"],
            "alert_reminder": module.params["alert_reminder"],
            "alert_expiry": module.params["alert_expiry"],
            "alert_broken": module.params["alert_broken"],
            "alert_mixed": module.params["alert_mixed"],
            "follow_redirects": module.params["follow_redirects"],
            "alert_at_csv": module.params["alert_at_csv"],
            "contact_groups_csv": module.params["contact_groups_csv"],
            "paused": module.params["paused"],
            "hostname": module.params["hostname"],
            "user_agent": module.params["user_agent"],
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
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
