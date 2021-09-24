#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_registry_info
short_description: Get information from Docker Registry (v2).
description:
  - Get information from Docker Registry (v2).
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
  tag_name:
    description:
      - image tag name when I(get_manifest) is `True`.
    required: false
    type: str
  limit:
    description:
      - number of results retrieved in one call.
    required: false
    type: int
    default: 1000
  list_repos:
    description:
      - get all repositories?
    required: false
    type: bool
  list_tags:
    description:
      - get all I(repo_name) tags?
    required: false
    type: bool
  get_manifest:
    description:
      - get image manifest I(repo_name) and I(tag_name)?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: connection test
  community.missing_collection.docker_registry_info:
    scheme: 'http'
    host: 'localhost'
    port: 5000

- name: get all docker repositories
  community.missing_collection.docker_registry_info:
    scheme: 'http'
    host: 'localhost'
    port: 5000
    list_repos: true
  register: '__'

- name: get all docker repository tags
  community.missing_collection.docker_registry_info:
    list_tags: true
    repo_name: '{{ __.result.repositories[0] }}'

- name: get image tag manifest
  community.missing_collection.docker_registry_info:
    get_manifest: true
    repo_name: '{{ __.result.repositories[0] }}'
    tag_name: '{{ tags.result.tags[0] }}'
"""

RETURN = """
result:
  description: result of docker registry api.
  returned: when success.
  type: dict
  sample: {"repositories": ["test-timedb"]}
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
        limit=dict(type=int, default=1000),
        repo_name=dict(),
        tag_name=dict(),
        list_repos=dict(type=bool),
        list_tags=dict(type=bool),
        get_manifest=dict(type=bool),
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

    params = {
        "n": module.params["limit"]
    }

    url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/v2/"

    if module.params["list_repos"]:
        url = url + "_catalog"
    elif module.params["list_tags"]:
        url = url + module.params["repo_name"] + "/tags/list"
    elif module.params["get_manifest"]:
        headers = {
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        url = url + module.params["repo_name"] + "/manifests/" + module.params["tag_name"]
    else:
        pass  # make connection test

    r = requests.get(
        url,
        auth=auth,
        params=params,
        headers=headers
    )
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
