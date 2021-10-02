#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_configs_info
short_description: Get information about Docker Configs.
description:
  - Get information about Docker Configs.
  - U(https://docker-py.readthedocs.io/en/stable/configs.html#)
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
      - id of docker config
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - docker
"""

EXAMPLES = """
- name: get all configs
  community.missing_collection.docker_configs_info:
  register: '__'

- name: get info about one config
  community.missing_collection.docker_configs_info:
    id: '{{ __.configs[0].id }}'
"""

RETURN = """
configs:
  description: list of all the docker configs.
  returned: when success.
  type: list
attrs:
  description: attributes of given config
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
            configs = client.configs.list()
            for config in configs:
                results.append(
                    {
                        "id": config.id,
                        "name": config.name
                    }
                )
            module.exit_json(configs=results)
        else:
            config = client.configs.get(module.params["id"])
            module.exit_json(attrs=config.attrs)
    except APIError as e:
        module.fail_json(e.explanation)
    finally:
        client.close()


if __name__ == "__main__":
    main()
