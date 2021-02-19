#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_identitystore_info
short_description: Get Information about AWS SSO Identity Store (IdentityStore).
description:
  - Get Information about AWS SSO Identity Store (IdentityStore).
  - U(https://docs.aws.amazon.com/singlesignon/latest/IdentityStoreAPIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of AWS SSO Directory.
    required: false
    type: str
  list_groups:
    description:
      - do you want to get list of groups for given SSO I(id)?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get list of users for given SSO I(id)?
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
- name: "get list of groups"
  aws_identitystore_info:
    list_groups: true
    id: 'd-1234567890'

- name: "get list of users"
  aws_identitystore_info:
    list_users: true
    id: 'd-1234567890'
"""

RETURN = """
groups:
  description: list of groups.
  returned: when `list_groups` is defined and success.
  type: list
users:
  description: list of users.
  returned: when `list_users` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _identitystore(client, module):
    try:
        if module.params['list_groups']:
            if client.can_paginate('list_groups'):
                paginator = client.get_paginator('list_groups')
                return paginator.paginate(
                    IdentityStoreId=module.params['id']
                ), True
            else:
                return client.list_groups(
                    IdentityStoreId=module.params['id']
                ), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    IdentityStoreId=module.params['id'],
                ), True
            else:
                return client.list_users(
                    IdentityStoreId=module.params['id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS SSO Identity Store details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        group_id=dict(required=False),
        list_groups=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_groups', True, ['id']),
            ('list_users', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_groups',
                'list_users',
            )
        ],
    )

    client = module.client('identitystore', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _identitystore(client, module)

    if module.params['list_groups']:
        module.exit_json(groups=aws_response_list_parser(paginate, it, 'Groups'))
    elif module.params['list_users']:
        module.exit_json(users=aws_response_list_parser(paginate, it, 'Users'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
