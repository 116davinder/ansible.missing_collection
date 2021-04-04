#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sdb_info
short_description: Get Information about Amazon SimpleDB.
description:
  - Get Information about Amazon SimpleDB.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sdb.html)
version_added: 0.0.8
options:
  list_domains:
    description:
      - do you want to get list of domains?
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
- name: "get list of sdb"
  aws_sdb_info:
    list_domains: true
"""

RETURN = """
domains:
  description: list of domains.
  returned: when `list_domains` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sdb(client, module):
    try:
        if module.params['list_domains']:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(), True
            else:
                return client.list_domains(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon SimpleDB details')


def main():
    argument_spec = dict(
        list_domains=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_domains',
            )
        ],
    )

    client = module.client('sdb', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sdb(client, module)

    if module.params['list_domains']:
        module.exit_json(domains=aws_response_list_parser(paginate, it, 'DomainNames'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
