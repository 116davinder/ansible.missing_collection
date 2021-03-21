#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediatailor_info
short_description: Get Information about AWS Elemental Media Tailor.
description:
  - Get Information about AWS Elemental Media Tailor.
  - U(https://docs.aws.amazon.com/mediatailor/latest/apireference/resources.html)
version_added: 0.0.7
options:
  name:
    description:
      - source location name.
    required: false
    type: str
    aliases: ['source_location_name']
  list_channels:
    description:
      - do you want to get list of channels?
    required: false
    type: bool
  list_playback_configurations:
    description:
      - do you want to get playback_configurations?
    required: false
    type: bool
  list_source_locations:
    description:
      - do you want to get list of source_locations?
    required: false
    type: bool
  list_vod_sources:
    description:
      - do you want to get vod_sources for given I(name)?
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
  aws_mediatailor_info:
    list_channels: true

- name: "get playback_configurations"
  aws_mediatailor_info:
    list_playback_configurations: true

- name: "get list of source_locations"
  aws_mediatailor_info:
    list_source_locations: true

- name: "get vod_sources"
  aws_mediatailor_info:
    list_vod_sources: true
    name: 'source-location-name'
"""

RETURN = """
channels:
  description: list of channels.
  returned: when `list_channels` is defined and success.
  type: list
playback_configurations:
  description: get of playback_configurations.
  returned: when `list_playback_configurations` is defined and success.
  type: list
source_locations:
  description: list of source_locations.
  returned: when `list_source_locations` is defined and success.
  type: list
vod_sources:
  description: list of vod_sources.
  returned: when `list_vod_sources` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediatailor(client, module):
    try:
        if module.params['list_channels']:
            if client.can_paginate('list_channels'):
                paginator = client.get_paginator('list_channels')
                return paginator.paginate(), True
            else:
                return client.list_channels(), False
        elif module.params['list_playback_configurations']:
            if client.can_paginate('list_playback_configurations'):
                paginator = client.get_paginator('list_playback_configurations')
                return paginator.paginate(), True
            else:
                return client.list_playback_configurations(), False
        elif module.params['list_source_locations']:
            if client.can_paginate('list_source_locations'):
                paginator = client.get_paginator('list_source_locations')
                return paginator.paginate(), True
            else:
                return client.list_source_locations(), False
        elif module.params['list_vod_sources']:
            if client.can_paginate('list_vod_sources'):
                paginator = client.get_paginator('list_vod_sources')
                return paginator.paginate(
                    SourceLocationName=module.params['name']
                ), True
            else:
                return client.list_vod_sources(
                    SourceLocationName=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental mediatailor details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['source_location_name']),
        list_channels=dict(required=False, type=bool),
        list_playback_configurations=dict(required=False, type=bool),
        list_source_locations=dict(required=False, type=bool),
        list_vod_sources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_vod_sources', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_channels',
                'list_playback_configurations',
                'list_source_locations',
                'list_vod_sources',
            )
        ],
    )

    client = module.client('mediatailor', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediatailor(client, module)

    if module.params['list_channels']:
        module.exit_json(channels=aws_response_list_parser(paginate, it, 'Items'))
    elif module.params['list_playback_configurations']:
        module.exit_json(playback_configurations=aws_response_list_parser(paginate, it, 'Items'))
    elif module.params['list_source_locations']:
        module.exit_json(source_locations=aws_response_list_parser(paginate, it, 'Items'))
    elif module.params['list_vod_sources']:
        module.exit_json(vod_sources=aws_response_list_parser(paginate, it, 'Items'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
