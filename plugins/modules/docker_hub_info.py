#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_info
short_description: Get information about docker namespaces/repositories/images.
description:
  - Get information about docker namespaces/repositories/images.
  - U(https://docs.docker.com/docker-hub/api/latest/#tag/images)
  - U(https://hub.docker.com/support/doc/how-do-i-authenticate-with-the-v2-api)
version_added: 0.4.0
options:
  url:
    description:
      - docker hub api.
    required: false
    type: str
    default: 'https://hub.docker.com/v2/'
  token:
    description:
      - jwt/Bearer token for docker hub api.
    required: true
    type: str
  username:
    description:
      - username for docker hub for which you want to list repository.
    required: false
    type: str
  namespace:
    description:
      - Namespace of the repository.
    required: false
    type: str
  repository:
    description:
      - Name of the repository.
    required: false
    type: str
  status:
    description:
      - Filters to only show images of this status.
    required: false
    type: str
    choices: ["active", "inactive"]
    default: "active"
  currently_tagged:
    description:
      - Filters to only show images with
    required: false
    type: bool
    default: true
  ordering:
    description:
      - Orders the results by this property.
      - Prefixing with B(-) sorts by descending order.
    required: false
    type: str
    choices: ["last_activity", "-last_activity", "digest", "-digest"]
    default: "last_activity"
  active_from:
    description:
      - Sets the time from which an image must have been pushed or pulled to be counted as active.
      - Defaults to 1 month before the current time.
    required: false
    type: str
  page_size:
    description:
      - number of records retrieved in one call.
    required: false
    type: int
    default: 100
  page:
    description:
      - page number of record retrieve call.
    required: false
    type: int
    default: 1
  list_namespaces:
    description:
      - get list of all namespaces.
    required: false
    type: bool
  list_repositories:
    description:
      - get list of all repository for given I(username).
    required: false
    type: bool
  get_repository_summary:
    description:
      - Gets the number of images in a repository and the number of images counted as active and inactive.
      - for given I(namespace) and I(repository).
    required: false
    type: bool
  get_repository_images:
    description:
      - Gets details on the images in a repository.
      - for given I(namespace) and I(repository).
    required: false
    type: bool
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

- name: get all namespaces from docker hub
  community.missing_collection.docker_hub_info:
    token: '{{ __.token }}'
    list_namespaces: true
  register: '__ns'

- name: get all repositories for given username
  community.missing_collection.docker_hub_info:
    token: '{{ __.token }}'
    list_repositories: true
    username: 'testUser'

- name: get repository summary
  community.missing_collection.docker_hub_info:
    token: '{{ __.token }}'
    get_repository_summary: true
    namespace: 'testUser'
    repository: 'test'

- name: get repository images (required Pro license)
  community.missing_collection.docker_hub_info:
    token: '{{ __.token }}'
    get_repository_images: true
    namespace: 'testUser'
    repository: 'test'
"""

RETURN = """
result:
  description: result of docker hub api.
  returned: when success.
  type: dict
  sample: {"namespaces": ["testUser"]}
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/"),
        token=dict(required=True, no_log=True),
        username=dict(),
        namespace=dict(),
        repository=dict(),
        status=dict(choices=["active", "inactive"], default="active"),
        currently_tagged=dict(type=bool, default=True),
        ordering=dict(choices=["last_activity", "-last_activity", "digest", "-digest"], default="last_activity"),
        active_from=dict(),
        page_size=dict(type=int, default=100),
        page=dict(type=int, default=1),
        list_namespaces=dict(type=bool),
        list_repositories=dict(type=bool),
        get_repository_summary=dict(type=bool),
        get_repository_images=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=(
            ("list_repositories", True, ["username"]),
            ("get_repository_summary", True, ["namespace", "repository"]),
            ("get_repository_images", True, ["namespace", "repository"]),
        )
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["token"]),
        "Content-Type": "application/json"
    }
    params = {
        "page_size": module.params["page_size"],
        "page": module.params["page"]
    }
    if module.params["list_namespaces"]:
        url_suffix = "repositories/namespaces"
    elif module.params["list_repositories"]:
        url_suffix = "repositories/" + module.params["username"]
    elif module.params["get_repository_summary"]:
        url_suffix = "namespaces/{}/repositories/{}/images-summary".format(
            module.params["namespace"], module.params["repository"]
        )
    elif module.params["get_repository_images"]:
        params["status"] = module.params["status"]
        params["currently_tagged"] = module.params["currently_tagged"]
        params["ordering"] = module.params["ordering"]
        if not module.params["active_from"]:
            params["active_from"] = module.params["active_from"]

        url_suffix = "namespaces/{}/repositories/{}/images".format(
            module.params["namespace"], module.params["repository"]
        )
    else:
        module.fail_json("unknown parameters")

    r = requests.get(module.params["url"] + url_suffix, headers=headers)
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
