#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kinesis_video_archived_media_info
short_description: Get Information about Amazon Kinesis Video Streams Archived Media.
description:
  - Get Information about Amazon Kinesis Video Streams Archived Media.
  - U(https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_Operations_Amazon_Kinesis_Video_Streams_Archived_Media.html)
version_added: 0.0.7
options:
  name:
    description:
      - name of stream.
    required: false
    type: str
    aliases: ['stream_name']
  list_fragments:
    description:
      - do you want to get list of fragments for given stream I(name)?
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
- name: "get list of fragments"
  aws_kinesis_video_archived_media_info:
    list_fragments: true
    name: 'stream-name'
"""

RETURN = """
fragments:
  description: list of fragments.
  returned: when `list_fragments` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kinesis_video_archived_media(client, module):
    try:
        if module.params['list_fragments']:
            if client.can_paginate('list_fragments'):
                paginator = client.get_paginator('list_fragments')
                return paginator.paginate(
                    StreamName=module.params['name'],
                ), True
            else:
                return client.list_fragments(
                    StreamName=module.params['name'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Kinesis Video Archived Media details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['stream_name']),
        list_fragments=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_fragments', True, ['name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('kinesis-video-archived-media', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kinesis_video_archived_media(client, module)

    if module.params['list_fragments']:
        module.exit_json(fragments=aws_response_list_parser(paginate, it, 'Fragments'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
