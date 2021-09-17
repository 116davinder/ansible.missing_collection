#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: containerd_info
short_description: Get Information from ContainerD Runtime.
description:
  - Get Information from ContainerD Runtime.
  - U(https://github.com/siemens/pycontainerd)
version_added: 0.4.0
options:
  sock_file:
    description:
      - containerd unix sock file location.
    required: true
    type: str
    default: 'unix:///run/containerd/containerd.sock'
  namespace:
    description:
      - name of containerd namespace.
    required: false
    type: str
  list_namespaces:
    description:
      - get list of namespaces.
    required: false
    type: bool
  list_containers:
    description:
      - get list of containers.
    required: false
    type: bool
  list_images:
    description:
      - get list of images.
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - grpc
  - containerd
'''

EXAMPLES = '''
- name: get all containerd namespaces
  community.missing_collection.containerd_info:
    list_namespaces: true

- name: get all images names from moby namespace
  community.missing_collection.containerd_info:
    list_images: true
    namespace: 'moby'

- name: get all container ids from moby namespace
  community.missing_collection.containerd_info:
    list_containers: true
    namespace: 'moby'
'''

RETURN = """
namspaces:
  description: list of containerd namespaces
  returned: when I(list_namespaces) and success.
  type: list
  sample: ['moby']
containers:
  description: list of containerd containers in given namespace.
  returned: when I(list_containers) and success.
  type: list
images:
  description: list of containerd images in given namespace.
  returned: when I(list_images) and success.
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
import grpc
from containerd.services.namespaces.v1 import namespace_pb2_grpc, namespace_pb2
from containerd.services.containers.v1 import containers_pb2_grpc, containers_pb2
from containerd.services.images.v1 import images_pb2_grpc, images_pb2


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sock_file=dict(default='unix:///run/containerd/containerd.sock'),
            namespace=dict(),
            list_namespaces=dict(type=bool),
            list_containers=dict(type=bool),
            list_images=dict(type=bool)
        )
    )

    module.warn("this module is beta level with insecure grpc channel")

    channel = grpc.insecure_channel(module.params['sock_file'])
    try:
        if module.params['list_namespaces']:
            namespacev1 = namespace_pb2_grpc.NamespacesStub(channel)
            results = namespacev1.List(
                namespace_pb2.ListNamespacesRequest()
            ).namespaces
            module.exit_json(
                namespaces=[i.name for i in results]
            )
        if module.params['list_containers']:
            containersv1 = containers_pb2_grpc.ContainersStub(channel)
            results = containersv1.List(
                containers_pb2.ListContainersRequest(),
                metadata=(
                    ('containerd-namespace', module.params['namespace']),
                )
            ).containers
            module.exit_json(containers=[i.id for i in results])
        elif module.params['list_images']:
            imagesv1 = images_pb2_grpc.ImagesStub(channel)
            results = imagesv1.List(
                images_pb2.ListImagesRequest(),
                metadata=(
                    ('containerd-namespace', module.params['namespace']),
                )
            ).images
            module.exit_json(
                images=[i.name for i in results]
            )
        else:
            module.fail_json(msg="unknown parameters")
    except grpc.RpcError as error:
        module.fail_json(error=error)
    finally:
        channel.close()


if __name__ == '__main__':
    main()
