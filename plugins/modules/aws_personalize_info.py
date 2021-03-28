#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_personalize_info
short_description: Get Information about Amazon Personalize.
description:
  - Get Information about Amazon Personalize.
  - U(https://docs.aws.amazon.com/personalize/latest/apiref/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - can be arn of solution version?
      - can be arn of dataset?
      - can be arn of solution?
      - can be arn of dataset group?
    required: false
    type: str
    aliases: ['solution_version_arn', 'solution_arn', 'dataset_arn', 'dataset_group_arn']
  list_batch_inference_jobs:
    description:
      - do you want to get list of batch_inference_jobs for given solution version I(arn)?
    required: false
    type: bool
  list_campaigns:
    description:
      - do you want to get campaigns for given solution I(arn)?
    required: false
    type: bool
  list_dataset_groups:
    description:
      - do you want to get list of dataset_groups?
    required: false
    type: bool
  list_dataset_import_jobs:
    description:
      - do you want to get dataset_import_jobs for given dataset I(arn)?
    required: false
    type: bool
  list_datasets:
    description:
      - do you want to get datasets for given dataset_group I(arn)?
    required: false
    type: bool
  list_solutions:
    description:
      - do you want to get solutions for given dataset_group I(arn)?
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
- name: "get list of batch_inference_jobs"
  aws_personalize_info:
    list_batch_inference_jobs: true
    arn: 'solution-version-arn'

- name: "get campaigns"
  aws_personalize_info:
    list_campaigns: true
    arn: 'solution-arn'

- name: "get list of dataset_groups"
  aws_personalize_info:
    list_dataset_groups: true

- name: "get dataset_import_jobs"
  aws_personalize_info:
    list_dataset_import_jobs: true
    arn: 'dataset_arn'

- name: "get datasets"
  aws_personalize_info:
    list_datasets: true
    arn: 'dataset_group_arn'

- name: "get solutions"
  aws_personalize_info:
    list_solutions: true
    arn: 'dataset_group_arn'
"""

RETURN = """
batch_inference_jobs:
  description: list of batch_inference_jobs.
  returned: when `list_batch_inference_jobs` is defined and success.
  type: list
campaigns:
  description: get of campaigns.
  returned: when `list_campaigns` is defined and success.
  type: list
dataset_groups:
  description: list of dataset_groups.
  returned: when `list_dataset_groups` is defined and success.
  type: list
dataset_import_jobs:
  description: list of dataset_import_jobs.
  returned: when `list_dataset_import_jobs` is defined and success.
  type: list
datasets:
  description: list of datasets.
  returned: when `list_datasets` is defined and success.
  type: list
solutions:
  description: list of solutions.
  returned: when `list_solutions` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _personalize(client, module):
    try:
        if module.params['list_batch_inference_jobs']:
            if client.can_paginate('list_batch_inference_jobs'):
                paginator = client.get_paginator('list_batch_inference_jobs')
                return paginator.paginate(
                    solutionVersionArn=module.params['arn']
                ), True
            else:
                return client.list_batch_inference_jobs(
                    solutionVersionArn=module.params['arn']
                ), False
        elif module.params['list_campaigns']:
            if client.can_paginate('list_campaigns'):
                paginator = client.get_paginator('list_campaigns')
                return paginator.paginate(
                    solutionArn=module.params['arn']
                ), True
            else:
                return client.list_campaigns(
                    solutionArn=module.params['arn']
                ), False
        elif module.params['list_dataset_groups']:
            if client.can_paginate('list_dataset_groups'):
                paginator = client.get_paginator('list_dataset_groups')
                return paginator.paginate(), True
            else:
                return client.list_dataset_groups(), False
        elif module.params['list_dataset_import_jobs']:
            if client.can_paginate('list_dataset_import_jobs'):
                paginator = client.get_paginator('list_dataset_import_jobs')
                return paginator.paginate(
                    datasetArn=module.params['arn']
                ), True
            else:
                return client.list_dataset_import_jobs(
                    datasetArn=module.params['arn']
                ), False
        elif module.params['list_datasets']:
            if client.can_paginate('list_datasets'):
                paginator = client.get_paginator('list_datasets')
                return paginator.paginate(
                    datasetGroupArn=module.params['arn']
                ), True
            else:
                return client.list_datasets(
                    datasetGroupArn=module.params['arn']
                ), False
        elif module.params['list_solutions']:
            if client.can_paginate('list_solutions'):
                paginator = client.get_paginator('list_solutions')
                return paginator.paginate(
                    datasetGroupArn=module.params['arn']
                ), True
            else:
                return client.list_solutions(
                    datasetGroupArn=module.params['arn']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Personalize details')


def main():
    argument_spec = dict(
        arn=dict(
            required=False,
            aliases=['solution_version_arn', 'solution_arn', 'dataset_arn', 'dataset_group_arn']
        ),
        list_batch_inference_jobs=dict(required=False, type=bool),
        list_campaigns=dict(required=False, type=bool),
        list_dataset_groups=dict(required=False, type=bool),
        list_dataset_import_jobs=dict(required=False, type=bool),
        list_datasets=dict(required=False, type=bool),
        list_solutions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_batch_inference_jobs', True, ['arn']),
            ('list_campaigns', True, ['arn']),
            ('list_dataset_import_jobs', True, ['arn']),
            ('list_datasets', True, ['arn']),
            ('list_solutions', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_batch_inference_jobs',
                'list_campaigns',
                'list_dataset_groups',
                'list_dataset_import_jobs',
                'list_datasets',
                'list_solutions',
            )
        ],
    )

    client = module.client('personalize', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _personalize(client, module)

    if module.params['list_batch_inference_jobs']:
        module.exit_json(batch_inference_jobs=aws_response_list_parser(paginate, it, 'batchInferenceJobs'))
    elif module.params['list_campaigns']:
        module.exit_json(campaigns=aws_response_list_parser(paginate, it, 'campaigns'))
    elif module.params['list_dataset_groups']:
        module.exit_json(dataset_groups=aws_response_list_parser(paginate, it, 'datasetGroups'))
    elif module.params['list_dataset_import_jobs']:
        module.exit_json(dataset_import_jobs=aws_response_list_parser(paginate, it, 'datasetImportJobs'))
    elif module.params['list_datasets']:
        module.exit_json(datasets=aws_response_list_parser(paginate, it, 'datasets'))
    elif module.params['list_solutions']:
        module.exit_json(solutions=aws_response_list_parser(paginate, it, 'solutions'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
