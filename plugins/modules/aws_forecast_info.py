#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_forecast_info
short_description: Get Information about Amazon Forecast Service.
description:
  - Get Information about Amazon Forecast Service.
  - U(https://docs.aws.amazon.com/forecast/latest/dg/API_Operations_Amazon_Forecast_Service.html)
version_added: 0.0.6
options:
  list_dataset_groups:
    description:
      - do you want to get list of dataset groups?
    required: false
    type: bool
  list_dataset_import_jobs:
    description:
      - do you want to get list of dataset import jobs?
    required: false
    type: bool
  list_datasets:
    description:
      - do you want to get list of datasets?
    required: false
    type: bool
  list_forecast_export_jobs:
    description:
      - do you want to get list of forecast export jobs?
    required: false
    type: bool
  list_predictor_backtest_export_jobs:
    description:
      - do you want to get list of predictor backtest export jobs?
    required: false
    type: bool
  list_predictors:
    description:
      - do you want to get list of predictors?
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
- name: "get list of forecasts"
  aws_forecast_info:

- name: "get list of dataset groups"
  aws_forecast_info:
    list_dataset_groups: true

- name: "get list of dataset import jobs"
  aws_forecast_info:
    list_dataset_import_jobs: true

- name: "get list of datasets"
  aws_forecast_info:
    list_datasets: true

- name: "get list of forecast export jobs"
  aws_forecast_info:
    list_forecast_export_jobs: true

- name: "get list of predictor backtest export jobs"
  aws_forecast_info:
    list_predictor_backtest_export_jobs: true

- name: "get list of predictors"
  aws_forecast_info:
    list_predictors: true
"""

RETURN = """
dataset_groups:
  description: list of dataset groups.
  returned: when `list_dataset_groups` is defined and success
  type: list
dataset_import_jobs:
  description: list of dataset import jobs.
  returned: when `list_dataset_import_jobs` is defined and success
  type: list
datasets:
  description: list of datasets.
  returned: when `list_datasets` is defined and success
  type: list
forecast_export_jobs:
  description: list of forecast export jobs.
  returned: when `list_forecast_export_jobs` is defined and success
  type: list
predictor_backtest_export_jobs:
  description: list of predictor backtest export jobs.
  returned: when `list_predictor_backtest_export_jobs` is defined and success
  type: list
predictors:
  description: list of predictors.
  returned: when `list_predictors` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _forecast(client, module):
    try:
        if module.params['list_dataset_groups']:
            if client.can_paginate('list_dataset_groups'):
                paginator = client.get_paginator('list_dataset_groups')
                return paginator.paginate(), True
            else:
                return client.list_dataset_groups(), False
        elif module.params['list_dataset_import_jobs']:
            if client.can_paginate('list_dataset_import_jobs'):
                paginator = client.get_paginator('list_dataset_import_jobs')
                return paginator.paginate(), True
            else:
                return client.list_dataset_import_jobs(), False
        elif module.params['list_datasets']:
            if client.can_paginate('list_datasets'):
                paginator = client.get_paginator('list_datasets')
                return paginator.paginate(), True
            else:
                return client.list_datasets(), False
        elif module.params['list_forecast_export_jobs']:
            if client.can_paginate('list_forecast_export_jobs'):
                paginator = client.get_paginator('list_forecast_export_jobs')
                return paginator.paginate(), True
            else:
                return client.list_forecast_export_jobs(), False
        elif module.params['list_predictor_backtest_export_jobs']:
            if client.can_paginate('list_predictor_backtest_export_jobs'):
                paginator = client.get_paginator('list_predictor_backtest_export_jobs')
                return paginator.paginate(), True
            else:
                return client.list_predictor_backtest_export_jobs(), False
        elif module.params['list_predictors']:
            if client.can_paginate('list_predictors'):
                paginator = client.get_paginator('list_predictors')
                return paginator.paginate(), True
            else:
                return client.list_predictors(), False
        else:
            if client.can_paginate('list_forecasts'):
                paginator = client.get_paginator('list_forecasts')
                return paginator.paginate(), True
            else:
                return client.list_forecasts(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon forecast details')


def main():
    argument_spec = dict(
        list_dataset_groups=dict(required=False, type=bool),
        list_dataset_import_jobs=dict(required=False, type=bool),
        list_datasets=dict(required=False, type=bool),
        list_forecast_export_jobs=dict(required=False, type=bool),
        list_predictor_backtest_export_jobs=dict(required=False, type=bool),
        list_predictors=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_dataset_groups',
                'list_dataset_import_jobs',
                'list_datasets',
                'list_forecast_export_jobs',
                'list_predictor_backtest_export_jobs',
                'list_predictors',
            )
        ],
    )

    client = module.client('forecast', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _forecast(client, module)

    if module.params['list_dataset_groups']:
        module.exit_json(dataset_groups=aws_response_list_parser(paginate, it, 'DatasetGroups'))
    elif module.params['list_dataset_import_jobs']:
        module.exit_json(dataset_import_jobs=aws_response_list_parser(paginate, it, 'DatasetImportJobs'))
    elif module.params['list_datasets']:
        module.exit_json(datasets=aws_response_list_parser(paginate, it, 'Datasets'))
    elif module.params['list_forecast_export_jobs']:
        module.exit_json(forecast_export_jobs=aws_response_list_parser(paginate, it, 'ForecastExportJobs'))
    elif module.params['list_predictor_backtest_export_jobs']:
        module.exit_json(predictor_backtest_export_jobs=aws_response_list_parser(paginate, it, 'PredictorBacktestExportJobs'))
    elif module.params['list_predictors']:
        module.exit_json(predictors=aws_response_list_parser(paginate, it, 'Predictors'))
    else:
        module.exit_json(forecasts=aws_response_list_parser(paginate, it, 'Forecasts'))


if __name__ == '__main__':
    main()
