#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_databrew_info
short_description: Get Information about AWS Glue DataBrew.
description:
  - Get Information about AWS Glue DataBrew.
  - U(https://docs.aws.amazon.com/databrew/latest/dg/API_Operations.html)
version_added: 0.0.5
options:
  project_name:
    description:
      -  The name of a project.
    required: false
    type: str
  dataset_name:
    description:
      - The name of the dataset.
    required: false
    type: str
  job_name:
    description:
      - The name of the job.
    required: false
    type: str
  list_datasets:
    description:
      - do you want to get list of dataset?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs of given I(dataset_name) and I(project_name)?
    required: false
    type: bool
  list_job_runs:
    description:
      - do you want to get list of job runs of given I(job_name)?
    required: false
    type: bool
  list_recipes:
    description:
      - do you want to get list of recipes?
    required: false
    type: bool
  list_schedules:
    description:
      - do you want to get list of schedules of given I(job_name)?
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
- name: "Lists all of the DataBrew projects"
  aws_databrew_info:

- name: "Lists all of the AWS Glue DataBrew datasets"
  aws_databrew_info:
    list_datasets: true

- name: "Lists the AWS Glue DataBrew jobs"
  aws_databrew_info:
    list_jobs: true
    dataset_name: 'test'
    project_name: 'test'

- name: "Lists all of the previous runs of a particular AWS Glue DataBrew job"
  aws_databrew_info:
    list_job_runs: true
    job_name: 'test'

- name: "Lists all of the AWS Glue DataBrew recipes"
  aws_databrew_info:
    list_recipes: true

- name: "Lists the AWS Glue DataBrew schedules"
  aws_databrew_info:
    job_name: 'test'
    list_schedules: true
"""

RETURN = """
projects:
  description: Lists all of the DataBrew projects in the current AWS account.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'create_date': datetime(2016, 6, 6),
        'created_by': 'string',
        'dataset_name': 'string',
        'last_modified_date': datetime(2017, 7, 7),
        'last_modified_by': 'string',
        'name': 'string',
        'recipe_name': 'string',
        'resource_arn': 'string',
        'sample': {},
        'tags': {},
        'role_arn': 'string',
        'opened_by': 'string',
        'open_date': datetime(2015, 1, 1)
    },
  ]
datasets:
  description: Lists all of the AWS Glue DataBrew datasets for the current AWS account.
  returned: when `list_datasets` is defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'create_date': datetime(2016, 6, 6),
        'created_by': 'string',
        'name': 'string',
        'format_options': {},
        'input': {},
        'last_modified_date': datetime(2017, 7, 7),
        'last_modified_by': 'string',
        'source': 'S3',
        'tags': {},
        'ResourceArn': 'string'
    },
  ]
jobs:
  description: Lists the AWS Glue DataBrew jobs in the current AWS account.
  returned: when `list_jobs`, `dataset_name`, and `project_name` are defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'create_date': datetime(2016, 6, 6),
        'created_by': 'string',
        'dataset_name': 'string',
        'encryption_key_arn': 'string',
        'encryption_mode': 'SSE-KMS',
        'name': 'string',
        'type': 'PROFILE',
        'last_modified_date': datetime(2017, 7, 7),
        'last_modified_by': 'string',
        'log_subscription': 'ENABLE',
        'max_capacity': 123,
        'max_retries': 123,
        'outputs': [],
        'project_name': 'string',
        'recipe_reference': {},
        'resource_arn': 'string',
        'role_arn': 'string',
        'timeout': 123,
        'tags': {},
    },
  ]
job_runs:
  description: Lists all of the previous runs of a particular AWS Glue DataBrew job in the current AWS account.
  returned: when `list_job_runs` and `job_name` are defined and success
  type: list
  sample: [
    {
        'attempt': 123,
        'completed_on': datetime(2016, 6, 6),
        'dataset_name': 'string',
        'error_message': 'string',
        'execution_time': 123,
        'job_name': 'string',
        'run_id': 'string',
        'state': 'STARTING',
        'log_subscription': 'ENABLE',
        'log_group_name': 'string',
        'outputs': [],
        'recipe_reference': {},
        'started_by': 'string',
        'started_nn': datetime(2015, 1, 1)
    },
  ]
