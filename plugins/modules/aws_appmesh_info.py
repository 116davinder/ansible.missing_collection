#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_appmesh_info
short_description: Get details about AWS App Mesh Service.
description:
  - Get Information about AWS App Mesh Service.
  - U(https://docs.aws.amazon.com/app-mesh/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  name:
    description:
      - name of the app mesh.
    required: false
    type: str
    aliases: ['mesh_name']
  list_virtual_routers:
    description:
      - do you want to fetch all virtual routers for given I(mesh_name)/I(name)?
    required: false
    type: bool
  virtual_router_name:
    description:
      - name of the virtual router in given I(mesh_name)/I(name)?
    required: false
    type: str
  list_routes:
    description:
      - do you want to fetch all virtual routes for given I(mesh_name)/I(name) and I(virtual_router_name)?
    required: false
    type: bool
  list_virtual_nodes:
    description:
      - do you want to fetch all virtual nodes for given I(mesh_name)/I(name)?
    required: false
    type: bool
  list_virtual_gateways:
    description:
      - do you want to fetch all virtual gateways for given I(mesh_name)/I(name)?
    required: false
    type: bool
  list_virtual_services:
    description:
      - do you want to fetch all virtual services for given I(mesh_name)/I(name)?
    required: false
    type: bool
  virtual_gateway_name:
    description:
      - name of the virtual gateway for given I(mesh_name)/I(name)?
    required: false
    type: str
  list_gateway_routes:
    description:
      - do you want to fetch all virtual gateways routes for given I(mesh_name)/I(name) and I(virtual_gateway_name)?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
extends_documentation_fragment:
  - amazon.aws.ec2
  - amazon.aws.aws
requirements:
  - boto3
  - botocore
"""

EXAMPLES = """
- name: "list all app meshes"
  aws_appmesh_info:
  register: _all

- name: "list virtual routers for given mesh_name"
  aws_appmesh_info:
    name: 'test'
    list_virtual_routers: true

- name: "list virtual routes for given mesh_name and virtual_router_name"
  aws_appmesh_info:
    name: 'test'
    virtual_router_name: 'test'
    list_routes: true

- name: "list virtual nodes for given mesh_name"
  aws_appmesh_info:
    name: 'test'
    list_virtual_nodes: true

- name: "list virtual gateways for given mesh_name"
  aws_appmesh_info:
    name: 'test'
    list_virtual_gateways: true

- name: "list virtual services for given mesh_name"
  aws_appmesh_info:
    name: 'test'
    list_virtual_services: true

- name: "list virtual gateway routes for given mesh_name and virtual_gateway_name"
  aws_appmesh_info:
    name: 'test'
    virtual_gateway_name: 'test'
    list_gateway_routes: true
"""

RETURN = """
meshes:
  description: Returns a list of existing service meshes.
  returned: when no argument success
  type: list
  sample: [
    {
        'arn': 'string',
        'created_At': datetime(2015, 1, 4),
        'last_updated_at': datetime(2016, 5, 6),
        'mesh_name': 'string',
        'mesh_owner': 'string',
        'resource_owner': 'string',
        'version': 123
    },
  ]
virtual_routers:
  description: Returns a list of existing virtual routers in a service mesh.
  returned: when `name` and `list_virtual_routers` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2018, 8, 3),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'version': 123,
          'virtual_router_name': 'string'
      },
  ]
routes:
  description: Returns a list of existing routes in a service mesh.
  returned: when `name` and `virtual_router_name` and `list_routes` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2019, 9, 9),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'route_name': 'string',
          'version': 123,
          'virtual_router_name': 'string'
      },
  ]
virtual_nodes:
  description: Returns a list of existing virtual routers in a service mesh.
  returned: when `name` and `list_virtual_nodes` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2010, 2, 3),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'version': 123,
          'virtual_node_name': 'string'
      },
  ]
virtual_gateways:
  description: Returns a list of existing virtual routers in a service mesh.
  returned: when `name` and `list_virtual_gateways` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2010, 2, 3),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'version': 123,
          'virtual_gateway_name': 'string'
      },
  ]
virtual_services:
  description: Returns a list of existing virtual routers in a service mesh.
  returned: when `name` and `list_virtual_services` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2010, 2, 3),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'version': 123,
          'virtual_service_name': 'string'
      },
  ]
