#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_delete_images
short_description: docker hub deletes one or more images within a namespace.
description:
  - Deletes one or more images within a namespace.
  - This is currently limited to a single repostiory.
  - B(Docker image management features are a Pro or Team feature)
  - U(https://docs.docker.com/docker-hub/api/latest/#operation/PostNamespacesDeleteImages)
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
  namespace:
    description:
      - Namespace of the repository.
    required: true
    type: str
  manifests:
    description:
      - Image manifests to delete.
    type: list
    required: true
    suboptions:
      repository:
        description:
          - Name of the repository to delete the image from.
        type: str
        required: true
      digest:
        description:
          - Digest of the image to delete.
        type: str
        required: true
  active_from:
    description:
      - Sets the time from which an image must have been pushed or pulled to be counted as active.
      - Defaults to 1 month before the current time.
    required: false
    type: str
  ignore_warnings:
    description:
      - Warnings to ignore.
      - If a warning is not ignored then no deletions will happen and
      - the warning is returned in the response.
    type: list
    required: true
    suboptions:
      repository:
        description:
          - Name of the repository of the image to ignore the warning for.
        type: str
        required: true
      digest:
        description:
          - Digest of the image to ignore the warning for.
        type: str
        required: true
      warning:
        description:
          - Digest of the image to ignore the warning for.
        type: str
        required: false
        choices: ["is_active", "current_tag"]
        default: "current_tag"
      tags:
        description:
          - Digest of the image to ignore the warning for.
        type: list
        required: false
  dry_run:
    description:
      - If I(true) then will check and return errors
      - and unignored warnings for the deletion request
      - but will not delete any images.
    required: false
    type: bool
    default: false
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

- name: delete image from docker hub (required Pro license)
  community.missing_collection.docker_hub_delete_images:
    token: '{{ __.token }}'
    dry_run: false
    namespace: 'yournamespace'
    manifests:
      - repository: 'test'
        digest: 'sha256:6ff24033b35ff1f6f66e2fc8fa4792cf91f0fee8da57955051036dbb8b6a6d44'
    ignore_warnings:
      - repository: 'test'
        digest: 'sha256:6ff24033b35ff1f6f66e2fc8fa4792cf91f0fee8da57955051036dbb8b6a6d44'
        warning: 'current_tag'
        tags:
          - 'latest'
"""

RETURN = """
result:
  description: result of docker hub api.
  returned: when success.
  type: dict
  sample: {
    "dry_run": false,
    "metrics": {
      "manifest_deletes": 3,
      "manifest_errors": 0,
      "tag_deletes": 1,
      "tag_errors": 0
    }
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/"),
        token=dict(required=True, no_log=True),
        namespace=dict(required=True),
        manifests=dict(
            type=list,
            required=True,
            options=dict(
                repository=dict(required=True),
                digest=dict(required=True),
            )
        ),
        active_from=dict(),
        ignore_warnings=dict(
            type=list,
            required=True,
            options=dict(
                repository=dict(required=True),
                digest=dict(required=True),
                warning=dict(choices=["is_active", "current_tag"], default="current_tag"),
                tags=dict(type=list),
            )
        ),
        dry_run=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["token"]),
        "Content-Type": "application/json"
    }
    url_suffix = "namespaces/{}/delete-images".format(
        module.params["namespace"]
    )

    data = {
        "dry_run": module.params["dry_run"],
        "manifests": module.params["manifests"],
        "ignore_warnings": module.params["ignore_warnings"]
    }

    if module.params["active_from"]:
        data["active_from"] = module.params["active_from"]

    r = requests.post(
        module.params["url"] + url_suffix,
        json=data,
        headers=headers
    )
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
