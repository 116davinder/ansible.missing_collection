#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_devops_guru_info
short_description: Get Information about AWS Device Guru.
description:
  - Get Information about AWS Device Guru.
  - U(https://docs.aws.amazon.com/devops-guru/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  id:
    description:
      - can be id of anomaly?
      - can be id of insight?
    required: false
    type: str
  from_time:
    description:
      - filter to results based on from time?
      - format example - '2021-12-01' or 'YYYY-MM-DD'
    required: false
    type: str
  resource_collection_type:
    description:
      - type of resource collection.
    required: false
    type: str
    default: 'AWS_CLOUD_FORMATION'
  describe_account_overview:
    description:
      - do you want to describe account overview for given I(from_time)?
    required: false
    type: bool
  describe_anomaly:
    description:
      - do you want to describe anomaly for given I(id)?
    required: false
    type: bool
  describe_insight:
    description:
      - do you want to describe insight for given I(id)?
    required: false
    type: bool
  describe_resource_collection_health:
    description:
      - do you want to describe resource collection health for given I(resource_collection_type)?
    required: false
    type: bool
  describe_service_integration:
    description:
      - do you want to describe service integration?
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
- name: "get health"
  aws_devops_guru_info:

- name: "account overview"
  aws_devops_guru_info:
    describe_account_overview: true
    from_time: '2020-12-31'

- name: "describe anomaly"
  aws_devops_guru_info:
    describe_anomaly: true
    id: 'test'

- name: "describe insight"
  aws_devops_guru_info:
    describe_insight: true
    id: 'test'

- name: "describe resource collection health"
  aws_devops_guru_info:
    describe_resource_collection_health: true
    resource_collection_type: 'AWS_CLOUD_FORMATION'

- name: "describe service integration"
  aws_devops_guru_info:
    describe_service_integration: true
"""

RETURN = """
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from datetime import datetime


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


def _convert_str_to_datetime(time: str):
    try:
        return datetime.strptime(time, '%Y-%m-%d')
    except ValueError:
        return None


def _devops_guru(client, module):
    try:
        if module.params['describe_account_overview']:
            return client.describe_account_overview(
                FromTime=_convert_str_to_datetime(module.params['from_time'])
            ), False
        elif module.params['describe_anomaly']:
            return client.describe_anomaly(
                Id=module.params['id']
            ), False
        elif module.params['describe_insight']:
            return client.describe_insight(
                Id=module.params['id']
            ), False
        elif module.params['describe_resource_collection_health']:
            if client.can_paginate('describe_resource_collection_health'):
                paginator = client.get_paginator('describe_resource_collection_health')
                return paginator.paginate(
                    ResourceCollectionType=module.params['resource_collection_type']
                ), True
            else:
                return client.describe_resource_collection_health(
                    ResourceCollectionType=module.params['resource_collection_type']
                ), False
        elif module.params['describe_service_integration']:
            return client.describe_service_integration(), False
        else:
            return client.describe_account_health(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Device Guru details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        from_time=dict(required=False),
        resource_collection_type=dict(required=False, default='AWS_CLOUD_FORMATION'),
        describe_account_overview=dict(required=False, type=bool),
        describe_anomaly=dict(required=False, type=bool),
        describe_insight=dict(required=False, type=bool),
        describe_resource_collection_health=dict(required=False, type=bool),
        describe_service_integration=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_account_overview', True, ['from_time']),
            ('describe_anomaly', True, ['id']),
            ('describe_insight', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_account_overview',
                'describe_anomaly',
                'describe_insight',
                'describe_resource_collection_health',
                'describe_service_integration',
            )
        ],
    )

    client = module.client('devops-guru', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _devops_guru(client, module)

    if module.params['describe_account_overview']:
        module.exit_json(overview=camel_dict_to_snake_dict(it))
    elif module.params['describe_anomaly']:
        module.exit_json(anomaly=camel_dict_to_snake_dict(it))
    elif module.params['describe_insight']:
        module.exit_json(insight=camel_dict_to_snake_dict(it))
    elif module.params['describe_resource_collection_health']:
        module.exit_json(cloud_formation=aws_response_list_parser(paginate, it, 'CloudFormation'))
    elif module.params['describe_service_integration']:
        module.exit_json(service_integration=camel_dict_to_snake_dict(it['ServiceIntegration']))
    else:
        module.exit_json(health=camel_dict_to_snake_dict(it))


if __name__ == '__main__':
    main()
