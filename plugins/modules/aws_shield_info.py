#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_shield_info
short_description: Get Information about Amazon Shield.
description:
  - Get Information about Amazon Shield.
  - U(https://docs.aws.amazon.com/waf/latest/DDOSAPIReference/API_Operations.html)
version_added: 0.0.9
options:
  id:
    description:
      - id of the protection group.
    required: false
    type: str
    aliases: ['protection_group_id']
  list_protection_groups:
    description:
      - do you want to get list of protection_groups?
    required: false
    type: bool
  list_protections:
    description:
      - do you want to get protections?
    required: false
    type: bool
  list_resources_in_protection_group:
    description:
      - do you want to get list of resources_in_protection_group for given I(id)
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
- name: "get list of protection_groups"
  aws_shield_info:
    list_protection_groups: true

- name: "get protections"
  aws_shield_info:
    list_protections: true

- name: "get list of resources_in_protection_group"
  aws_shield_info:
    list_resources_in_protection_group: true
    id: 'protection_group_id'
"""

RETURN = """
protection_groups:
  description: list of protection_groups.
  returned: when `list_protection_groups` is defined and success.
  type: list
protections:
  description: get of protections.
  returned: when `list_protections` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _shield(client, module):
    try:
        if module.params['list_protection_groups']:
            if client.can_paginate('list_protection_groups'):
                paginator = client.get_paginator('list_protection_groups')
                return paginator.paginate(), True
            else:
                return client.list_protection_groups(), False
        elif module.params['list_protections']:
            if client.can_paginate('list_protections'):
                paginator = client.get_paginator('list_protections')
                return paginator.paginate(), True
            else:
                return client.list_protections(), False
        elif module.params['list_resources_in_protection_group']:
            if client.can_paginate('list_resources_in_protection_group'):
                paginator = client.get_paginator('list_resources_in_protection_group')
                return paginator.paginate(
                    ProtectionGroupId=module.params['id']
                ), True
            else:
                return client.list_resources_in_protection_group(
                    ProtectionGroupId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Shield details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['protection_group_id']),
        list_protection_groups=dict(required=False, type=bool),
        list_protections=dict(required=False, type=bool),
        list_resources_in_protection_group=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_resources_in_protection_group', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_protection_groups',
                'list_protections',
                'list_resources_in_protection_group',
            )
        ],
    )

    client = module.client('shield', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _shield(client, module)

    if module.params['list_protection_groups']:
        module.exit_json(protection_groups=aws_response_list_parser(paginate, it, 'ProtectionGroups'))
    elif module.params['list_protections']:
        module.exit_json(protections=aws_response_list_parser(paginate, it, 'Protections'))
    elif module.params['list_resources_in_protection_group']:
        module.exit_json(resources_in_protection_group=aws_response_list_parser(paginate, it, 'ResourceArns'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
