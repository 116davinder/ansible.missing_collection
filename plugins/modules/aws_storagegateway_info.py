#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_storagegateway_info
short_description: Get Information about AWS Storage Gateway.
description:
  - Get Information about AWS Storage Gateway.
  - U(https://docs.aws.amazon.com/storagegateway/latest/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  arn:
    description:
      - arn of the storage gateway.
    required: false
    type: str
    aliases: ['gateway_arn']
  list_automatic_tape_creation_policies:
    description:
      - do you want to get list of automatic_tape_creation_policies for given I(arn)?
    required: false
    type: bool
  list_file_shares:
    description:
      - do you want to get file_shares for given I(arn)?
    required: false
    type: bool
  list_file_system_associations:
    description:
      - do you want to get list of file_system_associations for given I(arn)?
    required: false
    type: bool
  list_gateways:
    description:
      - do you want to get gateways?
    required: false
    type: bool
  list_local_disks:
    description:
      - do you want to get local_disks for given I(arn)?
    required: false
    type: bool
  list_tape_pools:
    description:
      - do you want to get tape_pools?
    required: false
    type: bool
  list_tapes:
    description:
      - do you want to get tapes for given I(arn)?
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
- name: "get list of automatic_tape_creation_policies"
  aws_storagegateway_info:
    list_automatic_tape_creation_policies: true
    arn: 'gateway_arn'

- name: "get list of file_shares"
  aws_storagegateway_info:
    list_file_shares: true
    arn: 'gateway_arn'

- name: "get list of file_system_associations"
  aws_storagegateway_info:
    list_file_system_associations: true
    arn: 'gateway_arn'

- name: "get list of gateways"
  aws_storagegateway_info:
    list_gateways: true

- name: "get list of local_disks"
  aws_storagegateway_info:
    list_local_disks: true
    arn: 'gateway_arn'

- name: "get list of tape_pools"
  aws_storagegateway_info:
    list_tape_pools: true
    arn: 'gateway_arn'

- name: "get list of tapes"
  aws_storagegateway_info:
    list_tapes: true

- name: "get list of volumes"
  aws_storagegateway_info:
    list_volumes: true
    arn: 'gateway_arn'
"""

RETURN = """
automatic_tape_creation_policies:
  description: list of automatic_tape_creation_policies.
  returned: when `list_automatic_tape_creation_policies` is defined and success.
  type: list
file_shares:
  description: get of file_shares.
  returned: when `list_file_shares` is defined and success.
  type: list
file_system_associations:
  description: list of file_system_associations.
  returned: when `list_file_system_associations` is defined and success.
  type: list
gateways:
  description: list of gateways.
  returned: when `list_gateways` is defined and success.
  type: list
local_disks:
  description: list of local_disks.
  returned: when `list_local_disks` is defined and success.
  type: list
tape_pools:
  description: list of tape_pools.
  returned: when `list_tape_pools` is defined and success.
  type: list
tapes:
  description: list of tapes.
  returned: when `list_tapes` is defined and success.
  type: list
volumes:
  description: list of volumes.
  returned: when `list_volumes` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _storagegateway(client, module):
    try:
        if module.params['list_automatic_tape_creation_policies']:
            if client.can_paginate('list_automatic_tape_creation_policies'):
                paginator = client.get_paginator('list_automatic_tape_creation_policies')
                return paginator.paginate(
                    GatewayARN=module.params['arn']
                ), True
            else:
                return client.list_automatic_tape_creation_policies(
                    GatewayARN=module.params['arn']
                ), False
        elif module.params['list_file_shares']:
            if client.can_paginate('list_file_shares'):
                paginator = client.get_paginator('list_file_shares')
                return paginator.paginate(
                    GatewayARN=module.params['arn']
                ), True
            else:
                return client.list_file_shares(
                    GatewayARN=module.params['arn']
                ), False
        elif module.params['list_file_system_associations']:
            if client.can_paginate('list_file_system_associations'):
                paginator = client.get_paginator('list_file_system_associations')
                return paginator.paginate(
                    GatewayARN=module.params['arn']
                ), True
            else:
                return client.list_file_system_associations(
                    GatewayARN=module.params['arn']
                ), False
        elif module.params['list_gateways']:
            if client.can_paginate('list_gateways'):
                paginator = client.get_paginator('list_gateways')
                return paginator.paginate(), True
            else:
                return client.list_gateways(), False
        elif module.params['list_local_disks']:
            if client.can_paginate('list_local_disks'):
                paginator = client.get_paginator('list_local_disks')
                return paginator.paginate(
                    GatewayARN=module.params['arn']
                ), True
            else:
                return client.list_local_disks(
                    GatewayARN=module.params['arn']
                ), False
        elif module.params['list_tape_pools']:
            if client.can_paginate('list_tape_pools'):
                paginator = client.get_paginator('list_tape_pools')
                return paginator.paginate(), True
            else:
                return client.list_tape_pools(), False
        elif module.params['list_tapes']:
            if client.can_paginate('list_tapes'):
                paginator = client.get_paginator('list_tapes')
                return paginator.paginate(), True
            else:
                return client.list_tapes(), False
        elif module.params['list_volumes']:
            if client.can_paginate('list_volumes'):
                paginator = client.get_paginator('list_volumes')
                return paginator.paginate(
                    GatewayARN=module.params['arn']
                ), True
            else:
                return client.list_volumes(
                    GatewayARN=module.params['arn']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Storage Gateway details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['gateway_arn']),
        list_automatic_tape_creation_policies=dict(required=False, type=bool),
        list_file_shares=dict(required=False, type=bool),
        list_file_system_associations=dict(required=False, type=bool),
        list_gateways=dict(required=False, type=bool),
        list_local_disks=dict(required=False, type=bool),
        list_tape_pools=dict(required=False, type=bool),
        list_tapes=dict(required=False, type=bool),
        list_volumes=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_automatic_tape_creation_policies', True, ['arn']),
            ('list_file_shares', True, ['arn']),
            ('list_file_system_associations', True, ['arn']),
            ('list_local_disks', True, ['arn']),
            ('list_volumes', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_automatic_tape_creation_policies',
                'list_file_shares',
                'list_file_system_associations',
                'list_gateways',
                'list_local_disks',
                'list_tape_pools',
                'list_tapes',
                'list_volumes',
            )
        ],
    )

    client = module.client('storagegateway', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _storagegateway(client, module)

    if module.params['list_automatic_tape_creation_policies']:
        module.exit_json(automatic_tape_creation_policies=aws_response_list_parser(paginate, it, 'AutomaticTapeCreationPolicyInfos'))
    elif module.params['list_file_shares']:
        module.exit_json(file_shares=aws_response_list_parser(paginate, it, 'FileShareInfoList'))
    elif module.params['list_file_system_associations']:
        module.exit_json(file_system_associations=aws_response_list_parser(paginate, it, 'FileSystemAssociationSummaryList'))
    elif module.params['list_gateways']:
        module.exit_json(gateways=aws_response_list_parser(paginate, it, 'Gateways'))
    elif module.params['list_local_disks']:
        module.exit_json(local_disks=aws_response_list_parser(paginate, it, 'Disks'))
    elif module.params['list_tape_pools']:
        module.exit_json(tape_pools=aws_response_list_parser(paginate, it, 'PoolInfos'))
    elif module.params['list_tapes']:
        module.exit_json(tapes=aws_response_list_parser(paginate, it, 'TapeInfos'))
    elif module.params['list_volumes']:
        module.exit_json(volumes=aws_response_list_parser(paginate, it, 'VolumeInfos'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
