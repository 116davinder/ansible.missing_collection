#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediapackage_info
short_description: Get Information about AWS Elemental MediaPackage.
description:
  - Get Information about AWS Elemental MediaPackage.
  - U(https://docs.aws.amazon.com/mediapackage/latest/apireference/resources.html)
version_added: 0.0.7
options:
  id:
    description:
      - channel id.
    required: false
    type: str
    aliases: ['channel_id']
  job_status:
    description:
      - filter harvest jobs.
    required: false
    type: str
    choices: ['IN_PROGRESS', 'SUCCEEDED', 'FAILED']
    default: 'SUCCEEDED'
  list_channels:
    description:
      - do you want to get list of channels?
    required: false
    type: bool
  list_harvest_jobs:
    description:
      - do you want to get list of harvest_jobs for given I(job_status)?
    required: false
    type: bool
  list_origin_endpoints:
    description:
      - do you want to get list of origin_endpoints for given channel I(id)?
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
  aws_mediapackage_info:
    list_channels: true

- name: "get list of harvest_jobs"
  aws_mediapackage_info:
    list_harvest_jobs: true
    job_status: 'SUCCEEDED'

- name: "get list of origin_endpoints"
  aws_mediapackage_info:
    list_origin_endpoints: true
    id: 'channel_id'
"""

RETURN = """
channels:
  description: list of channels.
  returned: when `list_channels` is defined and success.
  type: list
harvest_jobs:
  description: list of harvest_jobs.
  returned: when `list_harvest_jobs` is defined and success.
  type: list
origin_endpoints:
  description: list of origin_endpoints.
  returned: when `list_origin_endpoints` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediapackage(client, module):
    try:
        if module.params['list_channels']:
            if client.can_paginate('list_channels'):
                paginator = client.get_paginator('list_channels')
                return paginator.paginate(), True
            else:
                return client.list_channels(), False
        elif module.params['list_harvest_jobs']:
            if client.can_paginate('list_harvest_jobs'):
                paginator = client.get_paginator('list_harvest_jobs')
                return paginator.paginate(
                    IncludeStatus=module.params['job_status']
                ), True
            else:
                return client.list_harvest_jobs(
                    IncludeStatus=module.params['job_status']
                ), False
        elif module.params['list_origin_endpoints']:
            if client.can_paginate('list_origin_endpoints'):
                paginator = client.get_paginator('list_origin_endpoints')
                return paginator.paginate(
                    ChannelId=module.params['id']
                ), True
            else:
                return client.list_origin_endpoints(
                    ChannelId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental MediaPackage details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['channel_id']),
        job_status=dict(
            required=False,
            choices=['IN_PROGRESS', 'SUCCEEDED', 'FAILED'],
            default='SUCCEEDED'
        ),
        list_channels=dict(required=False, type=bool),
        list_harvest_jobs=dict(required=False, type=bool),
        list_origin_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_origin_endpoints', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_channels',
                'list_harvest_jobs',
                'list_origin_endpoints',
            )
        ],
    )

    client = module.client('mediapackage', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediapackage(client, module)

    if module.params['list_channels']:
        module.exit_json(channels=aws_response_list_parser(paginate, it, 'Channels'))
    elif module.params['list_harvest_jobs']:
        module.exit_json(harvest_jobs=aws_response_list_parser(paginate, it, 'HarvestJobs'))
    elif module.params['list_origin_endpoints']:
        module.exit_json(origin_endpoints=aws_response_list_parser(paginate, it, 'OriginEndpoints'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
