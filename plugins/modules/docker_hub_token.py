#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_token
short_description: Get Authentication Token aka JWT Token from Docker Hub.
description:
  - Get Authentication Token aka JWT Token from Docker Hub.
  - U(https://docs.docker.com/docker-hub/api/latest/#operation/PostUsersLogin)
version_added: 0.4.0
options:
  url:
    description:
      - docker hub rest api.
    required: false
    type: str
    default: 'https://hub.docker.com/v2/users/login'
  username:
    description:
      - username for docker hub.
    required: true
    type: str
  password:
    description:
      - password for docker hub.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get jwt token from docker hub
  community.missing_collection.docker_hub_token:
    username: "test"
    password: "test123"
"""

RETURN = """
token:
  description: jwt token.
  returned: when success.
  type: str
  sample: "yJ4NWMiOlsiTxxxxxxxxxxxxxxxxncWhra"
"""

import requests
from ansible.module_utils.basic import AnsibleModule


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/users/login"),
        username=dict(required=True),
        password=dict(required=True, no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "username": module.params["username"],
        "password": module.params["password"]
    }

    r = requests.post(
        module.params["url"],
        json=data,
        headers=headers
    )
    if r.status_code == 200:
        module.exit_json(token=r.json()["token"])
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
