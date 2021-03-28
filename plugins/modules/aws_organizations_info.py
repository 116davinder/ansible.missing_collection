#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_organizations_info
short_description: Get Information about Amazon Organizations.
description:
  - Get Information about Amazon Organizations.
  - U(https://docs.aws.amazon.com/organizations/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of account.
    required: false
    type: str
    aliases: ['account_id']
  list_accounts:
    description:
      - do you want to get list of accounts?
    required: false
    type: bool
  list_aws_service_access_for_organization:
    description:
      - do you want to get aws_service_access_for_organization?
    required: false
    type: bool
  list_delegated_administrators:
    description:
      - do you want to get list of delegated_administrators?
    required: false
    type: bool
  list_delegated_services_for_account:
    description:
      - do you want to get delegated_services_for_account for given I(id)?
    required: false
    type: bool
  list_handshakes_for_account:
    description:
      - do you want to get handshakes_for_account?
    required: false
    type: bool
  list_handshakes_for_organization:
    description:
      - do you want to get instances?
    required: false
    type: bool
  list_roots:
    description:
      - do you want to get roots?
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
- name: "get list of accounts"
  aws_organizations_info:
    list_accounts: true

- name: "get aws_service_access_for_organization"
  aws_organizations_info:
    list_aws_service_access_for_organization: true

- name: "get list of delegated_administrators"
  aws_organizations_info:
    list_delegated_administrators: true

- name: "get delegated_services_for_account"
  aws_organizations_info:
    list_delegated_services_for_account: true
    id: 'account_id'

- name: "get handshakes_for_account"
  aws_organizations_info:
    list_handshakes_for_account: true

- name: "get instances"
  aws_organizations_info:
    list_handshakes_for_organization: true

- name: "get roots"
  aws_organizations_info:
    list_roots: true
"""

RETURN = """
accounts:
  description: list of accounts.
  returned: when `list_accounts` is defined and success.
  type: list
aws_service_access_for_organization:
  description: get of aws_service_access_for_organization.
  returned: when `list_aws_service_access_for_organization` is defined and success.
  type: list
delegated_administrators:
  description: list of delegated_administrators.
  returned: when `list_delegated_administrators` is defined and success.
  type: list
delegated_services_for_account:
  description: list of delegated_services_for_account.
  returned: when `list_delegated_services_for_account` is defined and success.
  type: list
handshakes_for_account:
  description: list of handshakes_for_account.
  returned: when `list_handshakes_for_account` is defined and success.
  type: list
handshakes_for_organization:
  description: list of handshakes_for_organization.
  returned: when `list_handshakes_for_organization` is defined and success.
  type: list
roots:
  description: list of roots.
  returned: when `list_roots` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _organizations(client, module):
    try:
        if module.params['list_accounts']:
            if client.can_paginate('list_accounts'):
                paginator = client.get_paginator('list_accounts')
                return paginator.paginate(), True
            else:
                return client.list_accounts(), False
        elif module.params['list_aws_service_access_for_organization']:
            if client.can_paginate('list_aws_service_access_for_organization'):
                paginator = client.get_paginator('list_aws_service_access_for_organization')
                return paginator.paginate(), True
            else:
                return client.list_aws_service_access_for_organization(), False
        elif module.params['list_delegated_administrators']:
            if client.can_paginate('list_delegated_administrators'):
                paginator = client.get_paginator('list_delegated_administrators')
                return paginator.paginate(), True
            else:
                return client.list_delegated_administrators(), False
        elif module.params['list_delegated_services_for_account']:
            if client.can_paginate('list_delegated_services_for_account'):
                paginator = client.get_paginator('list_delegated_services_for_account')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_delegated_services_for_account(
                    AccountId=module.params['id']
                ), False
        elif module.params['list_handshakes_for_account']:
            if client.can_paginate('list_handshakes_for_account'):
                paginator = client.get_paginator('list_handshakes_for_account')
                return paginator.paginate(), True
            else:
                return client.list_handshakes_for_account(), False
        elif module.params['list_handshakes_for_organization']:
            if client.can_paginate('list_handshakes_for_organization'):
                paginator = client.get_paginator('list_handshakes_for_organization')
                return paginator.paginate(), True
            else:
                return client.list_handshakes_for_organization(), False
        elif module.params['list_roots']:
            if client.can_paginate('list_roots'):
                paginator = client.get_paginator('list_roots')
                return paginator.paginate(), True
            else:
                return client.list_roots(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Organizations details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['account_id']),
        list_accounts=dict(required=False, type=bool),
        list_aws_service_access_for_organization=dict(required=False, type=bool),
        list_delegated_administrators=dict(required=False, type=bool),
        list_delegated_services_for_account=dict(required=False, type=bool),
        list_handshakes_for_account=dict(required=False, type=bool),
        list_handshakes_for_organization=dict(required=False, type=bool),
        list_roots=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_delegated_services_for_account', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_accounts',
                'list_aws_service_access_for_organization',
                'list_delegated_administrators',
                'list_delegated_services_for_account',
                'list_handshakes_for_account',
                'list_handshakes_for_organization',
                'list_roots',
            )
        ],
    )

    client = module.client('organizations', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _organizations(client, module)

    if module.params['list_accounts']:
        module.exit_json(accounts=aws_response_list_parser(paginate, it, 'Accounts'))
    elif module.params['list_aws_service_access_for_organization']:
        module.exit_json(aws_service_access_for_organization=aws_response_list_parser(paginate, it, 'EnabledServicePrincipals'))
    elif module.params['list_delegated_administrators']:
        module.exit_json(delegated_administrators=aws_response_list_parser(paginate, it, 'DelegatedAdministrators'))
    elif module.params['list_delegated_services_for_account']:
        module.exit_json(delegated_services_for_account=aws_response_list_parser(paginate, it, 'DelegatedServices'))
    elif module.params['list_handshakes_for_account']:
        module.exit_json(handshakes_for_account=aws_response_list_parser(paginate, it, 'Handshakes'))
    elif module.params['list_handshakes_for_organization']:
        module.exit_json(handshakes_for_organization=aws_response_list_parser(paginate, it, 'Handshakes'))
    elif module.params['list_roots']:
        module.exit_json(roots=aws_response_list_parser(paginate, it, 'Roots'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
