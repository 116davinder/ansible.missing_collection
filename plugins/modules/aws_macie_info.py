#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_macie_info
short_description: Get Information about Amazon Macie.
description:
  - Get Information about Amazon Macie.
  - U(https://docs.aws.amazon.com/macie/1.0/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  id:
    description:
      - member account id.
    required: false
    type: str
  list_member_accounts:
    description:
      - do you want to get list of member_accounts?
    required: false
    type: bool
  list_s3_resources:
    description:
      - do you want to get list of s3_resources for given I(id))?
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
- name: "get list of member_accounts"
  aws_macie_info:
    list_member_accounts: true

- name: "get list of s3_resources"
  aws_macie_info:
    list_s3_resources: true
    id: 'member-account-id'
"""

RETURN = """
member_accounts:
  description: list of member_accounts.
  returned: when `list_member_accounts` is defined and success.
  type: list
s3_resources:
  description: list of s3_resources.
  returned: when `list_s3_resources` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _macie(client, module):
    try:
        if module.params['list_member_accounts']:
            if client.can_paginate('list_member_accounts'):
                paginator = client.get_paginator('list_member_accounts')
                return paginator.paginate(), True
            else:
                return client.list_member_accounts(), False
        elif module.params['list_s3_resources']:
            if client.can_paginate('list_s3_resources'):
                paginator = client.get_paginator('list_s3_resources')
                return paginator.paginate(
                    memberAccountId=module.params['id'],
                ), True
            else:
                return client.list_s3_resources(
                    memberAccountId=module.params['id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Macie details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        list_member_accounts=dict(required=False, type=bool),
        list_s3_resources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_s3_resources', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_member_accounts',
                'list_s3_resources',
            )
        ],
    )

    client = module.client('macie', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _macie(client, module)

    if module.params['list_member_accounts']:
        module.exit_json(member_accounts=aws_response_list_parser(paginate, it, 'memberAccounts'))
    elif module.params['list_s3_resources']:
        module.exit_json(s3_resources=aws_response_list_parser(paginate, it, 's3Resources'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