gateway_routes:
  description: Returns a list of existing virtual routers in a service mesh.
  returned: when `name` and `list_gateway_routes` and `virtual_gateway_name` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'created_at': datetime(2010, 2, 3),
          'last_updated_at': datetime(2015, 1, 1),
          'mesh_name': 'string',
          'mesh_owner': 'string',
          'resource_owner': 'string',
          'version': 123,
          'gateway_route_name': 'string',
          'virtual_gateway_name': 'string'
      },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _appmesh(client, module):
    try:
        if module.params['list_virtual_routers']:
            if client.can_paginate('list_virtual_routers'):
                paginator = client.get_paginator('list_virtual_routers')
                return paginator.paginate(
                    meshName=module.params['name']
                ), True
            else:
                return client.list_virtual_routers(
                    meshName=module.params['name']
                ), False
        elif module.params['list_routes']:
            if client.can_paginate('list_routes'):
                paginator = client.get_paginator('list_routes')
                return paginator.paginate(
                    meshName=module.params['name'],
                    virtualRouterName=module.params['virtual_router_name']
                ), True
            else:
                return client.list_routes(
                    meshName=module.params['name'],
                    virtualRouterName=module.params['virtual_router_name']
                ), False
        elif module.params['list_virtual_nodes']:
            if client.can_paginate('list_virtual_nodes'):
                paginator = client.get_paginator('list_virtual_nodes')
                return paginator.paginate(
                    meshName=module.params['name']
                ), True
            else:
                return client.list_virtual_nodes(
                    meshName=module.params['name']
                ), False
        elif module.params['list_virtual_gateways']:
            if client.can_paginate('list_virtual_gateways'):
                paginator = client.get_paginator('list_virtual_gateways')
                return paginator.paginate(
                    meshName=module.params['name']
                ), True
            else:
                return client.list_virtual_gateways(
                    meshName=module.params['name']
                ), False
        elif module.params['list_virtual_services']:
            if client.can_paginate('list_virtual_services'):
                paginator = client.get_paginator('list_virtual_services')
                return paginator.paginate(
                    meshName=module.params['name']
                ), True
            else:
                return client.list_virtual_services(
                    meshName=module.params['name']
                ), False
        elif module.params['list_gateway_routes']:
            if client.can_paginate('list_gateway_routes'):
                paginator = client.get_paginator('list_gateway_routes')
                return paginator.paginate(
                    meshName=module.params['name'],
                    virtualGatewayName=module.params['virtual_gateway_name']
                ), True
            else:
                return client.list_gateway_routes(
                    meshName=module.params['name'],
                    virtualGatewayName=module.params['virtual_gateway_name']
                ), False
        else:
            if client.can_paginate('list_meshes'):
                paginator = client.get_paginator('list_meshes')
                return paginator.paginate(), True
            else:
                return client.list_meshes(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws appmesh details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['mesh_name']),
        list_virtual_routers=dict(required=False, type=bool),
        virtual_router_name=dict(required=False),
        list_routes=dict(required=False, type=bool),
        list_virtual_nodes=dict(required=False, type=bool),
        list_virtual_gateways=dict(required=False, type=bool),
        list_virtual_services=dict(required=False, type=bool),
        virtual_gateway_name=dict(required=False),
        list_gateway_routes=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_virtual_routers', True, ['name']),
            ('list_virtual_nodes', True, ['name']),
            ('list_virtual_gateways', True, ['name']),
            ('list_virtual_services', True, ['name']),
            ('list_routes', True, ['name', 'virtual_router_name']),
            ('list_gateway_routes', True, ['name', 'virtual_gateway_name']),
        ],
        mutually_exclusive=[
            (
                'list_virtual_routers',
                'list_routes',
                'list_virtual_nodes',
                'list_virtual_gateways',
                'list_virtual_services',
            ),
        ],
    )

    client = module.client('appmesh', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _appmesh(client, module)

    if module.params['list_virtual_routers']:
        module.exit_json(virtual_routers=aws_response_list_parser(paginate, _it, 'virtualRouters'))
    elif module.params['list_routes']:
        module.exit_json(routes=aws_response_list_parser(paginate, _it, 'routes'))
    elif module.params['list_virtual_nodes']:
        module.exit_json(virtual_nodes=aws_response_list_parser(paginate, _it, 'virtualNodes'))
    elif module.params['list_virtual_gateways']:
        module.exit_json(virtual_gateways=aws_response_list_parser(paginate, _it, 'virtualGateways'))
    elif module.params['list_virtual_services']:
        module.exit_json(virtual_services=aws_response_list_parser(paginate, _it, 'virtualServices'))
    elif module.params['list_gateway_routes']:
        module.exit_json(gateway_routes=aws_response_list_parser(paginate, _it, 'gatewayRoutes'))
    else:
        module.exit_json(meshes=aws_response_list_parser(paginate, _it, 'meshes'))


if __name__ == '__main__':
    main()
