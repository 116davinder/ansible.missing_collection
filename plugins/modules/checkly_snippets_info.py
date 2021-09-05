#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_snippets_info
short_description: Get information about checkly snippets.
description:
  - Get information about checkly snippets.
  - U(https://www.checklyhq.com/docs/api#tag/Snippets)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/snippets/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  id:
    description:
      - id of snippet.
    required: false
    type: str
  limit:
    description:
      - number of environment snippet retrieved in one call.
    required: false
    type: int
    default: 100
  page:
    description:
      - page number of environment snippets retrieve call.
    required: false
    type: int
    default: 1
  get_all_snippets:
    description:
      - get information about all snippets given I(limit) and I(page).
    required: false
    type: bool
    default: false
  get_one_snippet:
    description:
      - get information about one snippet given I(id).
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get all alert channels from checkly
  community.missing_collection.checkly_snippets_info:
    api_key: 'a8f08873c494445ba156e572e1324300'
    get_all_snippets: true

- name: get one alert channel from checkly
  community.missing_collection.checkly_snippets_info:
    api_key: 'a8f08873c494445ba156e572e1324300'
    get_one_snippet: true
    id: '1706'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when success.
  type: list/dict
  sample: [
    {
      "id": 0,
      "name": "string",
      "script": "string",
      "created_at": "2019-08-24T14:15:22Z",
      "updated_at": "2019-08-24T14:15:22Z"
    }
  ]
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/snippets/"),
        api_key=dict(required=True, no_log=True),
        id=dict(),
        limit=dict(type=int, default=100),
        page=dict(type=int, default=1),
        get_all_snippets=dict(type=bool, default=False),
        get_one_snippet=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    if module.params["get_all_snippets"]:
        data = {
            "page": module.params["page"],
            "limit": module.params["limit"]
        }
        r = requests.get(module.params["url"], data=data, headers=headers)
    elif module.params["get_one_snippet"]:
        r = requests.get(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    else:
        module.fail_json(msg="unknown parameters passed")
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
