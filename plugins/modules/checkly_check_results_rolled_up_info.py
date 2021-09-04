#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_check_results_rolled_up_info
short_description: Get information from checkly about Check Results (Rolled Up).
description:
  - Get information from checkly about Check Results (Rolled Up).
  - U(https://www.checklyhq.com/docs/api#tag/Check-results-(rolled-up))
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/check-results-rolled-up/'
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
  from_date:
    description:
      - unix epoch from date to filter results.
      - check example for format or use I(to_datetime) filter.
    required: false
    type: str
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
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get check results (rolled up) detail from checkly
  community.missing_collection.checkly_check_results_rolled_up_info:
    api_key: '95e3814891ef433298150a539750076e'
    check_id: '1ceaff6c-12ce-4322-9ac1-2dd2c14a2967'
    page: 1
    from_date: '{{ ('2021-09-04 06:50:00'|to_datetime).strftime('%s') }}'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: list
  sample: [
    {
      "checkId": "1ceaff6c-12ce-4322-9ac1-2dd2c14a2967",
      "errorCount": 0,
      "failureCount": 0,
      "hour": "2021-09-04T07:00:00.000Z",
      "responseTimes": [75],
      "resultsCount": 1,
      "runLocation": "us-east-2"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/check-results-rolled-up/"),
        api_key=dict(required=True, no_log=True),
        check_id=dict(required=True),
        from_date=dict(),
        limit=dict(type=int, default=100),
        location=dict(),
        page=dict(type=int),
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
        "limit": module.params["limit"]
    }
    if module.params["from_date"]:
        params["from"] = module.params["from_date"]
    if module.params["location"]:
        params["location"] = module.params["location"]
    if module.params["page"]:
        params["page"] = module.params["page"]
    if module.params["to_date"]:
        params["to_date"] = module.params["to_date"]

    r = requests.get(
        module.params["url"] + module.params["check_id"],
        params=params,
        headers=headers
    )
    if r.status_code == 200:
        module.exit_json(data=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
