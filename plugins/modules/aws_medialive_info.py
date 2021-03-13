#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_medialive_info
short_description: Get Information about AWS Elemental MediaLive.
description:
  - Get Information about AWS Elemental MediaLive.
  - U(https://docs.aws.amazon.com/medialive/latest/api/resources.html)
version_added: 0.0.7
options:
  id:
    description:
      - multiplex id.
    required: false
    type: str
  transfer_type:
    description:
      - type of transfer.
    required: false
    type: str
    choices: ['OUTGOING', 'INCOMING']
    default: 'INCOMING'
  list_channels:
    description:
      - do you want to get list of channels?
    required: false
    type: bool
  list_input_device_transfers:
    description:
      - do you want to get list of input_device_transfers for given I(transfer_type)?
    required: false
    type: bool
  list_input_devices:
    description:
      - do you want to get list of input_devices?
    required: false
    type: bool
  list_input_security_groups:
    description:
      - do you want to get list of input_security_groups?
    required: false
    type: bool
  list_inputs:
    description:
      - do you want to get list of inputs?
    required: false
    type: bool
  list_multiplex_programs:
    description:
      - do you want to get list of multiplex_programs for given I(id)?
    required: false
    type: bool
  list_offerings:
    description:
      - do you want to get list of offerings?
    required: false
    type: bool
  list_reservations:
    description:
      - do you want to get list of reservations?
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
- name: "get list of channels"
  aws_medialive_info:
    list_channels: true

- name: "get list of input_device_transfers"
  aws_medialive_info:
    list_input_device_transfers: true
    transfer_type: 'INCOMING'

- name: "get list of input_devices"
  aws_medialive_info:
    list_input_devices: true

- name: "get list of input_security_groups"
  aws_medialive_info:
    list_input_security_groups: true

- name: "get list of inputs"
  aws_medialive_info:
    list_inputs: true

- name: "get list of multiplex_programs"
  aws_medialive_info:
    list_multiplex_programs: true
    id: 'mutliplex-id'

- name: "get list of multiplexes"
  aws_medialive_info:
    list_multiplexes: true

- name: "get list of offerings"
  aws_medialive_info:
    list_offerings: true

- name: "get list of reservations"
  aws_medialive_info:
    list_reservations: true
"""

RETURN = """
channels:
  description: list of channels.
  returned: when `list_channels` is defined and success.
  type: list
input_device_transfers:
  description: list of input_device_transfers.
  returned: when `list_input_device_transfers` is defined and success.
  type: list
input_devices:
  description: list of input_devices.
  returned: when `list_input_devices` is defined and success.
  type: list
input_security_groups:
  description: list of input_security_groups.
  returned: when `list_input_security_groups` is defined and success.
  type: list
inputs:
  description: list of inputs.
  returned: when `list_inputs` is defined and success.
  type: list
multiplex_programs:
  description: list of multiplex_programs.
  returned: when `list_multiplex_programs` is defined and success.
  type: list
multiplexes:
  description: list of multiplexes.
  returned: when `list_multiplexes` is defined and success.
  type: list
offerings:
  description: list of offerings.
  returned: when `list_offerings` is defined and success.
  type: list
reservations:
  description: list of reservations.
  returned: when `list_reservations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _medialive(client, module):
    try:
        if module.params['list_channels']:
            if client.can_paginate('list_channels'):
                paginator = client.get_paginator('list_channels')
                return paginator.paginate(), True
            else:
                return client.list_channels(), False
        elif module.params['list_input_device_transfers']:
            if client.can_paginate('list_input_device_transfers'):
                paginator = client.get_paginator('list_input_device_transfers')
                return paginator.paginate(
                    TransferType=module.params['transfer_type']
                ), True
            else:
                return client.list_input_device_transfers(
                    TransferType=module.params['transfer_type']
                ), False
        elif module.params['list_input_devices']:
            if client.can_paginate('list_input_devices'):
                paginator = client.get_paginator('list_input_devices')
                return paginator.paginate(), True
            else:
                return client.list_input_devices(), False
        elif module.params['list_input_security_groups']:
            if client.can_paginate('list_input_security_groups'):
                paginator = client.get_paginator('list_input_security_groups')
                return paginator.paginate(), True
            else:
                return client.list_input_security_groups(), False
        elif module.params['list_inputs']:
            if client.can_paginate('list_inputs'):
                paginator = client.get_paginator('list_inputs')
                return paginator.paginate(), True
            else:
                return client.list_inputs(), False
        elif module.params['list_multiplex_programs']:
            if client.can_paginate('list_multiplex_programs'):
                paginator = client.get_paginator('list_multiplex_programs')
                return paginator.paginate(
                    MultiplexId=module.params['id']
                ), True
            else:
                return client.list_multiplex_programs(
                    MultiplexId=module.params['id']
                ), False
        elif module.params['list_multiplexes']:
            if client.can_paginate('list_multiplexes'):
                paginator = client.get_paginator('list_multiplexes')
                return paginator.paginate(), True
            else:
                return client.list_multiplexes(), False
        elif module.params['list_offerings']:
            if client.can_paginate('list_offerings'):
                paginator = client.get_paginator('list_offerings')
                return paginator.paginate(), True
            else:
                return client.list_offerings(), False
        elif module.params['list_reservations']:
            if client.can_paginate('list_reservations'):
                paginator = client.get_paginator('list_reservations')
                return paginator.paginate(), True
            else:
                return client.list_reservations(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental MediaLive details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        transfer_type=dict(
            required=False,
            choices=['OUTGOING', 'INCOMING'],
            default='INCOMING'
        ),
        list_channels=dict(required=False, type=bool),
        list_input_device_transfers=dict(required=False, type=bool),
        list_input_devices=dict(required=False, type=bool),
        list_input_security_groups=dict(required=False, type=bool),
        list_inputs=dict(required=False, type=bool),
        list_multiplex_programs=dict(required=False, type=bool),
        list_multiplexes=dict(required=False, type=bool),
        list_offerings=dict(required=False, type=bool),
        list_reservations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_multiplex_programs', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_channels',
                'list_input_device_transfers',
                'list_input_devices',
                'list_input_security_groups',
                'list_inputs',
                'list_multiplex_programs',
                'list_multiplexes',
                'list_offerings',
                'list_reservations',
            )
        ],
    )

    client = module.client('medialive', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _medialive(client, module)

    if module.params['list_channels']:
        module.exit_json(channels=aws_response_list_parser(paginate, it, 'Channels'))
    elif module.params['list_input_device_transfers']:
        module.exit_json(input_device_transfers=aws_response_list_parser(paginate, it, 'InputDeviceTransfers'))
    elif module.params['list_input_devices']:
        module.exit_json(input_devices=aws_response_list_parser(paginate, it, 'InputDevices'))
    elif module.params['list_input_security_groups']:
        module.exit_json(input_security_groups=aws_response_list_parser(paginate, it, 'InputSecurityGroups'))
    elif module.params['list_inputs']:
        module.exit_json(inputs=aws_response_list_parser(paginate, it, 'Inputs'))
    elif module.params['list_multiplex_programs']:
        module.exit_json(multiplex_programs=aws_response_list_parser(paginate, it, 'MultiplexPrograms'))
    elif module.params['list_multiplexes']:
        module.exit_json(multiplexes=aws_response_list_parser(paginate, it, 'Multiplexes'))
    elif module.params['list_offerings']:
        module.exit_json(offerings=aws_response_list_parser(paginate, it, 'Offerings'))
    elif module.params['list_reservations']:
        module.exit_json(reservations=aws_response_list_parser(paginate, it, 'Reservations'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
