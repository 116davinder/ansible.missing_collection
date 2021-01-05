#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudtrail_info
short_description: Get Information about AWS Cloudtrail.
description:
  - Get Information about AWS Cloudtrail.
  - U(https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  name:
    description:
      - name of the cloudtrail.
    required: false
    type: str
  get_trail:
    description:
      - do you want to fetch details about given trail name I(name)?
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
- name: "get all the trails"
  aws_cloudtrail_info:

- name: "get detail about specific trail"
  aws_cloudtrail_info:
    get_trail: true
    name: 'test'
"""

RETURN = """
trails:
  description: List of cloudtrails
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        "home_region": "us-east-1",
        "name": "test-trail",
        "trail_arn": "arn:aws:cloudtrail:us-east-1:xxxxxxxxx:trail/test-trail"
    },
  ]
trail:
  description: details about given trail name
  returned: when `name` and `get_trail` are defined and success
  type: dict
  sample: {
    "has_custom_event_selectors": true,
    "has_insight_selectors": false,
    "home_region": "us-east-1",
    "include_global_service_events": true,
    "is_multi_region_trail": true,
    "is_organization_trail": false,
    "log_file_validation_enabled": true,
    "name": "test-trail",
    "s3_bucket_name": "test-trail-bucket",
    "trail_arn": "arn:aws:cloudtrail:us-east-1:xxxxxxxxx:trail/test-trail"
  }
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


def _cloudtrail(client, module):
    try:
        if module.params['get_trail']:
            return client.get_trail(
                Name=module.params['name']
            ), False
        else:
            if client.can_paginate('list_trails'):
                paginator = client.get_paginator('list_trails')
                return paginator.paginate(), True
            else:
                return client.list_trails(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudtrail details')


def main():
    argument_spec = dict(
        name=dict(required=False, type=str),
        get_trail=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_trail', True, ['name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('cloudtrail', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudtrail(client, module)

    if module.params['get_trail']:
        module.exit_json(trail=camel_dict_to_snake_dict(_it['Trail']))
    else:
        module.exit_json(trails=aws_response_list_parser(paginate, _it, 'Trails'))


if __name__ == '__main__':
    main()
