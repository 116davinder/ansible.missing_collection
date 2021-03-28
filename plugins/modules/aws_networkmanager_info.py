#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_networkmanager_info
short_description: Get Information about AWS Network Manager (NetworkManager).
description:
  - Get Information about AWS Network Manager (NetworkManager).
  - U(https://docs.aws.amazon.com/networkmanager/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of global network.
    required: false
    type: str
    aliases: ['global_network_id']
  describe_global_networks:
    description:
      - do you want to get list of global_networks?
    required: false
    type: bool
  get_connections:
    description:
      - do you want to get connections for given I(id)?
    required: false
    type: bool
  get_customer_gateway_associations:
    description:
      - do you want to get list of customer_gateway_associations for given I(id)?
    required: false
    type: bool
  get_devices:
    description:
      - do you want to get devices for given I(id)?
    required: false
    type: bool
  get_link_associations:
    description:
      - do you want to get link_associations for given I(id)?
    required: false
    type: bool
  get_links:
    description:
      - do you want to get links for given I(id)?
    required: false
    type: bool
  get_sites:
    description:
      - do you want to get sites for given I(id)?
    required: false
    type: bool
  get_transit_gateway_registrations:
    description:
      - do you want to get transit_gateway_registrations?
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
- name: "get list of global_networks"
  aws_networkmanager_info:
    describe_global_networks: true

- name: "get connections"
  aws_networkmanager_info:
    get_connections: true
    id: 'global_network_id'

- name: "get list of customer_gateway_associations"
  aws_networkmanager_info:
    get_customer_gateway_associations: true
    id: 'global_network_id'

- name: "get devices"
  aws_networkmanager_info:
    get_devices: true
    id: 'global_network_id'

- name: "get link_associations"
  aws_networkmanager_info:
    get_link_associations: true
    id: 'global_network_id'

- name: "get links"
  aws_networkmanager_info:
    get_links: true
    id: 'global_network_id'

- name: "get sites"
  aws_networkmanager_info:
    get_sites: true
    id: 'global_network_id'

- name: "get transit_gateway_registrations"
  aws_networkmanager_info:
    get_transit_gateway_registrations: true
    id: 'global_network_id'
"""

RETURN = """
global_networks:
  description: list of global_networks.
  returned: when `describe_global_networks` is defined and success.
  type: list
connections:
  description: get of connections.
  returned: when `get_connections` is defined and success.
  type: list
customer_gateway_associations:
  description: list of customer_gateway_associations.
  returned: when `get_customer_gateway_associations` is defined and success.
  type: list
devices:
  description: list of devices.
  returned: when `get_devices` is defined and success.
  type: list
link_associations:
  description: list of link_associations.
  returned: when `get_link_associations` is defined and success.
  type: list
links:
  description: list of links.
  returned: when `get_links` is defined and success.
  type: list
sites:
  description: list of sites.
  returned: when `get_sites` is defined and success.
  type: list
transit_gateway_registrations:
  description: list of transit_gateway_registrations.
  returned: when `get_transit_gateway_registrations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _networkmanager(client, module):
    try:
        if module.params['describe_global_networks']:
            if client.can_paginate('describe_global_networks'):
                paginator = client.get_paginator('describe_global_networks')
                return paginator.paginate(), True
            else:
                return client.describe_global_networks(), False
        elif module.params['get_connections']:
            if client.can_paginate('get_connections'):
                paginator = client.get_paginator('get_connections')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_connections(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_customer_gateway_associations']:
            if client.can_paginate('get_customer_gateway_associations'):
                paginator = client.get_paginator('get_customer_gateway_associations')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_customer_gateway_associations(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_devices']:
            if client.can_paginate('get_devices'):
                paginator = client.get_paginator('get_devices')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_devices(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_link_associations']:
            if client.can_paginate('get_link_associations'):
                paginator = client.get_paginator('get_link_associations')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_link_associations(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_links']:
            if client.can_paginate('get_links'):
                paginator = client.get_paginator('get_links')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_links(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_sites']:
            if client.can_paginate('get_sites'):
                paginator = client.get_paginator('get_sites')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_sites(
                    GlobalNetworkId=module.params['id']
                ), False
        elif module.params['get_transit_gateway_registrations']:
            if client.can_paginate('get_transit_gateway_registrations'):
                paginator = client.get_paginator('get_transit_gateway_registrations')
                return paginator.paginate(
                    GlobalNetworkId=module.params['id']
                ), True
            else:
                return client.get_transit_gateway_registrations(
                    GlobalNetworkId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Network Manager (NetworkManager) details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['global_network_id']),
        name=dict(required=False, aliases=['db_cluster_parameter_group_name']),
        describe_global_networks=dict(required=False, type=bool),
        get_connections=dict(required=False, type=bool),
        get_customer_gateway_associations=dict(required=False, type=bool),
        get_devices=dict(required=False, type=bool),
        get_link_associations=dict(required=False, type=bool),
        get_links=dict(required=False, type=bool),
        get_sites=dict(required=False, type=bool),
        get_transit_gateway_registrations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_connections', True, ['id']),
            ('get_customer_gateway_associations', True, ['id']),
            ('get_devices', True, ['id']),
            ('get_link_associations', True, ['id']),
            ('get_links', True, ['id']),
            ('get_sites', True, ['id']),
            ('get_transit_gateway_registrations', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_global_networks',
                'get_connections',
                'get_customer_gateway_associations',
                'get_devices',
                'get_link_associations',
                'get_links',
                'get_sites',
                'get_transit_gateway_registrations',
            )
        ],
    )

    client = module.client('networkmanager', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _networkmanager(client, module)

    if module.params['describe_global_networks']:
        module.exit_json(global_networks=aws_response_list_parser(paginate, it, 'GlobalNetworks'))
    elif module.params['get_connections']:
        module.exit_json(connections=aws_response_list_parser(paginate, it, 'Connections'))
    elif module.params['get_customer_gateway_associations']:
        module.exit_json(customer_gateway_associations=aws_response_list_parser(paginate, it, 'CustomerGatewayAssociations'))
    elif module.params['get_devices']:
        module.exit_json(devices=aws_response_list_parser(paginate, it, 'Devices'))
    elif module.params['get_link_associations']:
        module.exit_json(link_associations=aws_response_list_parser(paginate, it, 'LinkAssociations'))
    elif module.params['get_links']:
        module.exit_json(links=aws_response_list_parser(paginate, it, 'Links'))
    elif module.params['get_sites']:
        module.exit_json(sites=aws_response_list_parser(paginate, it, 'Sites'))
    elif module.params['get_transit_gateway_registrations']:
        module.exit_json(transit_gateway_registrations=aws_response_list_parser(paginate, it, 'TransitGatewayRegistrations'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
