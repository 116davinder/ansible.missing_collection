#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_timestream_query_info
short_description: Get Information about Amazon Timestream Query.
description:
  - Get Information about Amazon Timestream Query.
  - U(https://docs.aws.amazon.com/timestream/latest/developerguide/API_Operations_Amazon_Timestream_Query.html)
version_added: 0.1.0
options:
  describe_endpoints:
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
  aws_timestream_query_info:
    describe_endpoints: true
"""

RETURN = """
endpoints:
  description: list of endpoints.
  returned: when `describe_endpoints` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _timestream_query(client, module):
    try:
        if module.params['describe_endpoints']:
            if client.can_paginate('describe_endpoints'):
                paginator = client.get_paginator('describe_endpoints')
                return paginator.paginate(), True
            else:
                return client.describe_endpoints(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Timestream Query details')


def main():
    argument_spec = dict(
        describe_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[],
    )

    client = module.client('timestream-query', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _timestream_query(client, module)

    if module.params['describe_endpoints']:
        module.exit_json(endpoints=aws_response_list_parser(paginate, it, 'Endpoints'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
