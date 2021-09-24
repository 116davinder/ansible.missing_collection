#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_personal_token_info
short_description: Get information about docker hub personal tokens.
description:
  - Get information about docker hub personal tokens.
  - U(https://docs.docker.com/docker-hub/api/latest/#tag/access-tokens)
version_added: 0.4.0
options:
  url:
    description:
      - docker hub api.
    required: false
    type: str
    default: 'https://hub.docker.com/v2/access-tokens/'
  token:
    description:
      - jwt/Bearer token for docker hub api.
    required: true
    type: str
  uuid:
    description:
      - uuid of personal token.
      - if defined, will fetch info about given I(uuid) persona token only.
      - else all personal tokens will be fetched.
    required: false
    type: str
  page_size:
    description:
      - number of personal tokens retrieved in one call.
    required: false
    type: int
    default: 100
  page:
    description:
      - page number of personal tokens retrieve call.
    required: false
    type: int
    default: 1
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get jwt token from docker hub
  community.missing_collection.docker_hub_token:
    username: 'testUser'
    password: 'aDL0xxxxxxxxxxoQt6'
  register: '__'

- name: get information about all personal tokens
  community.missing_collection.docker_hub_personal_token_info:
    token: '{{ __.token }}'
  register: '__all'

- name: get information about one personal tokens
  community.missing_collection.docker_hub_personal_token_info:
    token: '{{ __.token }}'
    uuid: '{{ __all.result.results[0].uuid }}'
"""

RETURN = """
result:
  description: result of docker hub api.
  returned: when success.
  type: dict
  sample: {
    "count": 1,
    "next": "string",
    "previous": "string",
    "active_count": 1,
    "results": [
      {
        "uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb",
        "client_id": "HUB",
        "creator_ip": "127.0.0.1",
        "creator_ua": "some user agent",
        "created_at": "2021-07-20T12:00:00.000Z",
        "last_used": "string",
        "generated_by": "manual",
        "is_active": true,
        "token": "",
        "token_label": "My read only token",
        "scopes": [
          "repo:read"
        ]
      }
    ]
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/access-tokens/"),
        token=dict(required=True, no_log=True),
        uuid=dict(),
        page_size=dict(type=int, default=100),
        page=dict(type=int, default=1),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["token"]),
        "Content-Type": "application/json"
    }
    if not module.params["uuid"]:
        data = {
            "page": module.params["page"],
            "page_size": module.params["page_size"]
        }
        r = requests.get(module.params["url"], json=data, headers=headers)
    else:
        r = requests.get(
            module.params["url"] + module.params["uuid"],
            headers=headers
        )
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
