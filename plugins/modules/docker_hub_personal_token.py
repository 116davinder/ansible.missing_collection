#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_personal_token
short_description: Management of the Docker Hub Personal Tokens.
description:
  - Management of the Docker Hub Personal Tokens.
  - U(https://docs.docker.com/docker-hub/api/latest/#tag/access-tokens)
version_added: 0.4.0
options:
  url:
    description:
      - docker hub personal token api.
    required: false
    type: str
    default: 'https://hub.docker.com/v2/access-tokens/'
  token:
    description:
      - jwt/bearer token for api.
    required: true
    type: str
  command:
    description:
      - type of operation on docker hub api.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  uuid:
    description:
      - uuid of personal token.
      - required only for command I(delete)/I(update).
    required: false
    type: str
  token_label:
    description:
      - Friendly name for you to identify the token.
    required: false
    type: str
  is_active:
    description:
      - enable/disable personal token.
    required: false
    type: bool
    default: true
  scopes:
    description:
      - Valid scopes "repo:admin", "repo:write", "repo:read", "repo:public_read"
    required: false
    type: list
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

- name: create docker hub personal token
  community.missing_collection.docker_hub_personal_token:
    token: '{{ __.token }}'
    command: 'create'
    token_label: 'Ansible Managed Token'
    scopes:
      - 'repo:admin'
  register: '__created'

- name: update docker hub personal token aka disable it.
  community.missing_collection.docker_hub_personal_token:
    token: '{{ __.token }}'
    command: 'update'
    uuid: '{{ __created.result["uuid"] }}'
    is_active: false

- name: delete docker hub personal token.
  community.missing_collection.docker_hub_personal_token:
    token: '{{ __.token }}'
    command: 'delete'
    uuid: '{{ __created.result["uuid"] }}'

"""

RETURN = """
result:
  description: result of docker hub api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "uuid": "b30bbf97-506c-4ecd-aabc-842f3cb484fb",
    "client_id": "HUB",
    "creator_ip": "127.0.0.1",
    "creator_ua": "some user agent",
    "created_at": "2021-07-20T12:00:00.000Z",
    "last_used": "string",
    "generated_by": "manual",
    "is_active": true,
    "token": "a7a5ef25-8889-43a0-8cc7-f2a94268e861",
    "token_label": "My read only token",
    "scopes": [
      "repo:read"
    ]
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/access-tokens/"),
        token=dict(required=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        uuid=dict(),
        token_label=dict(),
        is_active=dict(type=bool, default=True),
        scopes=dict(type=list),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["token"]),
        "Content-Type": "application/json"
    }
    data = {}
    if module.params["command"] == "create":
        data = {
            "token_label": module.params["token_label"],
            "scopes": module.params["scopes"]
        }
        r = requests.post(module.params["url"], json=data, headers=headers)
    elif module.params["command"] == "update":
        if module.params["token_label"]:
            data["token_label"] = module.params["token_label"]
        data["is_active"] = module.params["is_active"]
        r = requests.patch(
            module.params["url"] + module.params["uuid"],
            json=data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["uuid"],
            headers=headers
        )
    if r.status_code in [200, 201] and module.params["command"] in ["create", "update"]:
        module.exit_json(changed=True, result=r.json())
    elif r.status_code in [202, 204] and module.params["command"] == "delete":
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
