#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_registry
short_description: Management operation of Docker Registry (v2).
description:
  - Management operation of Docker Registry (v2).
  - U(https://docs.docker.com/registry/spec/api/)
version_added: 0.4.0
options:
  scheme:
    description:
      - http scheme for docker registry.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of docker registry.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of docker registry.
    required: false
    type: str
    default: '5000'
  username:
    description:
      - docker registry username.
    required: false
    type: str
  password:
    description:
      - password for docker registry I(username).
    required: false
    type: str
  repo_name:
    description:
      - repository name when I(list_tags) is `True`.
    required: false
    type: str
  tag_digest:
    description:
      - docker digest for image sha256.
      - you can use I(community.missing_collection.docker_registry_info) to get this digest.
      - example I(sha256:157c270646xxxxxxxxx418bb63e4)
    required: false
    type: str
  command:
    description:
      - type of operation on docker registry api.
    required: false
    type: str
    choices: ["delete"]
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: delete image by digest
  community.missing_collection.docker_registry:
    command: 'delete'
    repo_name: 'test-timedb'
    tag_digest: 'sha256:157c270646500f0be63cb8eb809e1d192ad24646562bba2942e7b75418bb63e4'
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="5000"),
        username=dict(),
        password=dict(no_log=True),
        repo_name=dict(),
        tag_digest=dict(),
        command=dict(choices=["delete"]),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Content-Type": "application/json"
    }
    if not module.params["username"] and not module.params["password"]:
        auth = HTTPBasicAuth(
            module.params["username"], module.params["password"]
        )
    else:
        auth = None

    url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/v2/"

    if module.params["command"] == "delete":
        url = url + module.params["repo_name"] + "/manifests/" + module.params["tag_digest"]
        r = requests.delete(
            url,
            auth=auth,
            headers=headers
        )
        if r.status_code == 202:
            module.exit_json(changed=True)
        else:
            module.fail_json(r.text)
    else:
        module.fail_json("unknown parameters")


if __name__ == "__main__":
    main()
