#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_locations_info
short_description: Get information from Status Cake (Locations).
description:
  - Get information from Status Cake (Locations).
  - U(https://www.statuscake.com/api/v1/#tag/locations)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
  command:
    description:
      - for which service you want to fetch all locations.
    required: false
    type: str
    choices: ["uptime", "pagespeed"]
    default: "uptime"
  best:
    description:
      - Return only locations with the least number of tests.
    required: false
    type: bool
    default: true
  location:
    description:
      - Country ISO.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: list all uptime locations
  community.missing_collection.statuscake_locations_info:
    api_key: 'sGxxxxxxxxxxxx6y'
    command: 'uptime'

- name: list all pagespeed locations
  community.missing_collection.statuscake_locations_info:
    api_key: 'sGxxxxxxxxxxxx6y'
    command: 'pagespeed'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: list
  sample: [
    {
      "hostname": "UKINT",
      "description": "United Kingdom, London - 5",
      "region": "United Kingdom / London",
      "ipv4": "178.62.78.199",
      "ipv6": "2a03:b0c0:1:d0::5e:f001",
      "region_code": "london",
      "status": "up"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["uptime", "pagespeed"], default="uptime"),
        best=dict(type=bool, default=True),
        location=dict()
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    params = {
        "best": module.params["best"],
        "location": module.params["location"]
    }
    if module.params["command"] == "uptime":
        r = requests.get(
            module.params["url"] + "uptime-locations",
            params=params,
            headers=headers
        )
    else:
        r = requests.get(
            module.params["url"] + "pagespeed-locations",
            params=params,
            headers=headers
        )
    if r.status_code == 200:
        module.exit_json(data=r.json()["data"])
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
