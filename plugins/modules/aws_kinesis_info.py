#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kinesis_info
short_description: Get Information about Amazon Kinesis.
description:
  - Get Information about Amazon Kinesis.
  - U(https://docs.aws.amazon.com/kinesis/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  arn:
    description:
      - arn of stream.
    required: false
    type: str
    aliases: ['stream_arn']
  name:
    description:
      - name of stream.
    required: false
    type: str
    aliases: ['stream_name']
  list_shards:
    description:
      - do you want to get list of shards for given stream I(name)?
    required: false
    type: bool
  list_stream_consumers:
    description:
      - do you want to get list of stream_consumers for given stream I(arn)?
    required: false
    type: bool
  list_streams:
    description:
      - do you want to get list of streams?
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
- name: "get list of shards"
  aws_kinesis_info:
    list_shards: true
    name: 'stream-name'

- name: "get list of stream_consumers"
  aws_kinesis_info:
    list_stream_consumers: true
    arn: 'stream-arn'

- name: "get list of streams"
  aws_kinesis_info:
    list_streams: true
"""

RETURN = """
shards:
  description: list of shards.
  returned: when `list_shards` is defined and success.
  type: list
stream_consumers:
  description: list of stream_consumers.
  returned: when `list_stream_consumers` is defined and success.
  type: list
streams:
  description: list of streams.
  returned: when `list_streams` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kinesis(client, module):
    try:
        if module.params['list_shards']:
            if client.can_paginate('list_shards'):
                paginator = client.get_paginator('list_shards')
                return paginator.paginate(
                    StreamName=module.params['name'],
                ), True
            else:
                return client.list_shards(
                    StreamName=module.params['name'],
                ), False
        elif module.params['list_stream_consumers']:
            if client.can_paginate('list_stream_consumers'):
                paginator = client.get_paginator('list_stream_consumers')
                return paginator.paginate(
                    StreamARN=module.params['arn'],
                ), True
            else:
                return client.list_stream_consumers(
                    StreamARN=module.params['arn'],
                ), False
        elif module.params['list_streams']:
            if client.can_paginate('list_streams'):
                paginator = client.get_paginator('list_streams')
                return paginator.paginate(), True
            else:
                return client.list_streams(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Kinesis details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['stream_name']),
        arn=dict(required=False, aliases=['stream_arn']),
        list_shards=dict(required=False, type=bool),
        list_stream_consumers=dict(required=False, type=bool),
        list_streams=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_shards', True, ['name']),
            ('list_stream_consumers', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_shards',
                'list_stream_consumers',
                'list_streams',
            )
        ],
    )

    client = module.client('kinesis', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kinesis(client, module)

    if module.params['list_shards']:
        module.exit_json(shards=aws_response_list_parser(paginate, it, 'Shards'))
    elif module.params['list_stream_consumers']:
        module.exit_json(stream_consumers=aws_response_list_parser(paginate, it, 'Consumers'))
    elif module.params['list_streams']:
        module.exit_json(streams=aws_response_list_parser(paginate, it, 'StreamNames'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
