#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_account_info
short_description: Get information from checkly about Account.
description:
  - Get information from checkly about Account.
  - U(https://www.checklyhq.com/docs/api#tag/Account)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/account'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get details about account
  community.missing_collection.checkly_account_info:
    api_key: 'sGxxxxxxxxxxxx6y'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict
  sample: {
    "accountId": "string",
    "name": "string"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/account"),
        api_key=dict(required=True, no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    r = requests.get(module.params["url"], headers=headers)
    if r.status_code == 200:
        module.exit_json(data=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
