#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_machinelearning_info
short_description: Get Information about Amazon Machine Learning.
description:
  - Get Information about Amazon Machine Learning.
  - U(https://docs.aws.amazon.com/lookout-for-vision/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  filter_variable_prediction:
    description:
      - variable key to filter predictions.
    required: false
    type: str
    choices: ['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
  filter_variable_datasource:
    description:
      - variable key to filter datasource.
    required: false
    type: str
    choices: ['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'DataLocationS3', 'IAMUser']
  filter_variable_evaluation:
    description:
      - variable key to filter evaluation.
    required: false
    type: str
    choices: ['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
  filter_variable_ml_models:
    description:
      - variable key to filter predictions.
    required: false
    type: str
    choices: ['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
  eq:
    description:
      - variable value equals to?
    required: false
    type: str
  describe_batch_predictions:
    description:
      - do you want to get list of batch_predictions for given I(filter_variable_prediction) and I(eq)?
    required: false
    type: bool
  describe_data_sources:
    description:
      - do you want to get list of data_sources for given I(filter_variable_datasource) and given I(eq)?
    required: false
    type: bool
  describe_evaluations:
    description:
      - do you want to get list of evaluations for given I(filter_variable_evaluation) and I(eq)?
    required: false
    type: bool
  describe_ml_models:
    description:
      - do you want to get list of evaluations for given I(filter_variable_ml_models) and I(eq)?
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
- name: "get list of batch_predictions"
  aws_machinelearning_info:
    describe_batch_predictions: true
    filter_variable_prediction: 'Status'
    eq: 'COMPLETED'

- name: "get list of data_sources"
  aws_machinelearning_info:
    describe_data_sources: true
    filter_variable_prediction: 'Status'
    eq: 'COMPLETED'

- name: "get list of evaluations"
  aws_machinelearning_info:
    describe_evaluations: true
    filter_variable_prediction: 'Status'
    eq: 'COMPLETED'

- name: "get list of ml_models"
  aws_machinelearning_info:
    describe_ml_models: true
    filter_variable_prediction: 'Status'
    eq: 'COMPLETED'
"""

RETURN = """
batch_predictions:
  description: list of batch_predictions.
  returned: when `describe_batch_predictions` is defined and success.
  type: list
data_sources:
  description: list of data_sources.
  returned: when `describe_data_sources` is defined and success.
  type: list
evaluations:
  description: list of evaluations.
  returned: when `describe_evaluations` is defined and success.
  type: list
ml_models:
  description: list of ml_models.
  returned: when `describe_ml_models` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _machinelearning(client, module):
    try:
        if module.params['describe_batch_predictions']:
            if client.can_paginate('describe_batch_predictions'):
                paginator = client.get_paginator('describe_batch_predictions')
                return paginator.paginate(
                    FilterVariable=module.params['filter_variable_prediction'],
                    EQ=module.params['eq']
                ), True
            else:
                return client.describe_batch_predictions(
                    FilterVariable=module.params['filter_variable_prediction'],
                    EQ=module.params['eq']
                ), False
        elif module.params['describe_data_sources']:
            if client.can_paginate('describe_data_sources'):
                paginator = client.get_paginator('describe_data_sources')
                return paginator.paginate(
                    FilterVariable=module.params['filter_variable_datasource'],
                    EQ=module.params['eq']
                ), True
            else:
                return client.describe_data_sources(
                    FilterVariable=module.params['filter_variable_datasource'],
                    EQ=module.params['eq']
                ), False
        elif module.params['describe_evaluations']:
            if client.can_paginate('describe_evaluations'):
                paginator = client.get_paginator('describe_evaluations')
                return paginator.paginate(
                    FilterVariable=module.params['filter_variable_evaluation'],
                    EQ=module.params['eq']
                ), True
            else:
                return client.describe_evaluations(
                    FilterVariable=module.params['filter_variable_evaluation'],
                    EQ=module.params['eq']
                ), False
        elif module.params['describe_ml_models']:
            if client.can_paginate('describe_ml_models'):
                paginator = client.get_paginator('describe_ml_models')
                return paginator.paginate(
                    FilterVariable=module.params['filter_variable_ml_models'],
                    EQ=module.params['eq']
                ), True
            else:
                return client.describe_ml_models(
                    FilterVariable=module.params['filter_variable_ml_models'],
                    EQ=module.params['eq']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Machine Learning details')


def main():
    argument_spec = dict(
        filter_variable_prediction=dict(
            required=False,
            choices=['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
        ),
        filter_variable_datasource=dict(
            required=False,
            choices=['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'DataLocationS3', 'IAMUser']
        ),
        filter_variable_evaluation=dict(
            required=False,
            choices=['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
        ),
        filter_variable_ml_models=dict(
            required=False,
            choices=['CreatedAt', 'LastUpdatedAt', 'Status', 'Name', 'IAMUser', 'MLModelId', 'DataSourceId', 'DataURI']
        ),
        eq=dict(required=False),
        describe_batch_predictions=dict(required=False, type=bool),
        describe_data_sources=dict(required=False, type=bool),
        describe_evaluations=dict(required=False, type=bool),
        describe_ml_models=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_batch_predictions', True, ['filter_variable_prediction', 'eq']),
            ('describe_data_sources', True, ['filter_variable_datasource', 'eq']),
            ('describe_evaluations', True, ['filter_variable_evaluation', 'eq']),
            ('describe_ml_models', True, ['filter_variable_ml_models', 'eq']),
        ),
        mutually_exclusive=[
            (
                'describe_batch_predictions',
                'describe_data_sources',
                'describe_evaluations',
                'describe_ml_models',
            )
        ],
    )

    client = module.client('machinelearning', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _machinelearning(client, module)

    if module.params['describe_batch_predictions']:
        module.exit_json(batch_predictions=aws_response_list_parser(paginate, it, 'Results'))
    elif module.params['describe_data_sources']:
        module.exit_json(data_sources=aws_response_list_parser(paginate, it, 'Results'))
    elif module.params['describe_evaluations']:
        module.exit_json(evaluations=aws_response_list_parser(paginate, it, 'Results'))
    elif module.params['describe_ml_models']:
        module.exit_json(ml_models=aws_response_list_parser(paginate, it, 'Results'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
