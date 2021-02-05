#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_fms_info
short_description: Get Information about Firewall Management Service (FMS).
description:
  - Get Information about Firewall Management Service (FMS).
  - U(https://docs.aws.amazon.com/fms/2018-01-01/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  default_lists:
    description:
      - do you want to fetch default list?
    required: false
    type: bool
    default: True
  policy_id:
    description:
      - id of the policy.
    required: false
    type: str
  list_apps_lists:
    description:
      - do you want to get list of apps lists?
    required: false
    type: bool
  list_policies:
    description:
      - do you want to get list of policies?
    required: false
    type: bool
  list_compliance_status:
    description:
      - do you want to get compliance status of given I(policy_id)?
    required: false
    type: bool
  list_member_accounts:
    description:
      - do you want to get list of member accounts?
    required: false
    type: bool
  list_protocols_lists:
    description:
      - do you want to get protocols list?
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
- name: "get list of apps list"
  aws_fms_info:
    list_apps_lists: true
    default_lists: true

- name: "get list of policies"
  aws_fms_info:
    list_policies: true

- name: "get details of compliance status"
  aws_fms_info:
    list_compliance_status: true
    policy_id: 'test'

- name: "get list of member accounts"
  aws_fms_info:
    list_member_accounts: true

- name: "get list of protocols lists"
  aws_fms_info:
    list_protocols_lists: true
    default_lists: true
"""

RETURN = """
apps_lists:
  description: list of apps lists.
  returned: when `list_apps_lists` is defined and success
  type: list
policies:
  description: list of policies.
  returned: when `list_policies` is defined and success
  type: list
compliance_status:
  description: details about compliance status.
  returned: when `list_compliance_status` is defined and success
  type: list
member_accounts:
  description: list of member accounts.
  returned: when `list_member_accounts` is defined and success
  type: list
protocols_lists:
  description: list of protocols lists.
  returned: when `list_protocols_lists` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _fms(client, module):
    try:
        if module.params['list_apps_lists']:
            if client.can_paginate('list_apps_lists'):
                paginator = client.get_paginator('list_apps_lists')
                return paginator.paginate(
                    DefaultLists=module.params['default_lists'],
                    MaxResults=100
                ), True
            else:
                return client.list_apps_lists(
                    DefaultLists=module.params['default_lists'],
                    MaxResults=100
                ), False
        elif module.params['list_policies']:
            if client.can_paginate('list_policies'):
                paginator = client.get_paginator('list_policies')
                return paginator.paginate(), True
            else:
                return client.list_policies(), False
        elif module.params['list_compliance_status']:
            if client.can_paginate('list_compliance_status'):
                paginator = client.get_paginator('list_compliance_status')
                return paginator.paginate(
                    PolicyId=module.params['policy_id']
                ), True
            else:
                return client.list_compliance_status(
                    PolicyId=module.params['policy_id']
                ), False
        elif module.params['list_member_accounts']:
            if client.can_paginate('list_member_accounts'):
                paginator = client.get_paginator('list_member_accounts')
                return paginator.paginate(), True
            else:
                return client.list_member_accounts(), False
        elif module.params['list_protocols_lists']:
            if client.can_paginate('list_protocols_lists'):
                paginator = client.get_paginator('list_protocols_lists')
                return paginator.paginate(
                    DefaultLists=module.params['default_lists'],
                    MaxResults=100
                ), True
            else:
                return client.list_protocols_lists(
                    DefaultLists=module.params['default_lists'],
                    MaxResults=100
                ), False
        else:
            if client.can_paginate('list_domain_names'):
                paginator = client.get_paginator('list_domain_names')
                return paginator.paginate(), True
            else:
                return client.list_domain_names(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon FMS details')


def main():
    argument_spec = dict(
        default_lists=dict(required=False, type=bool, default=True),
        policy_id=dict(required=False),
        list_apps_lists=dict(required=False, type=bool),
        list_policies=dict(required=False, type=bool),
        list_compliance_status=dict(required=False, type=bool),
        list_member_accounts=dict(required=False, type=bool),
        list_protocols_lists=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_compliance_status', True, ['policy_id']),
        ),
        mutually_exclusive=[
            (
                'list_apps_lists',
                'list_policies',
                'list_compliance_status',
                'list_member_accounts',
                'list_protocols_lists',
            )
        ],
    )

    client = module.client('fms', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _fms(client, module)

    if module.params['list_apps_lists']:
        module.exit_json(apps_lists=aws_response_list_parser(paginate, it, 'AppsLists'))
    elif module.params['list_policies']:
        module.exit_json(policies=aws_response_list_parser(paginate, it, 'PolicyList'))
    elif module.params['list_compliance_status']:
        module.exit_json(compliance_status=aws_response_list_parser(paginate, it, 'PolicyComplianceStatusList'))
    elif module.params['list_member_accounts']:
        module.exit_json(member_accounts=aws_response_list_parser(paginate, it, 'MemberAccounts'))
    elif module.params['list_protocols_lists']:
        module.exit_json(protocols_lists=aws_response_list_parser(paginate, it, 'ProtocolsLists'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
