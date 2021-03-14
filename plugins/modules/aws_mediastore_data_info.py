#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediastore_data_info
short_description: Get Information about AWS Elemental Mediastore Data.
description:
  - Get Information about AWS Elemental Mediastore Data.
  - U(https://docs.aws.amazon.com/mediastore/latest/apireference/API_Operations_AWS_Elemental_MediaStore_Data_Plane.html)
version_added: 0.0.7
options:
  list_items:
    description:
      - do you want to get list of items?
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
- name: "get list of items"
  aws_mediastore_data_info:
    list_items: true
"""

RETURN = """
items:
  description: list of items.
  returned: when `list_items` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediastore_data(client, module):
    try:
        if module.params['list_items']:
            if client.can_paginate('list_items'):
                paginator = client.get_paginator('list_items')
                return paginator.paginate(), True
            else:
                return client.list_items(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental mediastore_data details')


def main():
    argument_spec = dict(
        list_items=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_items',
            )
        ],
    )

    client = module.client('mediastore-data', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediastore_data(client, module)

    if module.params['list_items']:
        module.exit_json(items=aws_response_list_parser(paginate, it, 'Items'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
