#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_firehose_info
short_description: Get Information about Amazon Firehose.
description:
  - Get Information about Amazon Firehose.
  - U(https://docs.aws.amazon.com/firehose/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  name:
    description:
      - name of delivery stream.
    required: false
    type: str
  describe_delivery_stream:
    description:
      - do you want to get details of given I(name)?
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
- name: "get list of delivery stream"
  aws_firehose_info:

- name: "get details of delivery stream"
  aws_firehose_info:
    describe_delivery_stream: true
    name: 'test'
"""

RETURN = """
delivery_stream_names:
  description: list of stream names.
  returned: when no argument is defined and success
  type: list
delivery_stream:
  description: details of delivery stream.
  returned: when `describe_delivery_stream` is defined and success
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _firehose(client, module):
    try:
        if module.params['describe_delivery_stream']:
            return client.describe_delivery_stream(
                DeliveryStreamName=module.params['name'],
            ), False
        else:
            if client.can_paginate('list_delivery_streams'):
                paginator = client.get_paginator('list_delivery_streams')
                return paginator.paginate(), True
            else:
                return client.list_delivery_streams(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Firehose Details')


def main():
    argument_spec = dict(
        name=dict(required=False),
        describe_delivery_stream=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_delivery_stream', True, ['name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('firehose', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _firehose(client, module)

    if module.params['describe_delivery_stream']:
        module.exit_json(delivery_stream=camel_dict_to_snake_dict(it['DeliveryStreamDescription']))
    else:
        module.exit_json(delivery_stream_names=aws_response_list_parser(paginate, it, 'DeliveryStreamNames'))


if __name__ == '__main__':
    main()
