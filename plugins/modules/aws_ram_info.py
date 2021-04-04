#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ram_info
short_description: Get Information about AWS Resource Access Manager (RAM).
description:
  - Get Information about AWS Resource Access Manager (RAM).
  - U(https://docs.aws.amazon.com/ram/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  arn:
    description:
      - can be arn of invitation?
      - can be arn of resource share?
    required: false
    type: str
    aliases: ['resource_share_invitation_arn', 'resource_share_arn']
  resource_owner:
    description:
      - owner of the resource.
    required: false
    type: str
    choices: ['SELF', 'OTHER-ACCOUNTS']
    default: 'OTHER-ACCOUNTS'
  list_pending_invitation_resources:
    description:
      - do you want to get list of pending_invitation_resources for given resource share invitation I(arn)?
    required: false
    type: bool
  list_permissions:
    description:
      - do you want to get permissions?
    required: false
    type: bool
  list_principals:
    description:
      - do you want to get list of principals for given I(resource_owner)?
    required: false
    type: bool
  list_resource_share_permissions:
    description:
      - do you want to get resource_share_permissions for given resource share I(arn)?
    required: false
    type: bool
  list_resource_types:
    description:
      - do you want to get resource_types?
    required: false
    type: bool
  list_resources:
    description:
      - do you want to get resources for given I(resource_owner)?
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
- name: "get list of pending_invitation_resources"
  aws_ram_info:
    list_pending_invitation_resources: true
    arn: 'resource_share_invitation_arn'

- name: "get permissions"
  aws_ram_info:
    list_permissions: true

- name: "get list of principals"
  aws_ram_info:
    list_principals: true
    resource_owner: 'SELF'

- name: "get resource_share_permissions"
  aws_ram_info:
    list_resource_share_permissions: true
    arn: 'resource_share_arn'

- name: "get resource_types"
  aws_ram_info:
    list_resource_types: true

- name: "get resources"
  aws_ram_info:
    list_resources: true
    resource_owner: 'SELF'
"""

RETURN = """
pending_invitation_resources:
  description: list of pending_invitation_resources.
  returned: when `list_pending_invitation_resources` is defined and success.
  type: list
permissions:
  description: get of permissions.
  returned: when `list_permissions` is defined and success.
  type: list
principals:
  description: list of principals.
  returned: when `list_principals` is defined and success.
  type: list
resource_share_permissions:
  description: list of resource_share_permissions.
  returned: when `list_resource_share_permissions` is defined and success.
  type: list
resource_types:
  description: list of resource_types.
  returned: when `list_resource_types` is defined and success.
  type: list
resources:
  description: list of resources.
  returned: when `list_resources` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _ram(client, module):
    try:
        if module.params['list_pending_invitation_resources']:
            if client.can_paginate('list_pending_invitation_resources'):
                paginator = client.get_paginator('list_pending_invitation_resources')
                return paginator.paginate(
                    resourceShareInvitationArn=module.params['arn']
                ), True
            else:
                return client.list_pending_invitation_resources(
                    resourceShareInvitationArn=module.params['arn']
                ), False
        elif module.params['list_permissions']:
            if client.can_paginate('list_permissions'):
                paginator = client.get_paginator('list_permissions')
                return paginator.paginate(), True
            else:
                return client.list_permissions(), False
        elif module.params['list_principals']:
            if client.can_paginate('list_principals'):
                paginator = client.get_paginator('list_principals')
                return paginator.paginate(
                    resourceOwner=module.params['resource_owner']
                ), True
            else:
                return client.list_principals(
                    resourceOwner=module.params['resource_owner']
                ), False
        elif module.params['list_resource_share_permissions']:
            if client.can_paginate('list_resource_share_permissions'):
                paginator = client.get_paginator('list_resource_share_permissions')
                return paginator.paginate(
                    resourceShareArn=module.params['arn']
                ), True
            else:
                return client.list_resource_share_permissions(
                    resourceShareArn=module.params['arn']
                ), False
        elif module.params['list_resource_types']:
            if client.can_paginate('list_resource_types'):
                paginator = client.get_paginator('list_resource_types')
                return paginator.paginate(), True
            else:
                return client.list_resource_types(), False
        elif module.params['list_resources']:
            if client.can_paginate('list_resources'):
                paginator = client.get_paginator('list_resources')
                return paginator.paginate(
                    resourceOwner=module.params['resource_owner']
                ), True
            else:
                return client.list_resources(
                    resourceOwner=module.params['resource_owner']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon RAM details')


def main():
    argument_spec = dict(
        arn=dict(
            required=False,
            aliases=['resource_share_invitation_arn', 'resource_share_arn']
        ),
        resource_owner=dict(required=False, choices=['SELF', 'OTHER-ACCOUNTS'], default='OTHER-ACCOUNTS'),
        list_pending_invitation_resources=dict(required=False, type=bool),
        list_permissions=dict(required=False, type=bool),
        list_principals=dict(required=False, type=bool),
        list_resource_share_permissions=dict(required=False, type=bool),
        list_resource_types=dict(required=False, type=bool),
        list_resources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_pending_invitation_resources', True, ['arn']),
            ('list_resource_share_permissions', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_pending_invitation_resources',
                'list_permissions',
                'list_principals',
                'list_resource_share_permissions',
                'list_resource_types',
                'list_resources',
            )
        ],
    )

    client = module.client('ram', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ram(client, module)

    if module.params['list_pending_invitation_resources']:
        module.exit_json(pending_invitation_resources=aws_response_list_parser(paginate, it, 'resources'))
    elif module.params['list_permissions']:
        module.exit_json(permissions=aws_response_list_parser(paginate, it, 'permissions'))
    elif module.params['list_principals']:
        module.exit_json(principals=aws_response_list_parser(paginate, it, 'principals'))
    elif module.params['list_resource_share_permissions']:
        module.exit_json(resource_share_permissions=aws_response_list_parser(paginate, it, 'permissions'))
    elif module.params['list_resource_types']:
        module.exit_json(resource_types=aws_response_list_parser(paginate, it, 'resourceTypes'))
    elif module.params['list_resources']:
        module.exit_json(resources=aws_response_list_parser(paginate, it, 'resources'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
