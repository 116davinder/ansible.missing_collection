#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_reporting_info
short_description: Generates a report with aggregate statistics for checks and check groups.
description:
  - Generates a report with aggregate statistics for checks and check groups.
  - U(https://www.checklyhq.com/docs/api#tag/Reporting)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/reporting'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  deactivated:
    description:
      - Filter checks by activated status.
    required: true
    type: bool
    default: false
  filter_by_tags:
    description:
      - Use tags to filter the checks you want to see in your report.
    required: false
    type: list
    default: []
  from_date:
    description:
      - unix epoch from date to filter results.
      - Setting a custom I(from_date) timestamp overrides the use of any I(preset_window).
      - check example for format or use I(to_datetime) filter.
    required: false
    type: str
  preset_window:
    description:
      - Preset reporting windows are used for quickly generating report on commonly used windows.
      - Can be overridden by using a custom I(to_date) and I(from_date) timestamp.
    required: false
    type: str
    choices: ["last24Hrs", "last7Days", "last30Days", "thisWeek", "thisMonth", "lastWeek", "lastMonth"]
    default: "last24Hrs"
  to_date:
    description:
      - unix epoch to date to filter results.
      - Setting a custom I(to_date) timestamp overrides the use of any I(preset_window).
      - check example for format or use I(to_datetime) filter.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: generate report for last 24 hours
  community.missing_collection.checkly_reporting_info:
    api_key: '95e3814891ef433298150a539750076e'
    preset_window: 'last24Hrs'

- name: generate report for specific period
  community.missing_collection.checkly_reporting_info:
    api_key: '95e3814891ef433298150a539750076e'
    from_date: "{{ ('2021-09-02 06:50:00'|to_datetime).strftime('%s') }}"
    to_date: "{{ ('2021-09-04 06:50:00'|to_datetime).strftime('%s') }}"
"""

RETURN = """
result:
  description: result of the api.
  returned: when success.
  type: list
  sample: [
    {
      "name": "string",
      "checkId": "string",
      "checkType": "string",
      "deactivated": true,
      "tags": ["string"],
      "aggregate": {
        "successRatio": 0,
        "avg": 0,
        "p95": 0,
        "p99": 0
      }
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/reporting"),
        api_key=dict(required=True, no_log=True),
        deactivated=dict(type=bool, default=False),
        filter_by_tags=dict(type=list, default=[]),
        from_date=dict(),
        preset_window=dict(
            choices=["last24Hrs", "last7Days", "last30Days", "thisWeek", "thisMonth", "lastWeek", "lastMonth"],
            default="last24Hrs"
        ),
        to_date=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    params = {
        "deactivated": module.params["deactivated"],
        "filter_by_tags": module.params["filter_by_tags"],
        "presetWindow": module.params["preset_window"],
    }
    if module.params["from_date"]:
        params["from"] = module.params["from_date"]
    if module.params["to_date"]:
        params["to"] = module.params["to_date"]

    r = requests.get(
        module.params["url"],
        params=params,
        headers=headers
    )

    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
