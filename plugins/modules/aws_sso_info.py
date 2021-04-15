#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sso_info
short_description: Get Information about AWS Single Sign-On (SSO).
description:
  - Get Information about AWS Single Sign-On (SSO).
  - U(https://docs.aws.amazon.com/singlesignon/latest/PortalAPIReference/API_Operations.html)
version_added: 0.0.9
options:
  access_token:
    description:
      - access token.
    required: false
    type: str
  account_id:
    description:
      - account id
    required: false
    type: str
  list_account_roles:
    description:
      - do you want to get list of account_roles for given I(access_token) and I(account_id)?
    required: false
    type: bool
  list_accounts:
    description:
      - do you want to get accounts for given I(access_token)?
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
- name: "get list of account_roles"
  aws_sso_info:
    list_account_roles: true
    access_token: 'access_token'
    account_id: '1234567890123'

- name: "get accounts"
  aws_sso_info:
    list_accounts: true
    access_token: 'access_token'
"""

RETURN = """
account_roles:
  description: list of account_roles.
  returned: when `list_account_roles` is defined and success.
  type: list
accounts:
  description: list of accounts.
  returned: when `list_accounts` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sso(client, module):
    try:
        if module.params['list_account_roles']:
            if client.can_paginate('list_account_roles'):
                paginator = client.get_paginator('list_account_roles')
                return paginator.paginate(
                    accessToken=module.params['access_token'],
                    accountId=module.params['account_id'],
                ), True
            else:
                return client.list_account_roles(
                    accessToken=module.params['access_token'],
                    accountId=module.params['account_id'],
                ), False
        elif module.params['list_accounts']:
            if client.can_paginate('list_accounts'):
                paginator = client.get_paginator('list_accounts')
                return paginator.paginate(
                    accessToken=module.params['access_token']
                ), True
            else:
                return client.list_accounts(
                    accessToken=module.params['access_token']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Single Sign-On (SSO) details')


def main():
    argument_spec = dict(
        access_token=dict(required=False),
        account_id=dict(required=False),
        list_account_roles=dict(required=False, type=bool),
        list_accounts=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_account_roles', True, ['access_token', 'account_id']),
            ('list_accounts', True, ['access_token']),
        ),
        mutually_exclusive=[
            (
                'list_account_roles',
                'list_accounts',
            )
        ],
    )

    client = module.client('sso', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sso(client, module)

    if module.params['list_account_roles']:
        module.exit_json(account_roles=aws_response_list_parser(paginate, it, 'roleList'))
    elif module.params['list_accounts']:
        module.exit_json(accounts=aws_response_list_parser(paginate, it, 'accountList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