recipes:
  description: Lists all of the AWS Glue DataBrew recipes in the current AWS account.
  returned: when `list_recipes` is defined and success
  type: list
  sample: [
    {
        'create_date': datetime(2016, 6, 6),
        'created_by': 'string',
        'last_modified_date': datetime(2017, 7, 7),
        'last_modified_by': 'string',
        'project_name': 'string',
        'published_by': 'string',
        'published_date': datetime(2015, 1, 1),
        'description': 'string',
        'name': 'string',
        'resource_arn': 'string',
        'steps': [],
        'tags': {},
        'recipe_version': 'string'
    },
  ]
schedules:
  description: Lists the AWS Glue DataBrew schedules in the current AWS account.
  returned: when `list_schedules`, and `job_name` are defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'create_date': datetime(2016, 6, 6),
        'created_by': 'string',
        'job_names': [],
        'last_modified_date': datetime(2017, 7, 7),
        'last_modified_by': 'string',
        'resource_arn': 'string',
        'cron_expression': 'string',
        'tags': {},
        'name': 'string'
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _databrew(client, module):
    try:
        if module.params['list_datasets']:
            if client.can_paginate('list_datasets'):
                paginator = client.get_paginator('list_datasets')
                return paginator.paginate(), True
            else:
                return client.list_datasets(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    DatasetName=module.params['dataset_name'],
                    ProjectName=module.params['project_name'],
                ), True
            else:
                return client.list_jobs(
                    DatasetName=module.params['dataset_name'],
                    ProjectName=module.params['project_name'],
                ), False
        elif module.params['list_job_runs']:
            if client.can_paginate('list_job_runs'):
                paginator = client.get_paginator('list_job_runs')
                return paginator.paginate(
                    Name=module.params['job_name'],
                ), True
            else:
                return client.list_job_runs(
                    Name=module.params['job_name'],
                ), False
        elif module.params['list_recipes']:
            if client.can_paginate('list_recipes'):
                paginator = client.get_paginator('list_recipes')
                return paginator.paginate(), True
            else:
                return client.list_recipes(), False
        elif module.params['list_schedules']:
            if client.can_paginate('list_schedules'):
                paginator = client.get_paginator('list_schedules')
                return paginator.paginate(
                    JobName=module.params['job_name'],
                ), True
            else:
                return client.list_schedules(
                    JobName=module.params['job_name'],
                ), False
        else:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(), True
            else:
                return client.list_projects(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws glue databrew details')


def main():
    argument_spec = dict(
        project_name=dict(required=False),
        dataset_name=dict(required=False),
        job_name=dict(required=False),
        list_datasets=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
        list_job_runs=dict(required=False, type=bool),
        list_recipes=dict(required=False, type=bool),
        list_schedules=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_jobs', True, ['project_name', 'dataset_name']),
            ('list_job_runs', True, ['job_name']),
            ('list_schedules', True, ['job_name']),
        ),
        mutually_exclusive=[
            (
                'list_datasets',
                'list_jobs',
                'list_job_runs',
                'list_recipes',
                'list_schedules',
            )
        ],
    )

    client = module.client('databrew', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _databrew(client, module)

    if module.params['list_datasets']:
        module.exit_json(datasets=aws_response_list_parser(paginate, _it, 'Datasets'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, _it, 'Jobs'))
    elif module.params['list_job_runs']:
        module.exit_json(job_runs=aws_response_list_parser(paginate, _it, 'JobRuns'))
    elif module.params['list_recipes']:
        module.exit_json(recipes=aws_response_list_parser(paginate, _it, 'Recipes'))
    elif module.params['list_schedules']:
        module.exit_json(schedules=aws_response_list_parser(paginate, _it, 'Schedules'))
    else:
        module.exit_json(projects=aws_response_list_parser(paginate, _it, 'Projects'))


if __name__ == '__main__':
    main()
