#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_globalaccelerator_info
short_description: (WIP) Get Information about Amazon Global Accelerator.
description:
  - Get Information about Amazon Global Accelerator.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/globalaccelerator.html)
version_added: 0.0.6
options:
  arn:
    description:
      - can be arn of accelerator?
      - can be arn of listener?
    required: false
    type: str
    aliases: ['listener_arn', 'accelerator_arn']
  list_accelerators:
    description:
      - do you want to get list of accelerators?
    required: false
    type: bool
  list_byoip_cidrs:
    description:
      - do you want to get list of byoip cidrs?
    required: false
    type: bool
  list_custom_routing_accelerators:
    description:
      - do you want to get list of custom routing accelerators?
    required: false
    type: bool
  list_custom_routing_endpoint_groups:
    description:
      - do you want to get list of custom routing endpoint groups for given listener I(arn)?
    required: false
    type: bool
  list_custom_routing_listeners:
    description:
      - do you want to get list of custom routing listeners for given accelerator I(arn)?
    required: false
    type: bool
  list_custom_routing_port_mappings:
    description:
      - do you want to get list of custom routing port mappings for given accelerator I(arn)?
    required: false
    type: bool
  list_endpoint_groups:
    description:
      - do you want to get list of endpoint groups for given listener I(arn)?
    required: false
    type: bool
  list_listeners:
    description:
      - do you want to get list of listeners for given accelerator I(arn)?
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
- name: "get list of accelerators"
  aws_globalaccelerator_info:
    list_accelerators: true

- name: "get list of byoip cidrs"
  aws_globalaccelerator_info:
    list_byoip_cidrs: true

- name: "get list of custom routing accelerators"
  aws_globalaccelerator_info:
    list_custom_routing_accelerators: true

- name: "get list of custom routing endpoint groups"
  aws_globalaccelerator_info:
    list_custom_routing_endpoint_groups: true
    arn: 'test-listener-arn'

- name: "get list of custom routing listeners"
  aws_globalaccelerator_info:
    list_custom_routing_listeners: true
    arn: 'test-accelerator-arn'

- name: "get list of custom routing port mappings"
  aws_globalaccelerator_info:
    list_custom_routing_port_mappings: true
    arn: 'test-accelerator-arn'

- name: "get list of endpoint groups"
  aws_globalaccelerator_info:
    list_endpoint_groups: true
    arn: 'test-listener-arn'

- name: "get list of listeners"
  aws_globalaccelerator_info:
    list_listeners: true
    arn: 'test-accelerator-arn'
"""

RETURN = """
accelerators:
  description: list of accelerators.
  returned: when `list_accelerators` is defined and success.
  type: list
byoip_cidrs:
  description: list of byoip cidrs.
  returned: when `list_byoip_cidrs` is defined and success.
  type: list
custom_routing_accelerators:
  description: list of custom routing accelerators.
  returned: when `list_custom_routing_accelerators` is defined and success.
  type: list
custom_routing_endpoint_groups:
  description: list of custom routing endpoint groups.
  returned: when `list_custom_routing_endpoint_groups` is defined and success.
  type: list
custom_routing_listeners:
  description: list of custom_routing_listeners.
  returned: when `list_custom_routing_listeners` is defined and success.
  type: list
custom_routing_port_mappings:
  description: list of custom routing port mappings.
  returned: when `list_custom_routing_port_mappings` is defined and success.
  type: list
endpoint_groups:
  description: list of endpoint groups.
  returned: when `list_endpoint_groups` is defined and success.
  type: list
