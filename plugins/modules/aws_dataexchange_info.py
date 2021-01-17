#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dataexchange_info
short_description: Get Information about AWS Data Exchange.
description:
  - Get Information about AWS Data Exchange.
  - U(https://docs.aws.amazon.com/data-exchange/latest/apireference/operations.html)
version_added: 0.0.5
options:
  data_set_id:
    description:
      -  id of the dataset.
    required: false
    type: str
  list_data_sets:
    description:
      - do you want to get list of datasets?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs of given I(data_set_id)?
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
- name: "Lists all of the dataexchange datasets"
  aws_dataexchange_info:
    list_datasets: true

- name: "Lists the dataexchange jobs"
  aws_dataexchange_info:
    list_jobs: true
    data_set_id: 'test'
"""

RETURN = """
datasets:
  description: Lists all of the dataexchange datasets for the current AWS account.
  returned: when `list_data_sets` is defined and success
  type: list
  sample: [
    {
        'arn': 'string',
        'asset_type': 'S3_SNAPSHOT',
        'created_at': datetime(2016, 6, 6),
        'description': 'string',
        'id': 'string',
        'name': 'string',
        'origin': 'OWNED',
        'origin_details': {
            'product_id': 'string'
        },
        'source_id': 'string',
        'updated_at': datetime(2015, 1, 1)
    },
  ]
jobs:
  description: Lists the dataexchange jobs in the current AWS account.
  returned: when `list_jobs`, and `data_set_id` are defined and success
  type: list
  sample: [
    {
        'arn': 'string',
        'created_at': datetime(2015, 1, 1),
        'details': {
            'export_asset_to_signed_url': {},
            'export_assets_to_s3': {},
            'import_asset_from_signed_url': {},
            'import_assets_from_s3': {}
        },
        'errors': [],
        'id': 'string',
        'state': 'WAITING',
        'type': 'IMPORT_ASSETS_FROM_S3',
        'updated_at': datetime(2015, 1, 1)
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


def _dataexchange(client, module):
    try:
        if module.params['list_data_sets']:
            if client.can_paginate('list_data_sets'):
                paginator = client.get_paginator('list_data_sets')
                return paginator.paginate(), True
            else:
                return client.list_data_sets(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    DataSetId=module.params['data_set_id'],
                ), True
            else:
                return client.list_jobs(
                    DataSetId=module.params['data_set_id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Data Exchange details')


def main():
    argument_spec = dict(
        data_set_id=dict(required=False),
        list_data_sets=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_jobs', True, ['data_set_id']),
        ),
        mutually_exclusive=[
            (
                'list_data_sets',
                'list_jobs',
            )
        ],
    )

    client = module.client('dataexchange', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _dataexchange(client, module)

    if module.params['list_data_sets']:
        module.exit_json(datasets=aws_response_list_parser(paginate, _it, 'DataSets'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, _it, 'Jobs'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
