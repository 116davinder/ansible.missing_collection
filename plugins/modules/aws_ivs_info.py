#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ivs_info
short_description: Get Information about Amazon Interactive Video Service (IVS).
description:
  - Get Information about Amazon Interactive Video Service (IVS).
  - U(https://docs.aws.amazon.com/ivs/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  arn:
    description:
      - channel arn.
    required: false
    type: str
    aliases: ['channel_arn']
  list_channels:
    description:
      - do you want to get list of channels?
    required: false
    type: bool
  list_playback_key_pairs:
    description:
      - do you want to get list of playback_key_pairs?
    required: false
    type: bool
  list_stream_keys:
    description:
      - do you want to get list of stream_keys for given channel I(arn)?
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
- name: "get list of channels"
  aws_ivs_info:
    list_channels: true

- name: "get list of playback_key_pairs"
  aws_ivs_info:
    list_playback_key_pairs: true

- name: "get list of stream_keys"
  aws_ivs_info:
    list_stream_keys: true
    arn: 'channel-arn'

- name: "get list of streams"
  aws_ivs_info:
    list_streams: true
"""

RETURN = """
channels:
  description: list of channels.
  returned: when `list_channels` is defined and success.
  type: list
playback_key_pairs:
  description: list of playback_key_pairs.
  returned: when `list_playback_key_pairs` is defined and success.
  type: list
stream_keys:
  description: list of stream_keys.
  returned: when `list_stream_keys` is defined and success.
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


def _ivs(client, module):
    try:
        if module.params['list_channels']:
            if client.can_paginate('list_channels'):
                paginator = client.get_paginator('list_channels')
                return paginator.paginate(), True
            else:
                return client.list_channels(), False
        elif module.params['list_playback_key_pairs']:
            if client.can_paginate('list_playback_key_pairs'):
                paginator = client.get_paginator('list_playback_key_pairs')
                return paginator.paginate(), True
            else:
                return client.list_playback_key_pairs(), False
        elif module.params['list_stream_keys']:
            if client.can_paginate('list_stream_keys'):
                paginator = client.get_paginator('list_stream_keys')
                return paginator.paginate(
                    channelArn=module.params['arn']
                ), True
            else:
                return client.list_stream_keys(
                    channelArn=module.params['arn']
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
        module.fail_json_aws(e, msg='Failed to fetch Amazon ivs details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['channel_arn']),
        list_channels=dict(required=False, type=bool),
        list_playback_key_pairs=dict(required=False, type=bool),
        list_stream_keys=dict(required=False, type=bool),
        list_streams=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_stream_keys', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_channels',
                'list_playback_key_pairs',
                'list_stream_keys',
                'list_streams',
            )
        ],
    )

    client = module.client('ivs', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ivs(client, module)

    if module.params['list_channels']:
        module.exit_json(channels=aws_response_list_parser(paginate, it, 'channels'))
    elif module.params['list_playback_key_pairs']:
        module.exit_json(playback_key_pairs=aws_response_list_parser(paginate, it, 'keyPairs'))
    elif module.params['list_stream_keys']:
        module.exit_json(stream_keys=aws_response_list_parser(paginate, it, 'streamKeys'))
    elif module.params['list_streams']:
        module.exit_json(streams=aws_response_list_parser(paginate, it, 'streams'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
