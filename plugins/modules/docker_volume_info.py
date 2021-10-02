#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_volume_info
short_description: Get information about Docker Volumes.
description:
  - Get information about Docker Volumes.
  - U(https://docker-py.readthedocs.io/en/stable/volumes.html#)
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
      - id of docker volume
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - docker
"""

EXAMPLES = """
- name: get all volumes
  community.missing_collection.docker_volume_info:
  register: '__'

- name: get info about one volume
  community.missing_collection.docker_volume_info:
    id: '{{ __.volumes[0].id }}'
"""

RETURN = """
volumes:
  description: list of all the docker volumes.
  returned: when success.
  type: list
  sample: [
    {
      "id": "34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02",
      "name": "34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02"
    }
  ]
attrs:
  description: attributes of given volume
  returned: when success and defined I(id).
  type: dict
  sample: {
    "CreatedAt": "2021-09-23T21:01:17Z",
    "Driver": "local",
    "Labels": null,
    "Mountpoint": "/var/lib/docker/volumes/34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02/_data",
    "Name": "34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02",
    "Options": null,
    "Scope": "local"
  }
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
            volumes = client.volumes.list()
            for volume in volumes:
                results.append(
                    {
                        "id": volume.id,
                        "name": volume.name
                    }
                )
            module.exit_json(volumes=results)
        else:
            volume = client.volumes.get(module.params["id"])
            module.exit_json(attrs=volume.attrs)
    except APIError as e:
        module.fail_json(e.explanation)
    finally:
        client.close()


if __name__ == "__main__":
    main()
