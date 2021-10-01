#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: statuscake_uptime
short_description: Management of the Status Cake (Uptime).
description:
  - Management of the Status Cake (Uptime).
  - U(https://www.statuscake.com/api/v1/#tag/uptime)
version_added: 0.3.0
options:
  url:
    description:
      - statuscake uptime api.
    required: false
    type: str
    default: 'https://api.statuscake.com/v1/uptime/'
  api_key:
    description:
      - api key for statuscake.
    required: true
    type: str
  command:
    description:
      - type of operation on uptime.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of uptime test.
      - required only for I(delete) and I(update).
    required: false
    type: str
  name:
    description:
      - name of uptime test.
      - required only for I(create) and I(update).
    required: false
    type: str
  test_type:
    description:
      - type of test for Uptime.
    required: false
    type: str
    choices: ["DNS", "HEAD", "HTTP", "PING", "PUSH", "PUT", "SMTP", "SSH", "TCP"]
    default: "HTTP"
  website_url:
    description:
      - URL or IP address of the website under test.
      - I(example): https://www.google.com
    required: false
    type: str
  check_rate:
    description:
      - Number of seconds between tests.
      - I(Example) 0 30 60 300 900 1800 3600 86400
    required: false
    type: int
    default: 60
  basic_user:
    description:
      - Basic authentication username.
    required: false
    type: str
  basic_pass:
    description:
      - Basic authentication password.
    required: false
    type: str
  confirmation:
    description:
      - Number of confirmation servers to confirm downtime before an alert is triggered.
    required: false
    type: int
    default: 2
  contact_groups_csv:
    description:
      - Comma separated list of contact group IDs.
    required: false
    type: str
  custom_header:
    description:
      - JSON object. Represents headers to be sent when making requests.
    required: false
    type: str
  do_not_find:
    description:
      - Whether to consider the test as down if the string in FindString is present within the response.
    required: false
    type: bool
    default: false
  dns_ip:
    description:
      - IP address to compare a DNS test against.
    required: false
    type: str
  dns_server:
    description:
      - Hostname or IP address of the nameserver to query.
    required: false
    type: str
  enable_ssl_alert:
    description:
      - Send an alert if the SSL certificate is soon to expire.
    required: false
    type: bool
    default: false
  final_endpoint:
    description:
      - Specify where the redirect chain should end.
    required: false
    type: str
  find_string:
    description:
      - String to look for within the response. Considered down if not found.
    required: false
    type: str
  follow_redirects:
    description:
      - Whether to follow redirects when testing.
    required: false
    type: bool
    default: false
  host:
    description:
      - Name of the hosting provider.
    required: false
    type: str
  include_header:
    description:
      - Include header content in string match search.
    required: false
    type: bool
    default: false
  paused:
    description:
      - Whether the test should be run.
    required: false
    type: bool
    default: false
  port:
    description:
      - Destination port for TCP tests.
    required: false
    type: int
  post_body:
    description:
      - JSON object. This is converted to form data on request.
    required: false
    type: str
  post_raw:
    description:
      - Raw HTTP POST string to send to the server.
    required: false
    type: str
  regions:
    description:
      - List of regions on which to run tests.
    required: false
    type: list
  status_codes_csv:
    description:
      - Comma separated list of status codes that trigger an alert.
    required: false
    type: str
  tags_csv:
    description:
      - Comma separated list of tags.
    required: false
    type: str
  timeout:
    description:
      - How long to wait to receive the first byte.
    required: false
    type: int
    default: 40
  trigger_rate:
    description:
      - The number of minutes to wait before sending an alert.
    required: false
    type: int
    default: 4
  use_jar:
    description:
      - Enable cookie storage.
    required: false
    type: bool
    default: false
  user_agent:
    description:
      - User agent to be used when making requests.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create uptime test
  community.missing_collection.statuscake_uptime:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'create'
    website_url: 'https://www.google.com'
    test_type: 'HTTP'
    check_rate: 60
    name: 'google_http_check'
  register: __id

- name: update uptime test check rate and name
  community.missing_collection.statuscake_uptime:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'update'
    id: '{{ __id.id }}'
    name: "new_google_http_check"
    check_rate: 86400

- name: delete uptime test
  community.missing_collection.statuscake_uptime:
    api_key: 'Ohxxxxxxxxxxxxxxxxpi'
    command: 'delete'
    id: '{{ __id.id }}'
"""

RETURN = """
id:
  description: id of uptime test.
  returned: when command is `create` and success.
  type: str
  sample: 88175
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.statuscake.com/v1/uptime/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        name=dict(),
        test_type=dict(
            choices=["DNS", "HEAD", "HTTP", "PING", "PUSH", "PUT", "SMTP", "SSH", "TCP"],
            default="HTTP"
        ),
        website_url=dict(),
        check_rate=dict(type=int, default=60),
        basic_user=dict(),
        basic_pass=dict(no_log=True),
        confirmation=dict(type=int, default=2),
        contact_groups_csv=dict(),
        custom_header=dict(),
        do_not_find=dict(type=bool, default=False),
        dns_ip=dict(),
        dns_server=dict(),
        enable_ssl_alert=dict(type=bool, default=False),
        final_endpoint=dict(),
        find_string=dict(),
        follow_redirects=dict(type=bool, default=False),
        host=dict(),
        include_header=dict(type=bool, default=False),
        paused=dict(type=bool, default=False),
        port=dict(type=int),
        post_body=dict(),
        post_raw=dict(),
        regions=dict(type=list),
        status_codes_csv=dict(),
        tags_csv=dict(),
        timeout=dict(type=int, default=40),
        trigger_rate=dict(type=int, default=4),
        use_jar=dict(),
        user_agent=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    # common/default values
    data = {
        "check_rate": module.params["check_rate"],
        "confirmation": module.params["confirmation"],
        "follow_redirects": module.params["follow_redirects"],
        "paused": module.params["paused"],
        "timeout": module.params["timeout"],
        "trigger_rate": module.params["trigger_rate"],
        "include_header": module.params["include_header"],
    }
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }

    if module.params["basic_user"] is not None:
        data["basic_user"] = module.params["basic_user"]
    if module.params["basic_pass"] is not None:
        data["basic_pass"] = module.params["basic_pass"]
    if module.params["contact_groups_csv"] is not None:
        data["contact_groups_csv"] = module.params["contact_groups_csv"]
    if module.params["custom_header"] is not None:
        data["custom_header"] = module.params["custom_header"]
    if module.params["do_not_find"] is not None:
        data["do_not_find"] = module.params["do_not_find"]
    if module.params["dns_ip"] is not None:
        data["dns_ip"] = module.params["dns_ip"]
    if module.params["dns_server"] is not None:
        data["dns_server"] = module.params["dns_server"]
    if module.params["enable_ssl_alert"] is not None:
        data["enable_ssl_alert"] = module.params["enable_ssl_alert"]
    if module.params["final_endpoint"] is not None:
        data["final_endpoint"] = module.params["final_endpoint"]
    if module.params["find_string"] is not None:
        data["find_string"] = module.params["find_string"]
    if module.params["host"] is not None:
        data["host"] = module.params["host"]
    if module.params["port"] is not None:
        data["port"] = module.params["port"]
    if module.params["post_body"] is not None:
        data["post_body"] = module.params["post_body"]
    if module.params["post_raw"] is not None:
        data["post_raw"] = module.params["post_raw"]
    if module.params["regions"] is not None:
        data["regions"] = module.params["regions"]
    if module.params["status_codes_csv"] is not None:
        data["status_codes_csv"] = module.params["status_codes_csv"]
    if module.params["tags_csv"] is not None:
        data["tags_csv"] = module.params["tags_csv"]
    if module.params["use_jar"] is not None:
        data["use_jar"] = module.params["use_jar"]
    if module.params["user_agent"] is not None:
        data["user_agent"] = module.params["user_agent"]

    # create/update/delete operation
    if module.params["command"] == "create":
        data["website_url"] = module.params["website_url"]
        data["test_type"] = module.params["test_type"]
        data["name"] = module.params["name"]

        r = requests.post(module.params["url"], data=data, headers=headers)
    elif module.params["command"] == "update":
        if module.params["name"] is not None:
            data["name"] = module.params["name"]
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
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
