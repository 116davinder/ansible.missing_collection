#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_check_groups
short_description: Management of the checkly Check Groups.
description:
  - Management of the checkly Check Groups.
  - U(https://www.checklyhq.com/docs/api#tag/Check-groups)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/check-groups/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on checks.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of check group.
      - required only for I(delete) and I(update).
    required: false
    type: str
  auto_assign_alerts:
    description:
      - nothing mentioned in api docs.
    required: false
    type: bool
    default: true
  activated:
    description:
      - Determines if the check is running or not.
    required: false
    type: bool
    default: true
  name:
    description:
      - name of the check group.
    required: false
    type: str
  alert_channel_subscriptions:
    description:
      - List of alert channel subscriptions.
    required: false
    type: list
    default: []
  alert_settings:
    description:
      - Alert settings.
    required: false
    type: dict
    default: {}
  api_check_defaults:
    description:
      - default settings for all checks which will be part of this group.
    required: false
    type: dict
    default: {}
  browser_check_defaults:
    description:
      - default settings for all checks which will be part of this group.
    required: false
    type: dict
  concurrency:
    description:
      - Determines how many checks are invoked concurrently
      - when triggering a check group from CI/CD or through the API.
    required: false
    type: int
    default: 3
  double_check:
    description:
      - Setting this to "true" will trigger a retry when a check fails from the failing region and another,
      - randomly selected region before marking the check as failed.
    required: false
    type: bool
    default: true
  environment_variables:
    description:
      - Key/value pairs for setting environment variables during check execution.
    required: false
    type: list
    default: []
  local_setup_script:
    description:
      - A valid piece of Node.js code to run in the setup phase.
    required: false
    type: str
  local_tear_down_script:
    description:
      - A valid piece of Node.js code to run in the teardown phase.
    required: false
    type: str
  locations:
    description:
      - An array of one or more data center locations where to run the this check.
    required: false
    type: list
    default: ["ap-south-1"]
  muted:
    description:
      - Determines if any notifications will be send out when a check fails and/or recovers.
    required: false
    type: bool
    default: false
  runtime_id:
    description:
      - The runtime version, i.e. fixed set of runtime dependencies, used to execute this check.
    required: false
    type: str
    choices: ["2021.06", "2020.01"]
    default: "2021.06"
  setup_snippet_id:
    description:
      - An ID reference to a snippet to use in the setup phase of an API check.
    required: false
    type: int
  tags:
    description:
      - A list of one or more tags that filter which checks to display on the dashboard.
    required: false
    type: list
    default: ""
  tear_down_snippet_id:
    description:
      - An ID reference to a snippet to use in the teardown phase of an API check.
    required: false
    type: int
  use_global_alert_settings:
    description:
      - When true, the account level alert setting will be used,
      - not the alert setting defined on this check.
    required: false
    type: bool
    default: true
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create a check group with apicheckDefaults
  community.missing_collection.checkly_check_groups:
    api_key: 'f9a037281de04a36b74534dd973c3a78'
    command: 'create'
    name: 'Ansible API Check Group'
    api_check_defaults:
      assertions:
        - comparison: "EQUALS"
          property: ""
          source: "STATUS_CODE"
          target: "200"
      basicAuth:
        password: ""
        username: ""
      body: ""
      bodyType: "NONE"
      followRedirects: true
      headers: []
      method: "GET"
      queryParameters: []
      url: "https://www.axway.com/"
    alert_channel_subscriptions:
      - activated: true
        alertChannelId: 39739
    alert_settings:
      escalationType: "RUN_BASED"
      reminders:
        amount: 0
        interval: 5
      runBasedEscalation:
        failedRunThreshold: 1
      sslCertificates:
        alertThreshold: 30
        enabled: true
      timeBasedEscalation:
        minutesFailingThreshold: 5
    use_global_alert_settings: false
    tags:
      - 'api'
      - 'axway'
  register: __

- name: update a check group
  community.missing_collection.checkly_check_groups:
    api_key: 'f9a037281de04a36b74534dd973c3a78'
    command: 'update'
    name: 'New Ansible API Check Group'
    id: '{{ __.result.id }}'

- name: delete a check group
  community.missing_collection.checkly_check_groups:
    api_key: 'f9a037281de04a36b74534dd973c3a78'
    command: 'delete'
    id: '{{ __.result.id }}'

"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "id": 0,
    "name": "string",
    "activated": true,
    "muted": true,
    "tags": [],
    "locations": [],
    "concurrency": 3,
    "apiCheckDefaults": {},
    "browserCheckDefaults": {},
    "environmentVariables": [],
    "doubleCheck": true,
    "useGlobalAlertSettings": true,
    "alertSettings": {},
    "alertChannelSubscriptions": [],
    "setupSnippetId": 0,
    "tearDownSnippetId": 0,
    "localSetupScript": "string",
    "localTearDownScript": "string",
    "runtimeId": "2021.06",
    "created_at": "2019-08-24",
    "updated_at": "2019-08-24T14:15:22Z"
    }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/check-groups/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        auto_assign_alerts=dict(type=bool, default=True),
        activated=dict(type=bool, default=True),
        name=dict(),
        alert_channel_subscriptions=dict(type=list, default=[]),
        alert_settings=dict(type=dict, default={}),
        api_check_defaults=dict(type=dict, default={}),
        browser_check_defaults=dict(type=dict),
        concurrency=dict(type=int, default=3),
        double_check=dict(type=bool, default=True),
        environment_variables=dict(type=list, default=[]),
        local_setup_script=dict(),
        local_tear_down_script=dict(),
        locations=dict(type=list, default=["ap-south-1"]),
        muted=dict(type=bool, default=False),
        runtime_id=dict(choices=["2021.06", "2020.01"], default="2021.06"),
        setup_snippet_id=dict(type=int),
        tags=dict(type=list, default=[]),
        tear_down_snippet_id=dict(type=int),
        use_global_alert_settings=dict(type=bool, default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    params = {
        "autoAssignAlerts": module.params["auto_assign_alerts"]
    }
    data = {
        "concurrency": module.params["concurrency"],
        "activated": module.params["activated"],
        "muted": module.params["muted"],
        "doubleCheck": module.params["double_check"],
        "locations": module.params["locations"],
        "environmentVariables": module.params["environment_variables"],
        "alertSettings": module.params["alert_settings"],
        "apiCheckDefaults": module.params["api_check_defaults"],
        "useGlobalAlertSettings": module.params["use_global_alert_settings"],
        "runtimeId": module.params["runtime_id"],
        "alertChannelSubscriptions": module.params["alert_channel_subscriptions"]
    }

    if module.params["name"]:
        data["name"] = module.params["name"]
    if module.params["browser_check_defaults"]:
        data["browserCheckDefaults"] = module.params["browser_check_defaults"]
    if module.params["setup_snippet_id"]:
        data["setupSnippetId"] = module.params["setup_snippet_id"]
    if module.params["tear_down_snippet_id"]:
        data["tearDownSnippetId"] = module.params["tear_down_snippet_id"]
    if module.params["tags"]:
        data["tags"] = module.params["tags"]

    if module.params["command"] == "create":
        r = requests.post(module.params["url"], json=data, params=params, headers=headers)
    elif module.params["command"] == "update":
        r = requests.put(
            module.params["url"] + module.params["id"],
            json=data,
            params=params,
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
