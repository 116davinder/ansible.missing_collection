#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_directconnect_info
short_description: Get Information about AWS Direct Connect.
description:
  - Get Information about AWS Direct Connect.
  - U(https://docs.aws.amazon.com/directconnect/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  id:
    description:
      - can be id of connection, interconnect, direct_connect_gateway or lag?
    required: false
    type: str
    aliases: [ 'connection_id', 'interconnect_id', 'direct_connect_gateway_id', 'lag_id' ]
  describe_connections:
    description:
      - do you want to get details about given connection I(id)?
    required: false
    type: bool
  describe_connections_on_interconnect:
    description:
      - do you want to get details about connections of given interconnect I(id)?
    required: false
    type: bool
  describe_direct_connect_gateway_association_proposals:
    description:
      - do you want to get details of association proposals of given direct connect gateway I(id)?
    required: false
    type: bool
  describe_direct_connect_gateway_attachments:
    description:
      - do you want to get details of association attachments of given direct connect gateway I(id)?
    required: false
    type: bool
  describe_hosted_connections:
    description:
      - do you want to get details about given hosted connections of given connection I(id)?
    required: false
    type: bool
  describe_interconnects:
    description:
      - do you want to get details about given interconnect I(id)?
    required: false
    type: bool
  describe_lags:
    description:
      - do you want to get details about link aggregation groups (LAG) of given lag I(id)?
    required: false
    type: bool
  describe_loa:
    description:
      - do you want to get details about the LOA-CFA for a connection I(id)?
    required: false
    type: bool
  describe_locations:
    description:
      - do you want to get details of direct connect locations?
    required: false
    type: bool
  describe_virtual_gateways:
    description:
      - do you want to get details about all virtual gateways?
    required: false
    type: bool
  describe_virtual_interfaces:
    description:
      - do you want to get details about virtual interfaces of given connection I(id)?
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
- name: "Gets detailed of all the direct connect gateways"
  aws_directconnect_info:

- name: "get details about given connection"
  aws_directconnect_info:
    describe_connections: true
    id: 'test-connection-id'

- name: "get details about connections of given interconnect"
  aws_directconnect_info:
    describe_connections_on_interconnect: true
    id: 'test-interconnect-id'

- name: "get details about given connection"
  aws_directconnect_info:
    describe_connections: true
    id: 'test-connection-id'

- name: "get details of association proposals of given direct connect gateway"
  aws_directconnect_info:
    describe_direct_connect_gateway_association_proposals: true
    id: 'test-connect-gateway-id'

- name: "get details of association attachments of given direct connect gateway"
  aws_directconnect_info:
    describe_direct_connect_gateway_attachments: true
    id: 'test-connect-gateway-id'

- name: "get details about given hosted connections"
  aws_directconnect_info:
    describe_hosted_connections: true
    id: 'test-connection-id'

- name: "get details about given interconnect"
  aws_directconnect_info:
    describe_interconnects: true
    id: 'test-interconnect-id'

- name: "gget details about link aggregation groups (LAG)"
  aws_directconnect_info:
    describe_lags: true
    id: 'test-connection-id'

- name: "get details about the LOA-CFA for a connection"
  aws_directconnect_info:
    describe_loa: true
    id: 'test-lag-id'

- name: "get details of direct connect locations"
  aws_directconnect_info:
    describe_locations: true

- name: "get details about all virtual gateways"
  aws_directconnect_info:
    describe_virtual_gateways: true

- name: "get details about virtual interfaces of given connection"
  aws_directconnect_info:
    describe_virtual_interfaces: true
    id: 'test-connection-id'
"""

RETURN = """
direct_connect_gateways:
  description: list of direct connect gateways
  returned: when no arguments are defined and success
  type: list
connections:
  description: detailed about direct connect connections.
  returned: when `describe_connections` or `describe_connections_on_interconnect` or `describe_hosted_connections` are defined and success
  type: list
direct_connect_gateway_association_proposals:
  description: get details of association proposals of given direct connect gateway
  returned: when `describe_direct_connect_gateway_association_proposals` is defined and success
  type: list
direct_connect_gateway_attachments:
  description: get details of association attachments of given direct connect gateway
  returned: when `describe_direct_connect_gateway_attachments` is defined and success
  type: list
interconnects:
  description: get details about given interconnect
  returned: when `describe_interconnects` is defined and success
  type: list
lags:
  description: get details about link aggregation groups (LAG)
  returned: when `describe_lags` is defined and success
  type: list
loa:
  description: get details about the LOA-CFA
  returned: when `describe_loa` is defined and success
  type: list
locations:
  description: get details of direct connect locations
  returned: when `describe_locations` is defined and success
  type: list
virtual_gateways:
  description: get details about all virtual gateways
  returned: when `describe_virtual_gateways` is defined and success
  type: list
virtual_interfaces:
  description: get details about virtual interfaces
  returned: when `describe_virtual_interfaces` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _directconnect(client, module):
    try:
        if module.params['describe_connections']:
            if client.can_paginate('describe_connections'):
                paginator = client.get_paginator('describe_connections')
                return paginator.paginate(
                    connectionId=module.params['id'],
                ), True
            else:
                return client.describe_connections(
                    connectionId=module.params['id'],
                ), False
        elif module.params['describe_connections_on_interconnect']:
            if client.can_paginate('describe_connections_on_interconnect'):
                paginator = client.get_paginator('describe_connections_on_interconnect')
                return paginator.paginate(
                    interconnectId=module.params['id'],
                ), True
            else:
                return client.describe_connections_on_interconnect(
                    interconnectId=module.params['id'],
                ), False
        elif module.params['describe_direct_connect_gateway_association_proposals']:
            if client.can_paginate('describe_direct_connect_gateway_association_proposals'):
                paginator = client.get_paginator('describe_direct_connect_gateway_association_proposals')
                return paginator.paginate(
                    directConnectGatewayId=module.params['id'],
                ), True
            else:
                return client.describe_direct_connect_gateway_association_proposals(
                    directConnectGatewayId=module.params['id'],
                ), False
        elif module.params['describe_direct_connect_gateway_attachments']:
            if client.can_paginate('describe_direct_connect_gateway_attachments'):
                paginator = client.get_paginator('describe_direct_connect_gateway_attachments')
                return paginator.paginate(
                    directConnectGatewayId=module.params['id'],
                ), True
            else:
                return client.describe_direct_connect_gateway_attachments(
                    directConnectGatewayId=module.params['id'],
                ), False
        elif module.params['describe_hosted_connections']:
            if client.can_paginate('describe_hosted_connections'):
                paginator = client.get_paginator('describe_hosted_connections')
                return paginator.paginate(
                    connectionId=module.params['id'],
                ), True
            else:
                return client.describe_hosted_connections(
                    connectionId=module.params['id'],
                ), False
        elif module.params['describe_interconnects']:
            if client.can_paginate('describe_interconnects'):
                paginator = client.get_paginator('describe_interconnects')
                return paginator.paginate(
                    interconnectId=module.params['id'],
                ), True
            else:
                return client.describe_interconnects(
                    interconnectId=module.params['id'],
                ), False
        elif module.params['describe_lags']:
            if client.can_paginate('describe_lags'):
                paginator = client.get_paginator('describe_lags')
                return paginator.paginate(
                    lagId=module.params['id'],
                ), True
            else:
                return client.describe_lags(
                    lagId=module.params['id'],
                ), False
        elif module.params['describe_loa']:
            return client.describe_loa(
                connectionId=module.params['id'],
            ), False
        elif module.params['describe_locations']:
            if client.can_paginate('describe_locations'):
                paginator = client.get_paginator('describe_locations')
                return paginator.paginate(), True
            else:
                return client.describe_locations(), False
        elif module.params['describe_virtual_gateways']:
            if client.can_paginate('describe_virtual_gateways'):
                paginator = client.get_paginator('describe_virtual_gateways')
                return paginator.paginate(), True
            else:
                return client.describe_virtual_gateways(), False
        elif module.params['describe_virtual_interfaces']:
            if client.can_paginate('describe_virtual_interfaces'):
                paginator = client.get_paginator('describe_virtual_interfaces')
                return paginator.paginate(
                    connectionId=module.params['id'],
                ), True
            else:
                return client.describe_virtual_interfaces(
                    connectionId=module.params['id'],
                ), False
        else:
            if client.can_paginate('describe_direct_connect_gateways'):
                paginator = client.get_paginator('describe_direct_connect_gateways')
                return paginator.paginate(), True
            else:
                return client.describe_direct_connect_gateways(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Direct Connect details')


def main():
    argument_spec = dict(
        id=dict(
            required=False,
            aliases=[
                'connection_id',
                'interconnect_id',
                'direct_connect_gateway_id',
                'lag_id',
            ]
        ),
        describe_connections=dict(required=False, type=bool),
        describe_connections_on_interconnect=dict(required=False, type=bool),
        describe_direct_connect_gateway_association_proposals=dict(required=False, type=bool),
        describe_direct_connect_gateway_attachments=dict(required=False, type=bool),
        describe_hosted_connections=dict(required=False, type=bool),
        describe_interconnects=dict(required=False, type=bool),
        describe_lags=dict(required=False, type=bool),
        describe_loa=dict(required=False, type=bool),
        describe_locations=dict(required=False, type=bool),
        describe_virtual_gateways=dict(required=False, type=bool),
        describe_virtual_interfaces=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_connections', True, ['id']),
            ('describe_connections_on_interconnect', True, ['id']),
            ('describe_direct_connect_gateway_association_proposals', True, ['id']),
            ('describe_direct_connect_gateway_attachments', True, ['id']),
            ('describe_hosted_connections', True, ['id']),
            ('describe_interconnects', True, ['id']),
            ('describe_lags', True, ['id']),
            ('describe_loa', True, ['id']),
            ('describe_virtual_interfaces', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_connections',
                'describe_connections_on_interconnect',
                'describe_direct_connect_gateway_association_proposals',
                'describe_direct_connect_gateway_attachments',
                'describe_hosted_connections',
                'describe_interconnects',
                'describe_lags',
                'describe_loa',
                'describe_locations',
                'describe_virtual_gateways',
                'describe_virtual_interfaces',
            )
        ],
    )

    client = module.client('directconnect', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _directconnect(client, module)

    if module.params['describe_connections'] or module.params['describe_connections_on_interconnect'] or module.params['describe_hosted_connections']:
        module.exit_json(connections=aws_response_list_parser(paginate, it, 'connections'))
    elif module.params['describe_direct_connect_gateway_association_proposals']:
        module.exit_json(direct_connect_gateway_association_proposals=aws_response_list_parser(paginate, it, 'directConnectGatewayAssociationProposals'))
    elif module.params['describe_direct_connect_gateway_attachments']:
        module.exit_json(direct_connect_gateway_attachments=aws_response_list_parser(paginate, it, 'directConnectGatewayAttachments'))
    elif module.params['describe_interconnects']:
        module.exit_json(interconnects=aws_response_list_parser(paginate, it, 'interconnects'))
    elif module.params['describe_lags']:
        module.exit_json(lags=aws_response_list_parser(paginate, it, 'lags'))
    elif module.params['describe_loa']:
        module.exit_json(loa=camel_dict_to_snake_dict(it))
    elif module.params['describe_locations']:
        module.exit_json(locations=aws_response_list_parser(paginate, it, 'locations'))
    elif module.params['describe_virtual_gateways']:
        module.exit_json(virtual_gateways=aws_response_list_parser(paginate, it, 'virtualGateways'))
    elif module.params['describe_virtual_interfaces']:
        module.exit_json(virtual_interfaces=aws_response_list_parser(paginate, it, 'virtualInterfaces'))
    else:
        module.exit_json(direct_connect_gateways=aws_response_list_parser(paginate, it, 'directConnectGateways'))


if __name__ == '__main__':
    main()
