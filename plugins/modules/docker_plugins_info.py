#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_plugins_info
short_description: Get information about Docker Plugins.
description:
  - Get information about Docker Plugins.
  - U(https://docker-py.readthedocs.io/en/stable/plugins.html#)
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
      - id of docker plugin
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - docker
"""

EXAMPLES = """
- name: get all plugins
  community.missing_collection.docker_plugins_info:
  register: '__'

- name: get info about one plugin
  community.missing_collection.docker_plugins_info:
    id: '{{ __.plugins[0].id }}'
"""

RETURN = """
plugins:
  description: list of all the docker plugins.
  returned: when success.
  type: list
  sample: [
    {
      "enabled": true,
      "id": "299f9f87dd9bd0052fb52fa2f5bd6d983b0d7b4f9d505cc07e37742bb17337bd",
      "name": "vieux/sshfs:latest"
    }
  ]
attrs:
  description: attributes of given plugin
  returned: when success and defined I(id).
  type: dict
  sample: {
    "Config": {
      "Args": {
        "Description": "",
        "Name": "",
        "Settable": null,
        "Value": null
      },
      "Description": "sshFS plugin for Docker",
      "DockerVersion": "18.05.0-ce-rc1",
      "Documentation": "https://docs.docker.com/engine/extend/plugins/",
      "Entrypoint": ["/docker-volume-sshfs"],
      "Env": [{
        "Description": "",
        "Name": "DEBUG",
        "Settable": ["value"],
        "Value": "0"
      }],
      "Interface": {
        "Socket": "sshfs.sock",
        "Types": ["docker.volumedriver/1.0"]
      },
      "IpcHost": false,
      "Linux": {
        "AllowAllDevices": false,
        "Capabilities": ["CAP_SYS_ADMIN"],
        "Devices": [{
          "Description": "",
          "Name": "",
          "Path": "/dev/fuse",
          "Settable": null
        }]
      },
      "Mounts": [{
        "Description": "",
        "Destination": "/mnt/state",
        "Name": "state",
        "Options": ["rbind"],
        "Settable": ["source"],
        "Source": "/var/lib/docker/plugins/",
        "Type": "bind"
      }, {
        "Description": "",
        "Destination": "/root/.ssh",
        "Name": "sshkey",
        "Options": ["rbind"],
        "Settable": ["source"],
        "Source": "",
        "Type": "bind"
      }],
      "Network": {
        "Type": "host"
      },
      "PidHost": false,
      "PropagatedMount": "/mnt/volumes",
      "User": {},
      "WorkDir": "",
      "rootfs": {
        "diff_ids": ["sha256:ce2b7a99c5db05cfe263bcd3640f2c1ce7c6f4619339633d44e65a8168ec3587"],
        "type": "layers"
      }
    },
    "Enabled": true,
    "Id": "299f9f87dd9bd0052fb52fa2f5bd6d983b0d7b4f9d505cc07e37742bb17337bd",
    "Name": "vieux/sshfs:latest",
    "PluginReference": "docker.io/vieux/sshfs:latest",
    "Settings": {
      "Args": [],
      "Devices": [{
        "Description": "",
        "Name": "",
        "Path": "/dev/fuse",
        "Settable": null
      }],
      "Env": ["DEBUG=0"],
      "Mounts": [{
        "Description": "",
        "Destination": "/mnt/state",
        "Name": "state",
        "Options": ["rbind"],
        "Settable": ["source"],
        "Source": "/var/lib/docker/plugins/",
        "Type": "bind"
      }, {
        "Description": "",
        "Destination": "/root/.ssh",
        "Name": "sshkey",
        "Options": ["rbind"],
        "Settable": ["source"],
        "Source": "",
        "Type": "bind"
      }]
    }
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
            plugins = client.plugins.list()
            for plugin in plugins:
                results.append(
                    {
                        "id": plugin.id,
                        "name": plugin.name,
                        "enabled": plugin.enabled
                    }
                )
            module.exit_json(plugins=results)
        else:
            plugin = client.plugins.get(module.params["id"])
            module.exit_json(attrs=plugin.attrs)
    except APIError as e:
        module.fail_json(e.explanation)
    finally:
        client.close()


if __name__ == "__main__":
    main()
