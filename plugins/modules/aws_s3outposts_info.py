#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_s3outposts_info
short_description: Get Information about Amazon S3 on Outposts.
description:
  - Get Information about Amazon S3 on Outposts.
  - U(https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_AWS_S3_Control.html)
version_added: 0.0.9
options:
  list_endpoints:
    description:
      - do you want to get list of endpoints?
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
- name: "get list of endpoints"
  aws_s3outposts_info:
    list_endpoints: true
"""

RETURN = """
endpoints:
  description: list of endpoints.
  returned: when `list_endpoints` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _s3outposts(client, module):
    try:
        if module.params['list_endpoints']:
            if client.can_paginate('list_endpoints'):
                paginator = client.get_paginator('list_endpoints')
                return paginator.paginate(), True
            else:
                return client.list_endpoints(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon S3 on Outposts details')


def main():
    argument_spec = dict(
        list_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[],
    )

    client = module.client('s3outposts', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _s3outposts(client, module)

    if module.params['list_endpoints']:
        module.exit_json(endpoints=aws_response_list_parser(paginate, it, 'Endpoints'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
