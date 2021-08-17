#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_contact_groups_info
short_description: Get information from Status Cake (contact-groups).
description:
  - Get information from Status Cake (contact-groups).
  - U(https://www.statuscake.com/api/v1/#tag/contact-groups)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake contact-groups api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/contact-groups/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all contact-groups
  community.missing_collection.statuscake_contact_groups_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: list
  sample: [
    {
      "id": "1",
      "name": "Operations Team",
      "ping_url": "https://www.example.com/notificaions",
      "email_addresses": [],
      "mobile_numbers": [],
      "integrations": []
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/contact-groups/"),
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
        module.exit_json(data=r.json()["data"])
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
