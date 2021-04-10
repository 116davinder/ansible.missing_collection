#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_s3control_info
short_description: Get Information about AWS S3 Control.
description:
  - Get Information about AWS S3 Control.
  - U(https://docs.aws.amazon.com/AmazonS3/latest/API/API_Operations_AWS_S3_Control.html)
version_added: 0.0.9
options:
  id:
    description:
      - aws account id.
    required: false
    type: str
    aliases: ['account_id']
  list_access_points:
    description:
      - do you want to get list of access_points for given account I(id)?
    required: false
    type: bool
  list_access_points_for_object_lambda:
    description:
      - do you want to get access_points_for_object_lambda for given account I(id)?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs for given account I(id)?
    required: false
    type: bool
  list_regional_buckets:
    description:
      - do you want to get regional_buckets for given account I(id)?
    required: false
    type: bool
  list_storage_lens_configurations:
    description:
      - do you want to get storage_lens_configurations for given account I(id)?
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
- name: "get list of access_points"
  aws_s3control_info:
    list_access_points: true
    id: 'account_id'

- name: "get access_points_for_object_lambda"
  aws_s3control_info:
    list_access_points_for_object_lambda: true
    id: 'account_id'

- name: "get list of jobs"
  aws_s3control_info:
    list_jobs: true
    id: 'account_id'

- name: "get regional_buckets"
  aws_s3control_info:
    list_regional_buckets: true
    id: 'account_id'

- name: "get storage_lens_configurations"
  aws_s3control_info:
    list_storage_lens_configurations: true
    id: 'account_id'
"""

RETURN = """
access_points:
  description: list of access_points.
  returned: when `list_access_points` is defined and success.
  type: list
access_points_for_object_lambda:
  description: get of access_points_for_object_lambda.
  returned: when `list_access_points_for_object_lambda` is defined and success.
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
regional_buckets:
  description: list of regional_buckets.
  returned: when `list_regional_buckets` is defined and success.
  type: list
storage_lens_configurations:
  description: list of storage_lens_configurations.
  returned: when `list_storage_lens_configurations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _s3control(client, module):
    try:
        if module.params['list_access_points']:
            if client.can_paginate('list_access_points'):
                paginator = client.get_paginator('list_access_points')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_access_points(
                    AccountId=module.params['id']
                ), False
        elif module.params['list_access_points_for_object_lambda']:
            if client.can_paginate('list_access_points_for_object_lambda'):
                paginator = client.get_paginator('list_access_points_for_object_lambda')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_access_points_for_object_lambda(
                    AccountId=module.params['id']
                ), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_jobs(
                    AccountId=module.params['id']
                ), False
        elif module.params['list_regional_buckets']:
            if client.can_paginate('list_regional_buckets'):
                paginator = client.get_paginator('list_regional_buckets')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_regional_buckets(
                    AccountId=module.params['id']
                ), False
        elif module.params['list_storage_lens_configurations']:
            if client.can_paginate('list_storage_lens_configurations'):
                paginator = client.get_paginator('list_storage_lens_configurations')
                return paginator.paginate(
                    AccountId=module.params['id']
                ), True
            else:
                return client.list_storage_lens_configurations(
                    AccountId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS S3 Control details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['account_id', 'resolver_endpoint_id']),
        list_access_points=dict(required=False, type=bool),
        list_access_points_for_object_lambda=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
        list_regional_buckets=dict(required=False, type=bool),
        list_storage_lens_configurations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_regional_buckets', True, ['id']),
            ('list_access_points_for_object_lambda', True, ['id']),
            ('list_jobs', True, ['id']),
            ('list_regional_buckets', True, ['id']),
            ('list_storage_lens_configurations', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_access_points',
                'list_access_points_for_object_lambda',
                'list_jobs',
                'list_regional_buckets',
                'list_storage_lens_configurations',
            )
        ],
    )

    client = module.client('s3control', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _s3control(client, module)

    if module.params['list_access_points']:
        module.exit_json(access_points=aws_response_list_parser(paginate, it, 'AccessPointList'))
    elif module.params['list_access_points_for_object_lambda']:
        module.exit_json(access_points_for_object_lambda=aws_response_list_parser(paginate, it, 'ObjectLambdaAccessPointList'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'Jobs'))
    elif module.params['list_regional_buckets']:
        module.exit_json(regional_buckets=aws_response_list_parser(paginate, it, 'RegionalBucketList'))
    elif module.params['list_storage_lens_configurations']:
        module.exit_json(storage_lens_configurations=aws_response_list_parser(paginate, it, 'StorageLensConfigurationList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
