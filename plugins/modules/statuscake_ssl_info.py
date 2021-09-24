#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_ssl_info
short_description: Get information from Status Cake (SSL).
description:
  - Get information from Status Cake (SSL).
  - U(https://www.statuscake.com/api/v1/#tag/ssl)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake ssl api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/ssl/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
  id:
    description:
      - id of ssl test.
    required: false
    type: str
  get_all_tests:
    description:
      - get list of all ssl tests.
    required: false
    type: bool
  get_one_test:
    description:
      - fetch info about one specific test I(id).
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all ssl tests
  community.missing_collection.statuscake_ssl_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    get_all_tests: true
  register: __tests

- name: get info about one ssl test
  community.missing_collection.statuscake_ssl_info:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    get_one_test: true
    id: '{{ __tests.data[0].id }}'
"""

RETURN = """
data:
  description: result of the api.
  returned: when success.
  type: dict/list
  sample: [
    {
      "alert_at": [1, 7, 30],
      "alert_broken": false,
      "alert_expiry": false,
      "alert_mixed": false,
      "alert_reminder": false,
      "certificate_score": 95,
      "certificate_status": "CERT_OK",
      "check_rate": 999999,
      "cipher": "TLS_CHACHA20_POLY1305_SHA256",
      "cipher_score": 100,
      "contact_groups": [],
      "flags": {
        "follow_redirects": false,
        "has_mixed": false,
        "has_pfs": true,
        "is_broken": false,
        "is_expired": false,
        "is_extended": false,
        "is_missing": false,
        "is_revoked": false
      },
      "follow_redirects": false,
      "hostname": "new_google_ssl_test",
      "id": "238191",
      "issuer_common_name": "GTS CA 1C",
      "last_reminder": 0,
      "mixed_content": [],
      "paused": false,
      "updated_at": "2021-08-12T20:06:55+00:00",
      "user_agent": "",
      "valid_from": "2021-07-12T03:48:00+00:00",
      "valid_until": "2021-10-04T03:48:00+00:00",
      "website_url": "https://www.google.com"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/ssl/"),
        id=dict(),
        api_key=dict(required=True, no_log=True),
        get_all_tests=dict(type=bool),
        get_one_test=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("get_one_test", True, ["id"]),
        ),
        mutually_exclusive=[
            (
                "get_all_tests",
                "get_one_test",
            )
        ]
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["get_all_tests"]:
        r = requests.get(module.params["url"], headers=headers)
    else:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )

    if r.status_code == 200:
        module.exit_json(data=r.json()["data"])
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
