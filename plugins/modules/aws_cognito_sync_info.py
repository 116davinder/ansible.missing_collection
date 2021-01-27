#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cognito_sync_info
short_description: Get Information about Amazon Cognito Sync.
description:
  - Get Information about Amazon Cognito Sync.
  - U(https://docs.aws.amazon.com/cognitosync/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  identity_pool_id:
    description:
      - id of cognito identity pool.
    required: false
    type: str
  identity_id:
    description:
      - id of cognito identity.
    required: false
    type: str
  dataset_name:
    description:
      - name of the cognito dataset.
    required: false
    type: str
  list_datasets:
    description:
      - do you want to get list of cognito datasets?
    required: false
    type: bool
  list_identity_pool_usage:
    description:
      - do you want to get list of usage of cognito pools?
    required: false
    type: bool
  list_records:
    description:
      - do you want to get list of cognito dataset records?
    required: false
    type: bool
  describe_dataset:
    description:
      - do you want to get details about cognito dataset I(dataset_name)?
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
- name: "get list of cognito datasets"
  aws_cognito_sync_info:
    list_datasets: true
    identity_pool_id: 'test-pool-id'
    identity_id: 'test-id'

- name: "get list of cognito pool usage"
  aws_cognito_sync_info:
    list_identity_pool_usage: true

- name: "get list of cognito dataset records"
  aws_cognito_sync_info:
    list_records: true
    identity_pool_id: 'test-pool-id'
    identity_id: 'test-id'
    dataset_name: 'test-dataset'

- name: "get details about cognito dataset"
  aws_cognito_sync_info:
    describe_dataset: true
    identity_pool_id: 'test-pool-id'
    identity_id: 'test-id'
    dataset_name: 'test-dataset'
"""

RETURN = """
datasets:
  description: get list of cognito datasets.
  returned: when `list_datasets`, `identity_pool_id` , and `identity_id` are defined and success
  type: list
  sample: [
    {
        'identity_id': 'string',
        'dataset_name': 'string',
        'creation_date': datetime(2016, 6, 6),
        'last_modified_date': datetime(2015, 1, 1),
        'last_modified_by': 'string',
        'data_storage': 123,
        'num_records': 123
    },
  ]
identity_pool_usages:
  description: get list of usage for identity pools.
  returned: when `list_identity_pool_usage` is defined and success
  type: list
  sample: [
    {
        'identity_pool_id': 'string',
        'sync_sessions_count': 123,
        'data_storage': 123,
        'last_modified_date': datetime(2015, 1, 1)
    },
  ]
records:
  description: get details about notification rule.
  returned: when `list_records`, `identity_pool_id` , `dataset_name`, and `identity_id` are defined and success
  type: list
  sample: [
    {
        'key': 'string',
        'value': 'string',
        'sync_count': 123,
        'last_modified_date': datetime(2015, 1, 1),
        'last_modified_by': 'string',
        'device_last_modified_date': datetime(2016, 6, 6)
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _cognito(client, module):
    try:
        if module.params['list_datasets']:
            if client.can_paginate('list_datasets'):
                paginator = client.get_paginator('list_datasets')
                return paginator.paginate(
                    IdentityPoolId=module.params['identity_pool_id'],
                    IdentityId=module.params['identity_id'],
                ), True
            else:
                return client.list_datasets(
                    IdentityPoolId=module.params['identity_pool_id'],
                    IdentityId=module.params['identity_id'],
                ), False
        elif module.params['list_identity_pool_usage']:
            if client.can_paginate('list_identity_pool_usage'):
                paginator = client.get_paginator('list_identity_pool_usage')
                return paginator.paginate(), True
            else:
                return client.list_identity_pool_usage(), False
        elif module.params['list_records']:
            if client.can_paginate('list_records'):
                paginator = client.get_paginator('list_records')
                return paginator.paginate(
                    IdentityPoolId=module.params['identity_pool_id'],
                    IdentityId=module.params['identity_id'],
                    DatasetName=module.params['dataset_name'],
                ), True
            else:
                return client.list_records(
                    IdentityPoolId=module.params['identity_pool_id'],
                    IdentityId=module.params['identity_id'],
                    DatasetName=module.params['dataset_name'],
                ), False
        elif module.params['describe_dataset']:
            return client.describe_dataset(
                IdentityPoolId=module.params['identity_pool_id'],
                IdentityId=module.params['identity_id'],
                DatasetName=module.params['dataset_name'],
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cognito sync details')


def main():
    argument_spec = dict(
        identity_pool_id=dict(required=False),
        identity_id=dict(required=False),
        dataset_name=dict(required=False),
        list_datasets=dict(required=False, type=bool),
        list_identity_pool_usage=dict(required=False, type=bool),
        list_records=dict(required=False, type=bool),
        describe_dataset=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_datasets', True, ['identity_pool_id', 'identity_id']),
            ('list_records', True, ['identity_pool_id', 'identity_id', 'dataset_name']),
            ('describe_dataset', True, ['identity_pool_id', 'identity_id', 'dataset_name']),
        ),
        mutually_exclusive=[
            (
                'list_datasets',
                'list_identity_pool_usage',
                'list_records',
                'describe_dataset',
            )
        ],
    )

    client = module.client('cognito-sync', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cognito(client, module)

    if module.params['list_datasets']:
        module.exit_json(datasets=aws_response_list_parser(paginate, _it, 'Datasets'))
    elif module.params['list_identity_pool_usage']:
        module.exit_json(identity_pool_usages=aws_response_list_parser(paginate, _it, 'IdentityPoolUsages'))
    elif module.params['list_records']:
        module.exit_json(records=aws_response_list_parser(paginate, _it, 'Records'))
    elif module.params['describe_dataset']:
        module.exit_json(dataset=camel_dict_to_snake_dict(_it['Dataset']))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
