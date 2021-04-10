#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_securityhub_info
short_description: Get Information about AWS SecurityHub.
description:
  - Get Information about AWS SecurityHub.
  - U(https://docs.aws.amazon.com/securityhub/1.0/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  list_enabled_products_for_import:
    description:
      - do you want to get list of enabled_products_for_import?
    required: false
    type: bool
  list_invitations:
    description:
      - do you want to get invitations?
    required: false
    type: bool
  list_members:
    description:
      - do you want to get list of members?
    required: false
    type: bool
  list_organization_admin_accounts:
    description:
      - do you want to get organization_admin_accounts?
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
- name: "get list of enabled_products_for_import"
  aws_securityhub_info:
    list_enabled_products_for_import: true

- name: "get invitations"
  aws_securityhub_info:
    list_invitations: true

- name: "get list of members"
  aws_securityhub_info:
    list_members: true

- name: "get organization_admin_accounts"
  aws_securityhub_info:
    list_organization_admin_accounts: true
"""

RETURN = """
enabled_products_for_import:
  description: list of enabled_products_for_import.
  returned: when `list_enabled_products_for_import` is defined and success.
  type: list
invitations:
  description: get of invitations.
  returned: when `list_invitations` is defined and success.
  type: list
members:
  description: list of members.
  returned: when `list_members` is defined and success.
  type: list
organization_admin_accounts:
  description: list of organization_admin_accounts.
  returned: when `list_organization_admin_accounts` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _securityhub(client, module):
    try:
        if module.params['list_enabled_products_for_import']:
            if client.can_paginate('list_enabled_products_for_import'):
                paginator = client.get_paginator('list_enabled_products_for_import')
                return paginator.paginate(), True
            else:
                return client.list_enabled_products_for_import(), False
        elif module.params['list_invitations']:
            if client.can_paginate('list_invitations'):
                paginator = client.get_paginator('list_invitations')
                return paginator.paginate(), True
            else:
                return client.list_invitations(), False
        elif module.params['list_members']:
            if client.can_paginate('list_members'):
                paginator = client.get_paginator('list_members')
                return paginator.paginate(), True
            else:
                return client.list_members(), False
        elif module.params['list_organization_admin_accounts']:
            if client.can_paginate('list_organization_admin_accounts'):
                paginator = client.get_paginator('list_organization_admin_accounts')
                return paginator.paginate(), True
            else:
                return client.list_organization_admin_accounts(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS SecurityHub details')


def main():
    argument_spec = dict(
        list_enabled_products_for_import=dict(required=False, type=bool),
        list_invitations=dict(required=False, type=bool),
        list_members=dict(required=False, type=bool),
        list_organization_admin_accounts=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_enabled_products_for_import',
                'list_invitations',
                'list_members',
                'list_organization_admin_accounts',
            )
        ],
    )

    client = module.client('securityhub', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _securityhub(client, module)

    if module.params['list_enabled_products_for_import']:
        module.exit_json(enabled_products_for_import=aws_response_list_parser(paginate, it, 'ProductSubscriptions'))
    elif module.params['list_invitations']:
        module.exit_json(invitations=aws_response_list_parser(paginate, it, 'Invitations'))
    elif module.params['list_members']:
        module.exit_json(members=aws_response_list_parser(paginate, it, 'Members'))
    elif module.params['list_organization_admin_accounts']:
        module.exit_json(organization_admin_accounts=aws_response_list_parser(paginate, it, 'AdminAccounts'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
