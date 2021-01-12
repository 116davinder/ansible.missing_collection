#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

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
    aliases: ['arn']
  get_trail:
    description:
      - do you want to fetch details about given trail name I(name)?
    required: false
    type: bool
  get_trail_status:
    description:
      - do you want to fetch status detail about given trail name I(name)?
    required: false
    type: bool
  get_insight_selectors:
    description:
      - do you want to fetch insight selector detail about given trail name I(name)?
    required: false
    type: bool
  get_event_selectors:
    description:
      - do you want to fetch event selector detail about given trail name I(name)?
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
  register: __app

- name: "get detail about specific trail"
  aws_cloudtrail_info:
    get_trail: true
    name: '{{ __app.trails[0].name }}'

- name: "get status information about given trail"
  aws_cloudtrail_info:
    get_trail_status: true
    name: '{{ __app.trails[0].name }}'

- name: "get insight selectors about given trail"
  aws_cloudtrail_info:
    get_insight_selectors: true
    name: '{{ __app.trails[0].name }}'

- name: "get event selector about given trail"
  aws_cloudtrail_info:
    get_event_selectors: true
    arn: '{{ __app.trails[0].name }}'
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
status:
  description: status detail about given trail name
  returned: when `name` and `get_trail_status` are defined and success
  type: dict
  sample: {
    "is_logging": true,
    "latest_delivery_attempt_succeeded": "2021-01-06T13:22:52Z",
    "latest_delivery_attempt_time": "2021-01-06T13:22:52Z",
    "latest_delivery_time": "2021-01-06T15:22:52.719000+02:00",
    "latest_digest_delivery_time": "2021-01-06T14:55:16.802000+02:00",
    "latest_notification_attempt_succeeded": "",
    "latest_notification_attempt_time": "",
    "response_metadata": {},
    "start_logging_time": "2018-11-23T16:03:40.179000+02:00",
    "time_logging_started": "2018-11-23T14:03:40Z",
    "time_logging_stopped": ""
  }
insight_selector:
  description: event selector detail about given trail name
  returned: when `name` and `get_insight_selectors` are defined and success
  type: dict
  sample: {
    'trail_arn': 'string',
    'insight_selectors': [
        {
            'insight_type': 'ApiCallRateInsight'
        },
    ]
  }
event_selector:
  description: event selector detail about given trail name
  returned: when `name` and `get_event_selectors` are defined and success
  type: dict
  sample: {
    "event_selectors": [
        {
            "data_resources": [],
            "exclude_management_event_sources": [],
            "include_management_events": true,
            "read_write_type": "ReadOnly"
        }
    ],
    "response_metadata": {},
    "trail_arn": "arn:aws:cloudtrail:us-east-1:xxxxxxxxx:trail/test-trail",
    "advanced_event_selectors": []
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
        elif module.params['get_trail_status']:
            return client.get_trail_status(
                Name=module.params['name']
            ), False
        elif module.params['get_insight_selectors']:
            return client.get_insight_selectors(
                TrailName=module.params['name']
            ), False
        elif module.params['get_event_selectors']:
            return client.get_event_selectors(
                TrailName=module.params['name']
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
        name=dict(required=False, type=str, aliases=['arn']),
        get_trail=dict(required=False, type=bool),
        get_trail_status=dict(required=False, type=bool),
        get_insight_selectors=dict(required=False, type=bool),
        get_event_selectors=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_trail', True, ['name']),
            ('get_trail_status', True, ['name']),
            ('get_insight_selectors', True, ['name']),
            ('get_event_selectors', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'get_trail',
                'get_trail_status',
                'get_insight_selectors',
                'get_event_selectors',
            )
        ],
    )

    client = module.client('cloudtrail', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudtrail(client, module)

    if module.params['get_trail']:
        module.exit_json(trail=camel_dict_to_snake_dict(_it['Trail']))
    elif module.params['get_trail_status']:
        module.exit_json(status=camel_dict_to_snake_dict(_it))
    elif module.params['get_insight_selectors']:
        module.exit_json(insight_selector=camel_dict_to_snake_dict(_it))
    elif module.params['get_event_selectors']:
        module.exit_json(event_selector=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(trails=aws_response_list_parser(paginate, _it, 'Trails'))


if __name__ == '__main__':
    main()
