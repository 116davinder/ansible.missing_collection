#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_migrationhub_config_info
short_description: Get Information about AWS Migration Hub Config.
description:
  - Get Information about AWS Migration Hub Config.
  - U(https://docs.aws.amazon.com/migrationhub-home-region/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  region:
    description:
      - migration hub region.
    required: false
    type: str
    aliases: ['home_region']
  describe_home_region_controls:
    description:
      - do you want to get list of home_region_controls for given I(region)?
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
- name: "get list of home_region_controls"
  aws_migrationhub_config_info:
    describe_home_region_controls: true
    region: 'us-west-2'
"""

RETURN = """
home_region_controls:
  description: list of home_region_controls.
  returned: when `describe_home_region_controls` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _migrationhub_config(client, module):
    try:
        if module.params['describe_home_region_controls']:
            if client.can_paginate('describe_home_region_controls'):
                paginator = client.get_paginator('describe_home_region_controls')
                return paginator.paginate(
                    HomeRegion=module.params['region']
                ), True
            else:
                return client.describe_home_region_controls(
                    HomeRegion=module.params['region']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Migration Hub Config details')


def main():
    argument_spec = dict(
        region=dict(required=False, aliases=['home_region']),
        describe_home_region_controls=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_home_region_controls', True, ['region']),
        ),
        mutually_exclusive=[
            (
                'describe_home_region_controls',
            )
        ],
    )

    client = module.client('migrationhub-config', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _migrationhub_config(client, module)

    if module.params['describe_home_region_controls']:
        module.exit_json(home_region_controls=aws_response_list_parser(paginate, it, 'HomeRegionControls'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
