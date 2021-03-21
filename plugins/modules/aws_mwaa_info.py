#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mwaa_info
short_description: Get Information about Amazon Managed Workflows for Apache Airflow (MWAA).
description:
  - Get Information about Amazon Managed Workflows for Apache Airflow (MWAA).
  - U(https://docs.aws.amazon.com/migrationhub-home-region/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  list_environments:
    description:
      - do you want to get list of environments?
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
- name: "get list of environments"
  aws_mwaa_info:
    list_environments: true
"""

RETURN = """
environments:
  description: list of environments.
  returned: when `list_environments` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mwaa(client, module):
    try:
        if module.params['list_environments']:
            if client.can_paginate('list_environments'):
                paginator = client.get_paginator('list_environments')
                return paginator.paginate(), True
            else:
                return client.list_environments(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Managed Workflows for Apache Airflow (MWAA) details')


def main():
    argument_spec = dict(
        list_environments=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_environments',
            )
        ],
    )

    client = module.client('mwaa', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mwaa(client, module)

    if module.params['list_environments']:
        module.exit_json(environments=aws_response_list_parser(paginate, it, 'Environments'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
