#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_contact_groups
short_description: Management of the Status Cake (contact-groups).
description:
  - Management of the Status Cake (contact-groups).
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
  command:
    description:
      - type of operation on contact groups.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of contact-groups test.
      - required only for `delete` and `update`.
    required: false
    type: str
  ping_url:
    description:
      - URL or IP address of an endpoint to push uptime events.
      - Currently this only supports HTTP GET endpoints.
      - I(example): https://www.google.com
    required: false
    type: str
  email_addresses_csv:
    description:
      - Comma separated list of email addresses.
    required: false
    type: str
  mobile_numbers_csv:
    description:
      - Comma separated list of international format mobile phone numbers.
    required: false
    type: str
  integrations_csv:
    description:
      - Comma separated list of integration IDs.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create contact groups test
  community.missing_collection.statuscake_contact_groups:
    api_key: 'sGxxxxxxxxxxxx6y'
    command: 'create'
    ping_url: 'https://www.google.com'
    name: "google_contact_groups_test"
    email_addresses_csv: "786spartan@gmail.com"
  register: __id

- name: update contact groups name
  community.missing_collection.statuscake_contact_groups:
    api_key: 'sGxxxxxxxxxxxx6y'
    command: 'update'
    id: '{{ __id.id }}'
    name: "new_google_contact_groups_test"

- name: delete contact groups test
  community.missing_collection.statuscake_contact_groups:
    api_key: 'sGxxxxxxxxxxxx6y'
    command: 'delete'
    id: '{{ __id.id }}'
"""

RETURN = """
id:
  description: id of contact-groups test.
  returned: when command is `create` and success.
  type: str
  sample: 230089
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/contact-groups/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        name=dict(),
        ping_url=dict(),
        email_addresses_csv=dict(),
        mobile_numbers_csv=dict(),
        integrations_csv=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    data = {
        "name": module.params["name"],
        "ping_url": module.params["ping_url"],
        "mobile_numbers_csv": module.params["mobile_numbers_csv"],
        "email_addresses_csv": module.params["email_addresses_csv"],
        "integrations_csv": module.params["integrations_csv"],
    }
    if module.params["command"] == "create":
        r = requests.post(module.params["url"], data=data, headers=headers)
    elif module.params["command"] == "update":
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
