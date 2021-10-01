#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_checks
short_description: Management of the checkly Checks.
description:
  - Management of the checkly Checks.
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
  command:
    description:
      - type of operation on checks.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of check.
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
  check_type:
    description:
      - The type of the check.
    required: false
    type: str
    choices: ["BROWSER", "API"]
    default: "API"
  name:
    description:
      - name of the check.
    required: false
    type: str
  script:
    description:
      - nodejs based script.
      - nothing mentioned in api docs.
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
  degraded_response_time:
    description:
      - The response time in milliseconds where a check should be considered degraded.
    required: false
    type: int
    default: 10000
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
      - These are only relevant for Browser checks.
      - Use global environment variables whenever possible.
    required: false
    type: list
    default: []
  frequency:
    description:
      - how often the check should run in minutes.
    required: false
    type: int
    default: 60
  frequency_offset:
    description:
      - Used for setting seconds for check frequencies under 1 minutes (only for API checks)
      - and spreading checks over a time range for frequencies over 1 minute.
      - This works as follows Checks with a frequency of 0 can have a frequencyOffset of 10, 20 or 30 meaning they will run every 10, 20 or 30 seconds.
      - Checks with a frequency lower than and equal to 60 can have a frequencyOffset between 1 and a max value based on the formula "Math.floor(frequency * 10)",
      - i.e. for a check that runs every 5 minutes the max frequencyOffset is 50.
      - Checks with a frequency higher than 60 can have a frequencyOffset between 1 and a max value based on the formula "Math.ceil(frequency / 60)",
      - i.e. for a check that runs every 720 minutes, the max frequencyOffset is 12.
    required: false
    type: int
  group_id:
    description:
      - The id of the check group this check is part of.
    required: false
    type: int
  group_order:
    description:
      - The position of this check in a check group.
      - It determines in what order checks are run when a group is triggered from the API or from CI/CD.
    required: false
    type: int
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
  max_response_time:
    description:
      - The response time in milliseconds where a check should be considered failing.
    required: false
    type: int
    default: 20000
  muted:
    description:
      - Determines if any notifications will be send out when a check fails and/or recovers.
    required: false
    type: bool
    default: false
  request:
    description:
      - request object.
    required: false
    type: dict
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
  should_fail:
    description:
      - Allows to invert the behaviour of when a check is considered to fail.
      - Allows for validating error status like 404.
    required: false
    type: bool
    default: false
  ssl_check:
    description:
      - Determines if the SSL certificate should be validated for expiry.
    required: false
    type: bool
    default: false
  tags:
    description:
      - A list of one or more tags that filter which checks to display on the dashboard.
    required: false
    type: list
    default: []
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
- name: create a check
  community.missing_collection.checkly_checks:
    api_key: 'c18803aafff44ec091558db24aa87098'
    command: 'create'
    name: 'Ansible API Check'
    check_type: "API"
    request:
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

# doesn't work yet - Internal Server Error
- name: update a check
  community.missing_collection.checkly_checks:
    api_key: 'c18803aafff44ec091558db24aa87098'
    command: 'update'
    name: 'New Ansible API Check'
    id: '{{ __.result.id }}'
    request:
      method: "GET"
      url: "https://example.com/"

- name: delete a check
  community.missing_collection.checkly_checks:
    api_key: 'c18803aafff44ec091558db24aa87098'
    command: 'delete'
    id: '{{ __.result.id }}'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
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
    "request": {},
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
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/checks/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        auto_assign_alerts=dict(type=bool, default=True),
        activated=dict(type=bool, default=True),
        check_type=dict(choices=["BROWSER", "API"], default="API"),
        name=dict(),
        script=dict(),
        alert_channel_subscriptions=dict(type=list, default=[]),
        alert_settings=dict(type=dict, default={}),
        degraded_response_time=dict(type=int, default=10000),
        double_check=dict(type=bool, default=True),
        environment_variables=dict(type=list, default=[]),
        frequency=dict(type=int, default=60),
        frequency_offset=dict(type=int),
        group_id=dict(type=int),
        group_order=dict(type=int),
        local_setup_script=dict(),
        local_tear_down_script=dict(),
        locations=dict(type=list, default=["ap-south-1"]),
        max_response_time=dict(type=int, default=20000),
        muted=dict(type=bool, default=False),
        request=dict(type=dict),
        runtime_id=dict(choices=["2021.06", "2020.01"], default="2021.06"),
        setup_snippet_id=dict(type=int),
        should_fail=dict(type=bool, default=False),
        ssl_check=dict(type=bool, default=False),
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
        "checkType": module.params["check_type"],
        "frequency": module.params["frequency"],
        "activated": module.params["activated"],
        "muted": module.params["muted"],
        "doubleCheck": module.params["double_check"],
        "sslCheck": module.params["ssl_check"],
        "shouldFail": module.params["should_fail"],
        "locations": module.params["locations"],
        "environmentVariables": module.params["environment_variables"],
        "alertSettings": module.params["alert_settings"],
        "useGlobalAlertSettings": module.params["use_global_alert_settings"],
        "degradedResponseTime": module.params["degraded_response_time"],
        "maxResponseTime": module.params["max_response_time"],
        "runtimeId": module.params["runtime_id"],
        "alertChannelSubscriptions": module.params["alert_channel_subscriptions"]
    }

    if module.params["name"]:
        data["name"] = module.params["name"]
    if module.params["frequency_offset"]:
        data["frequencyOffset"] = module.params["frequency_offset"]
    if module.params["request"]:
        data["request"] = module.params["request"]
    if module.params["script"]:
        data["script"] = module.params["script"]
    if module.params["setup_snippet_id"]:
        data["setupSnippetId"] = module.params["setup_snippet_id"]
    if module.params["tear_down_snippet_id"]:
        data["tearDownSnippetId"] = module.params["tear_down_snippet_id"]
    if module.params["local_setup_script"]:
        data["localSetupScript"] = module.params["local_setup_script"]
    if module.params["local_tear_down_script"]:
        data["localTearDownScript"] = module.params["local_tear_down_script"]
    if module.params["group_id"]:
        data["groupId"] = module.params["group_id"]
    if module.params["group_order"]:
        data["groupOrder"] = module.params["group_order"]
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
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
