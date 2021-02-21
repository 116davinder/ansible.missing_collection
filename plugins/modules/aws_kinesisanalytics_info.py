#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kinesisanalytics_info
short_description: Get Information about Amazon Kinesis Analytics.
description:
  - Get Information about Amazon Kinesis Analytics.
  - U(https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_Operations.html)
version_added: 0.0.7
options:
  list_applications:
    description:
      - do you want to get list of applications?
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
- name: "get list of applications"
  aws_kinesisanalytics_info:
    list_applications: true
"""

RETURN = """
applications:
  description: list of applications.
  returned: when `list_applications` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kinesisanalytics(client, module):
    try:
        if module.params['list_applications']:
            if client.can_paginate('list_applications'):
                paginator = client.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return client.list_applications(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Kinesis Analytics details')


def main():
    argument_spec = dict(
        list_applications=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[],
    )

    client = module.client('kinesisanalytics', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kinesisanalytics(client, module)

    if module.params['list_applications']:
        module.exit_json(applications=aws_response_list_parser(paginate, it, 'ApplicationSummaries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