listeners:
  description: list of listeners.
  returned: when `list_listeners` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _globalaccelerator(client, module):
    try:
        if module.params['list_accelerators']:
            if client.can_paginate('list_accelerators'):
                paginator = client.get_paginator('list_accelerators')
                return paginator.paginate(), True
            else:
                return client.list_accelerators(), False
        elif module.params['list_byoip_cidrs']:
            if client.can_paginate('list_byoip_cidrs'):
                paginator = client.get_paginator('list_byoip_cidrs')
                return paginator.paginate(), True
            else:
                return client.list_byoip_cidrs(), False
        elif module.params['list_custom_routing_accelerators']:
            if client.can_paginate('list_custom_routing_accelerators'):
                paginator = client.get_paginator('list_custom_routing_accelerators')
                return paginator.paginate(), True
            else:
                return client.list_custom_routing_accelerators(), False
        elif module.params['list_custom_routing_endpoint_groups']:
            if client.can_paginate('list_custom_routing_endpoint_groups'):
                paginator = client.get_paginator('list_custom_routing_endpoint_groups')
                return paginator.paginate(
                    ListenerArn=module.params['arn'],
                ), True
            else:
                return client.list_custom_routing_endpoint_groups(
                    ListenerArn=module.params['arn'],
                ), False
        elif module.params['list_custom_routing_listeners']:
            if client.can_paginate('list_custom_routing_listeners'):
                paginator = client.get_paginator('list_custom_routing_listeners')
                return paginator.paginate(
                    AcceleratorArn=module.params['arn'],
                ), True
            else:
                return client.list_custom_routing_listeners(
                    AcceleratorArn=module.params['arn'],
                ), False
        elif module.params['list_custom_routing_port_mappings']:
            if client.can_paginate('list_custom_routing_port_mappings'):
                paginator = client.get_paginator('list_custom_routing_port_mappings')
                return paginator.paginate(
                    AcceleratorArn=module.params['arn'],
                ), True
            else:
                return client.list_custom_routing_port_mappings(
                    AcceleratorArn=module.params['arn'],
                ), False
        elif module.params['list_endpoint_groups']:
            if client.can_paginate('list_endpoint_groups'):
                paginator = client.get_paginator('list_endpoint_groups')
                return paginator.paginate(
                    ListenerArn=module.params['arn'],
                ), True
            else:
                return client.list_endpoint_groups(
                    ListenerArn=module.params['arn'],
                ), False
        elif module.params['list_listeners']:
            if client.can_paginate('list_listeners'):
                paginator = client.get_paginator('list_listeners')
                return paginator.paginate(
                    AcceleratorArn=module.params['arn'],
                ), True
            else:
                return client.list_listeners(
                    AcceleratorArn=module.params['arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Global Accelerator details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['listener_arn', 'accelerator_arn']),
        list_accelerators=dict(required=False, type=bool),
        list_byoip_cidrs=dict(required=False, type=bool),
        list_custom_routing_accelerators=dict(required=False, type=bool),
        list_custom_routing_endpoint_groups=dict(required=False, type=bool),
        list_custom_routing_listeners=dict(required=False, type=bool),
        list_custom_routing_port_mappings=dict(required=False, type=bool),
        list_endpoint_groups=dict(required=False, type=bool),
        list_listeners=dict(required=False, type=bool),

    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_custom_routing_endpoint_groups', True, ['arn']),
            ('list_custom_routing_listeners', True, ['arn']),
            ('list_custom_routing_port_mappings', True, ['arn']),
            ('list_endpoint_groups', True, ['arn']),
            ('list_listeners', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_accelerators',
                'list_byoip_cidrs',
                'list_custom_routing_accelerators',
                'list_custom_routing_endpoint_groups',
                'list_custom_routing_listeners',
                'list_custom_routing_port_mappings',
                'list_endpoint_groups',
                'list_listeners',
            )
        ],
    )

    client = module.client('globalaccelerator', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _globalaccelerator(client, module)

    if module.params['list_accelerators']:
        module.exit_json(accelerators=aws_response_list_parser(paginate, it, 'Accelerators'))
    elif module.params['list_byoip_cidrs']:
        module.exit_json(byoip_cidrs=aws_response_list_parser(paginate, it, 'ByoipCidrs'))
    elif module.params['list_custom_routing_accelerators']:
        module.exit_json(custom_routing_accelerators=aws_response_list_parser(paginate, it, 'Accelerators'))
    elif module.params['list_custom_routing_endpoint_groups']:
        module.exit_json(custom_routing_endpoint_groups=aws_response_list_parser(paginate, it, 'EndpointGroups'))
    elif module.params['list_custom_routing_listeners']:
        module.exit_json(custom_routing_listeners=aws_response_list_parser(paginate, it, 'Listeners'))
    elif module.params['list_custom_routing_port_mappings']:
        module.exit_json(custom_routing_port_mappings=aws_response_list_parser(paginate, it, 'PortMappings'))
    elif module.params['list_endpoint_groups']:
        module.exit_json(endpoint_groups=aws_response_list_parser(paginate, it, 'EndpointGroups'))
    elif module.params['list_listeners']:
        module.exit_json(listeners=aws_response_list_parser(paginate, it, 'Listeners'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
