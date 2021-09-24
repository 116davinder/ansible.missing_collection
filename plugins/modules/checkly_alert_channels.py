#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_alert_channels
short_description: Management of the checkly Alert Channels.
description:
  - Management of the checkly Alert Channels.
  - U(https://www.checklyhq.com/docs/api#tag/Alert-channels)
  - Developer Note - B(subscriptions) field is skipped on purpose for I(create)/I(update).
version_added: 0.3.0
options:
  url:
    description:
      - checkly alert channel api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/alert-channels/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on alert channels.
    required: false
    type: str
    choices: ["create", "update", "update-sub", "delete"]
    default: "create"
  id:
    description:
      - id of alert channel.
      - required only for `delete` and `update`.
    required: false
    type: str
  config:
    description:
      - dict of data for alert channel.
      - object (AlertChannelCreateConfig).
    required: false
    type: dict
  send_degraded:
    description:
      - send alert when degraded.
    required: false
    type: bool
    default: false
  send_failure:
    description:
      - send alert when failure.
    required: false
    type: bool
    default: false
  send_recovery:
    description:
      - send alert when recovery.
    required: false
    type: bool
    default: false
  ssl_expiry:
    description:
      - Determines if an alert should be send for expiring SSL certificates.
    required: false
    type: bool
    default: false
  ssl_expiry_threshold:
    description:
      - At what moment in time to start alerting on SSL certificates.
    required: false
    type: int
    default: 30
  activated:
    description:
      - do you want to active I(check_id)/I(group_id) with subscription.
    required: false
    type: bool
    default: false
  check_id:
    description:
      - use only in I(update-sub) command.
      - You can either pass a I(check_id) or a I(group_id), but not both.
    required: false
    type: str
  group_id:
    description:
      - use only in I(update-sub) command.
      - You can either pass a I(check_id) or a I(group_id), but not both.
    required: false
    type: str
  type:
    description:
      - type of alert channels.
    required: false
    type: str
    choices: ["EMAIL", "SLACK", "WEBHOOK", "SMS", "PAGERDUTY", "OPSGENIE"]
    default: "EMAIL"
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create alert channel
  community.missing_collection.checkly_alert_channels:
    api_key: 'a8f08873c494445ba156e572e1324300'
    command: 'create'
    config:
      address: 'dpsangwal@gmail.com'
  register: __

- name: update a alert channel aka email address
  community.missing_collection.checkly_alert_channels:
    api_key: 'a8f08873c494445ba156e572e1324300'
    command: 'update'
    id: '{{ __.result.id }}'
    config:
      address: 'example1@gmail.com'

- name: update a alert channel subcriptions only
  community.missing_collection.checkly_alert_channels:
    api_key: 'a8f08873c494445ba156e572e1324300'
    command: 'update-sub'
    id: '{{ __.result.id }}'
    activated: true
    check_id: '1ceaff6c-12ce-4322-9ac1-2dd2c14a2967'

- name: delete a alert channel
  community.missing_collection.checkly_alert_channels:
    api_key: 'a8f08873c494445ba156e572e1324300'
    command: 'delete'
    id: '{{ __.result.id }}'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update)/I(update-sub) and success.
  type: dict
  sample: {
    "config": { "address": "dpsangwal@gmail.com"},
    "created_at": "2021-08-31T18:23:51.054Z",
    "id": 39323,
    "sendDegraded": false,
    "sendFailure": false,
    "sendRecovery": false,
    "sslExpiry": false,
    "sslExpiryThreshold": 30,
    "type": "EMAIL"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/alert-channels/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "update-sub", "delete"], default="create"),
        id=dict(),
        config=dict(type=dict),
        send_degraded=dict(type=bool, default=False),
        send_failure=dict(type=bool, default=False),
        send_recovery=dict(type=bool, default=False),
        ssl_expiry=dict(type=bool, default=False),
        ssl_expiry_threshold=dict(type=int, default=30),
        activated=dict(type=bool, default=False),
        check_id=dict(),
        group_id=dict(),
        type=dict(choices=["EMAIL", "SLACK", "WEBHOOK", "SMS", "PAGERDUTY", "OPSGENIE"], default="EMAIL"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ("check_id", "group_id"),
        ]
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    data = {
        "type": module.params["type"],
        "config": module.params["config"],
        "sendRecovery": module.params["send_recovery"],
        "sendFailure": module.params["send_failure"],
        "sendDegraded": module.params["send_degraded"],
        "sslExpiry": module.params["ssl_expiry"],
        "sslExpiryThreshold": module.params["ssl_expiry_threshold"]
    }
    if module.params["command"] == "create":
        r = requests.post(module.params["url"], json=data, headers=headers)
    elif module.params["command"] == "update":
        r = requests.put(
            module.params["url"] + module.params["id"],
            json=data,
            headers=headers
        )
    elif module.params["command"] == "update-sub":
        sub_data = {
            "activated": module.params["activated"]
        }
        if module.params["check_id"]:
            sub_data["checkId"] = module.params["check_id"]
        else:
            sub_data["groupId"] = module.params["group_id"]
        r = requests.put(
            module.params["url"] + module.params["id"] + "/subscriptions",
            json=sub_data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    if r.status_code in [200, 201] and module.params["command"] in ["create", "update", "update-sub"]:
        module.exit_json(changed=True, result=r.json())
    elif r.status_code == 204 and module.params["command"] == "delete":
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
