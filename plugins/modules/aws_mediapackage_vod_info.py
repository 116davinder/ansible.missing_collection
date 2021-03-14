#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediapackage_vod_info
short_description: Get Information about AWS Elemental Mediapackage Vod.
description:
  - Get Information about AWS Elemental Mediapackage Vod.
  - U(https://docs.aws.amazon.com/mediapackage_vod/latest/apireference/resources.html)
version_added: 0.0.7
options:
  id:
    description:
      - packaging group id.
    required: false
    type: str
    aliases: ['packaging_group_id']
  list_assets:
    description:
      - do you want to get list of assets for given I(id)?
    required: false
    type: bool
  list_packaging_configurations:
    description:
      - do you want to get list of packaging_configurations for given I(id)?
    required: false
    type: bool
  list_packaging_groups:
    description:
      - do you want to get list of packaging_groups?
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
- name: "get list of assets"
  aws_mediapackage_vod_info:
    list_assets: true
    id: 'packaging_group_id'

- name: "get list of packaging_configurations"
  aws_mediapackage_vod_info:
    list_packaging_configurations: true
    id: 'packaging_group_id'

- name: "get list of packaging_groups"
  aws_mediapackage_vod_info:
    list_packaging_groups: true
"""

RETURN = """
assets:
  description: list of assets.
  returned: when `list_assets` is defined and success.
  type: list
packaging_configurations:
  description: list of packaging_configurations.
  returned: when `list_packaging_configurations` is defined and success.
  type: list
packaging_groups:
  description: list of packaging_groups.
  returned: when `list_packaging_groups` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediapackage_vod(client, module):
    try:
        if module.params['list_assets']:
            if client.can_paginate('list_assets'):
                paginator = client.get_paginator('list_assets')
                return paginator.paginate(
                    PackagingGroupId=module.params['id']
                ), True
            else:
                return client.list_assets(
                    PackagingGroupId=module.params['id']
                ), False
        elif module.params['list_packaging_configurations']:
            if client.can_paginate('list_packaging_configurations'):
                paginator = client.get_paginator('list_packaging_configurations')
                return paginator.paginate(
                    PackagingGroupId=module.params['id']
                ), True
            else:
                return client.list_packaging_configurations(
                    PackagingGroupId=module.params['id']
                ), False
        elif module.params['list_packaging_groups']:
            if client.can_paginate('list_packaging_groups'):
                paginator = client.get_paginator('list_packaging_groups')
                return paginator.paginate(), True
            else:
                return client.list_packaging_groups(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental Mediapackage Vod details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['packaging_group_id']),
        list_assets=dict(required=False, type=bool),
        list_packaging_configurations=dict(required=False, type=bool),
        list_packaging_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_assets', True, ['id']),
            ('list_packaging_configurations', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_assets',
                'list_packaging_configurations',
                'list_packaging_groups',
            )
        ],
    )

    client = module.client('mediapackage-vod', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediapackage_vod(client, module)

    if module.params['list_assets']:
        module.exit_json(assets=aws_response_list_parser(paginate, it, 'Assets'))
    elif module.params['list_packaging_configurations']:
        module.exit_json(packaging_configurations=aws_response_list_parser(paginate, it, 'PackagingConfigurations'))
    elif module.params['list_packaging_groups']:
        module.exit_json(packaging_groups=aws_response_list_parser(paginate, it, 'PackagingGroups'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
