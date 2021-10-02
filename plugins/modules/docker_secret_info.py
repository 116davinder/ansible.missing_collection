#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_secret_info
short_description: Get information about Docker Secrets.
description:
  - Get information about Docker Secrets.
  - U(https://docker-py.readthedocs.io/en/stable/secrets.html#)
version_added: 0.4.0
options:
  base_url:
    description:
      - docker unix sock location.
    required: false
    type: str
    default: "unix://var/run/docker.sock"
  id:
    description:
      - id of docker secret.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - docker
"""

EXAMPLES = """
- name: get all secrets
  community.missing_collection.docker_secret_info:
  register: '__'

- name: get info about one secret
  community.missing_collection.docker_secret_info:
    id: '{{ __.secrets[0].id }}'
"""

RETURN = """
secrets:
  description: list of all the docker secrets.
  returned: when success.
  type: list
attrs:
  description: attributes of given secret
  returned: when success and defined I(id).
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
import docker
from docker.errors import APIError


def main():
    argument_spec = dict(
        base_url=dict(default="unix://var/run/docker.sock"),
        id=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    client = docker.DockerClient(base_url=module.params["base_url"])

    try:
        if not module.params["id"]:
            results = []
            secrets = client.secrets.list()
            for secret in secrets:
                results.append(
                    {
                        "id": secret.id,
                        "name": secret.name
                    }
                )
            module.exit_json(secrets=results)
        else:
            secret = client.secrets.get(module.params["id"])
            module.exit_json(attrs=secret.attrs)
    except APIError as e:
        module.fail_json(e.explanation)
    finally:
        client.close()


if __name__ == "__main__":
    main()
