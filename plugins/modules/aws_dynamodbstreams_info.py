#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dynamodbstreams_info
short_description: Get Information about Amazon DynamoDB Streams.
description:
  - Get Information about Amazon DynamoDB Streams.
  - U(https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB_Streams.html)
version_added: 0.0.5
options:
  name:
    description:
      - name of dynamodb table.
    required: false
    type: str
    aliases: ['table_name']
  stream_arn:
    description:
      - arn of stream.
    required: false
    type: str
  shard_id:
    description:
      - id of shard.
    required: false
    type: str
  shard_iterator_type:
    description:
      - type of shard iterator.
    required: false
    type: str
    choices: ['TRIM_HORIZON', 'LATEST', 'AT_SEQUENCE_NUMBER', 'AFTER_SEQUENCE_NUMBER']
  sequence_number:
    description:
      - sequence number.
    required: false
    type: str
  shard_iterator:
    description:
      - shard iterator.
    required: false
    type: list
  list_streams:
    description:
      - do you want to get list of streams for given I(name)?
    required: false
    type: bool
  describe_stream:
    description:
      - do you want to get summary about given stream I(stream_arn)?
    required: false
    type: bool
  get_shard_iterator:
    description:
      - do you want to get shard iterator for I(stream_arn), I(shard_id), I(shard_iterator_type) and I(sequence_number)?
    required: false
    type: bool
  get_records:
    description:
      - do you want to get records for given I(shard_iterator)?
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
- name: "get list of streams for given table name."
  aws_dynamodbstreams_info:
    list_streams: true
    table_name: 'test'

- name: "get summary about given stream arn."
  aws_dynamodbstreams_info:
    describe_stream: true
    stream_arn: 'test'

- name: "get shard iterator."
  aws_dynamodbstreams_info:
    get_shard_iterator: true
    stream_arn: 'test-arn'
    shard_id: 'test-id'
    shard_iterator_type: 'LATEST'
    sequence_number: 'test-number'

- name: "get records for given iterator."
  aws_dynamodbstreams_info:
    get_records: true
    shard_iterator: 'test'
"""

RETURN = """
streams:
  description: get list of streams for given table name.
  returned: when `list_streams` is defined and success
  type: list
stream:
  description: get summary about given stream arn.
  returned: when `describe_stream` is defined and success
  type: dict
shard_iterator:
  description: get shard iterator.
  returned: when `get_shard_iterator` is defined and success
  type: dict
records:
  description: get records for given iterator.
  returned: when `get_records` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _dynamodbstreams(client, module):
    try:
        if module.params['list_streams']:
            if client.can_paginate('list_streams'):
                paginator = client.get_paginator('list_streams')
                return paginator.paginate(
                    TableName=module.params['name'],
                ), True
            else:
                return client.list_streams(
                    TableName=module.params['name'],
                ), False
        elif module.params['describe_stream']:
            return client.describe_stream(
                StreamArn=module.params['stream_arn'],
            ), False
        elif module.params['get_shard_iterator']:
            return client.describe_stream(
                StreamArn=module.params['stream_arn'],
                ShardId=module.params['shard_id'],
                ShardIteratorType=module.params['shard_iterator_type'],
                SequenceNumber=module.params['sequence_number'],
            ), False
        elif module.params['get_records']:
            if client.can_paginate('get_records'):
                paginator = client.get_paginator('get_records')
                return paginator.paginate(
                    ShardIterator=module.params['shard_iterator'],
                ), True
            else:
                return client.get_records(
                    ShardIterator=module.params['shard_iterator'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS dynamodbstreams details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['table_name']),
        stream_arn=dict(required=False),
        shard_id=dict(required=False),
        shard_iterator_type=dict(
            required=False,
            choices=['TRIM_HORIZON', 'LATEST', 'AT_SEQUENCE_NUMBER', 'AFTER_SEQUENCE_NUMBER']
        ),
        sequence_number=dict(required=False),
        shard_iterator=dict(required=False),
        list_streams=dict(required=False, type=bool),
        describe_stream=dict(required=False, type=bool),
        get_shard_iterator=dict(required=False, type=bool),
        get_records=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_streams', True, ['name']),
            ('describe_stream', True, ['stream_arn']),
            ('get_shard_iterator', True, ['stream_arn', 'shard_id', 'shard_iterator_type', 'sequence_number']),
            ('get_records', True, ['shard_iterator']),
        ),
        mutually_exclusive=[
            (
                'list_streams',
                'describe_stream',
                'get_shard_iterator',
                'get_records',
            )
        ],
    )

    client = module.client('dynamodbstreams', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _dynamodbstreams(client, module)

    if module.params['list_streams']:
        module.exit_json(streams=aws_response_list_parser(paginate, it, 'Streams'))
    elif module.params['describe_stream']:
        module.exit_json(stream=camel_dict_to_snake_dict(it['StreamDescription']))
    elif module.params['get_shard_iterator']:
        module.exit_json(shard_iterator=camel_dict_to_snake_dict(it['ShardIterator']))
    elif module.params['get_records']:
        module.exit_json(records=aws_response_list_parser(paginate, it, 'Records'))
    else:
        module.fail_json_aws("unknown options are passed")


if __name__ == '__main__':
    main()
