#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_check_results_info
short_description: Get information from checkly about Check Results.
description:
  - Get information from checkly about Check Results.
  - U(https://www.checklyhq.com/docs/api#tag/Check-results)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/check-results/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  check_id:
    description:
      - check id for checkly.
    required: true
    type: str
  check_result_id:
    description:
      - check result id for checkly when I(get_one_result).
    required: false
    type: str
  check_type:
    description:
      - check type for checkly.
    required: false
    type: str
    choices: ["BROWSER", "API"]
    default: "API"
  from_date:
    description:
      - unix epoch from date to filter results.
      - check example for format or use I(to_datetime) filter.
    required: false
    type: str
  has_failures:
    description:
      - check result has one or more failures.
    required: true
    type: bool
    default: false
  limit:
    description:
      - number of results from checkly per call.
    required: false
    type: int
    default: 100
  location:
    description:
      - filter results with given location only.
      - example B(ap-south-1)
    required: false
    type: str
  page:
    description:
      - page number if there are results more than given I(limit) in a call.
    required: false
    type: int
  to_date:
    description:
      - unix epoch to date to filter results.
      - check example for format or use I(to_datetime) filter.
    required: false
    type: str
  get_all_results:
    description:
      - get all check results for given I(check_id).
    required: true
    type: bool
    default: false
  get_one_result:
    description:
      - get one check result for given I(check_id) and I(check_result_id).
    required: true
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all check results detail from checkly
  community.missing_collection.checkly_check_results_info:
    api_key: '95e3814891ef433298150a539750076e'
    check_id: '1ceaff6c-12ce-4322-9ac1-2dd2c14a2967'
    page: 1
    from_date: "{{ ('2021-09-04 06:50:00'|to_datetime).strftime('%s') }}"
    get_all_results: true

- name: get one check result detail from checkly
  community.missing_collection.checkly_check_results_info:
    api_key: '95e3814891ef433298150a539750076e'
    check_id: '1ceaff6c-12ce-4322-9ac1-2dd2c14a2967'
    check_result_id: 'c826dca7-6543-4649-ad47-ade94367f5b1'
    get_one_result: true
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: list/dict
  sample: [
    {
      "id": "string",
      "name": "string",
      "checkId": "string",
      "hasFailures": true,
      "hasErrors": true,
      "isDegraded": true,
      "overMaxResponseTime": true,
      "runLocation": "string",
      "startedAt": "2019-08-24T14:15:22Z",
      "stoppedAt": "2019-08-24T14:15:22Z",
      "created_at": "2019-08-24T14:15:22Z",
      "responseTime": 0,
      "apiCheckResult": {},
      "browserCheckResult": {},
      "checkRunId": 0,
      "attempts": 0
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/check-results/"),
        api_key=dict(required=True, no_log=True),
        check_id=dict(required=True),
        check_result_id=dict(),
        check_type=dict(choices=["BROWSER", "API"], default="API"),
        from_date=dict(),
        has_failures=dict(type=bool, default=False),
        limit=dict(type=int, default=100),
        location=dict(),
        page=dict(type=int),
        to_date=dict(),
        get_all_results=dict(type=bool),
        get_one_result=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one_result", True, ["check_result_id"]),
        )
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    params = {
        "checkType": module.params["check_type"],
        "limit": module.params["limit"],
        "hasFailures": module.params["has_failures"],
    }
    if module.params["from_date"]:
        params["from"] = module.params["from_date"]
    if module.params["location"]:
        params["location"] = module.params["location"]
    if module.params["page"]:
        params["page"] = module.params["page"]
    if module.params["to_date"]:
        params["to_date"] = module.params["to_date"]

    if module.params["get_all_results"]:
        r = requests.get(
            module.params["url"] + module.params["check_id"],
            params=params,
            headers=headers
        )
    elif module.params["get_one_result"]:
        r = requests.get(
            module.params["url"] + module.params["check_id"] + "/" + module.params["check_result_id"],
            headers=headers
        )
    else:
        module.fail_json("unknown option are passed")

    if r.status_code == 200:
        module.exit_json(data=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
