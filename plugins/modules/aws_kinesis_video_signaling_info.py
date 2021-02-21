#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kinesis_video_signaling_info
short_description: Get Information about Amazon Kinesis Video Signaling Channels.
description:
  - Get Information about Amazon Kinesis Video Signaling Channels.
  - U(https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_Operations_Amazon_Kinesis_Video_Signaling_Channels.html)
version_added: 0.0.7
options:
  arn:
    description:
      - arn of channel.
    required: false
    type: str
    aliases: ['channel_arn']
  name:
    description:
      - name of stream.
    required: false
    type: str
    aliases: ['stream_name']
  get_ice_server_config:
    description:
      - do you want to get list of shards for given channel I(arn)?
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
- name: "get ice server config"
  aws_kinesis_video_signaling_info:
    get_ice_server_config: true
    arn: 'channel-arn'
"""

RETURN = """
ice_server_config:
  description: list of ice server config.
  returned: when `get_ice_server_config` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kinesis_video_signaling(client, module):
    try:
        if module.params['get_ice_server_config']:
            if client.can_paginate('get_ice_server_config'):
                paginator = client.get_paginator('get_ice_server_config')
                return paginator.paginate(
                    ChannelARN=module.params['arn'],
                ), True
            else:
                return client.get_ice_server_config(
                    ChannelARN=module.params['arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Kinesis Video Signaling details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['channel_arn']),
        get_ice_server_config=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_ice_server_config', True, ['arn']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('kinesis-video-signaling', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kinesis_video_signaling(client, module)

    if module.params['get_ice_server_config']:
        module.exit_json(ice_server_config=aws_response_list_parser(paginate, it, 'IceServerList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
