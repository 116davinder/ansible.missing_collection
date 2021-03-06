#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_batch_info
short_description: Get details about AWS Batch.
description:
  - Get Information about AWS Batch.
  - U(https://docs.aws.amazon.com/batch/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  job_queue:
    description:
      - name of batch queue.
      - arn of batch queue.
    required: false
    type: str
    aliases: ['job_queue_arn']
  job_queues:
    description:
      - list of names of batch queue.
      - list of arn of batch queue.
    required: false
    type: list
    default: []
    aliases: ['job_queue_arns']
  job_ids:
    description:
      - list of job ids.
    required: false
    type: list
  job_definition_arns:
    description:
      - list of names of batch job definitions.
      - list of arns of batch job definitions.
    required: false
    type: list
    aliases: ['job_definition_names']
  job_definition_status:
    description:
      - job definition status to filter.
    required: false
    type: str
    default: 'ACTIVE'
  job_status:
    description:
      - job status to filter the results.
    required: false
    type: str
    choices: ['SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING', 'RUNNING', 'SUCCEEDED', 'FAILED']
    default: 'RUNNING'
  compute_environment_arns:
    description:
      - list of compute environment names.
      - list of compute environment arns.
    required: false
    type: list
    default: []
    aliases: ['compute_environment_names']
  list_jobs:
    description:
      - do you want to list job related to I(job_queue)?
    required: false
    type: bool
  describe_jobs:
    description:
      - do you want to describe job related to I(job_ids)?
    required: false
    type: bool
  describe_job_queues:
    description:
      - do you want to describe job queues related to I(job_queues)?
    required: false
    type: bool
  describe_job_definitions:
    description:
      - do you want to describe job definitations related to I(job_definition_arns) and I(job_definition_status)?
    required: false
    type: bool
  describe_compute_environments:
    description:
      - do you want to describe compute environments related to I(compute_environment_arns)?
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
- name: "Returns a list of AWS Batch jobs."
  aws_batch_info:
    job_queue: 'test'
    job_status: 'RUNNING'
    list_jobs: true

- name: "Describes a list of AWS Batch jobs."
  aws_batch_info:
    job_ids: ['test']
    describe_jobs: true

- name: "Describes one or more of your job queues."
  aws_batch_info:
    job_queues: []
    describe_job_queues: true

- name: "Describes a list of job definitions"
  aws_batch_info:
    job_definition_names: ['test']
    job_definition_status: 'ACTIVE'
    describe_job_definitions: true

- name: "Describes one or more of your compute environments."
  aws_batch_info:
    compute_environment_names: ['test']
    describe_compute_environments: true
"""

RETURN = """
job_summary_list:
  description: Returns a list of AWS Batch jobs.
  returned: when `list_jobs` and `job_queue` are defined and success
  type: list
  sample: [
    {
        'job_arn': 'string',
        'job_id': 'string',
        'job_name': 'string',
        'created_at': 123,
        'status': 'SUBMITTED',
        'status_reason': 'string',
        'started_at': 123,
        'stopped_at': 123,
        'container': {},
        'array_properties': {},
        'node_properties': {}
    },
  ]
jobs:
  description: Describes a list of AWS Batch jobs.
  returned: when `describe_jobs` and `job_ids` are defined and success
  type: list
  sample: [
    {
        'job_arn': 'string',
        'job_name': 'string',
        'job_id': 'string',
        'job_queue': 'string',
        'status': 'SUBMITTED',
        'attempts': [],
        'status_reason': 'string',
        'created_at': 123,
        'retry_strategy': {},
        'started_at': 123,
        'stopped_at': 123,
        'depends_on': [],
        'job_definition': 'string',
        'parameters': {},
        'container': {},
        'node_details': {},
        'node_properties': {},
        'array_properties': {},
        'timeout': {},
        'tags': {},
        'propagate_tags': True,
        'platform_capabilities': []
    },
  ]
job_queues:
  description: Describes one or more of your job queues.
  returned: when `describe_job_queues` and `job_queues` are defined and success
  type: list
  sample: [
    {
        'job_queue_name': 'string',
        'job_queue_arn': 'string',
        'state': 'ENABLED',
        'status': 'CREATING',
        'status_reason': 'string',
        'priority': 123,
        'compute_environment_order': [],
        'tags': {}
    },
  ]
job_definitions:
  description: Describes a list of job definitions.
  returned: when `describe_job_definitions` and `job_definition_arns` and `job_definition_status` are defined and success
  type: list
  sample: [
    {
        'job_definition_name': 'string',
        'job_definition_arn': 'string',
        'revision': 123,
        'status': 'string',
        'type': 'string',
        'parameters': {},
        'retry_strategy': {},
        'container_properties': {},
        'timeout': {},
        'node_properties': {},
        'tags': {},
        'propagate_tags': True,
        'platform_capabilities': []
    },
  ]
compute_environments:
  description: Describes one or more of your compute environments.
  returned: when `describe_compute_environments` and `compute_environment_arns` are defined and success
  type: list
  sample: [
    {
        'compute_environment_name': 'string',
        'compute_environment_arn': 'string',
        'ecs_cluster_arn': 'string',
        'tags': {},
        'type': 'MANAGED',
        'state': 'ENABLED',
        'status': 'CREATING',
        'status_reason': 'string',
        'compute_resources': {},
        'service_role': 'string'
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


def _batch(client, module):
    try:
        if module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    jobQueue=module.params['job_queue'],
                    jobStatus=module.params['job_status'],
                ), True
            else:
                return client.list_jobs(
                    jobQueue=module.params['job_queue'],
                    jobStatus=module.params['job_status'],
                ), False
        elif module.params['describe_jobs']:
            if client.can_paginate('describe_jobs'):
                paginator = client.get_paginator('describe_jobs')
                return paginator.paginate(
                    jobs=module.params['job_ids'],
                ), True
            else:
                return client.describe_jobs(
                    jobs=module.params['job_ids'],
                ), False
        elif module.params['describe_job_queues']:
            if client.can_paginate('describe_job_queues'):
                paginator = client.get_paginator('describe_job_queues')
                return paginator.paginate(
                    jobQueues=module.params['job_queues'],
                ), True
            else:
                return client.describe_job_queues(
                    jobQueues=module.params['job_queues'],
                ), False
        elif module.params['describe_job_definitions']:
            if client.can_paginate('describe_job_definitions'):
                paginator = client.get_paginator('describe_job_definitions')
                return paginator.paginate(
                    jobDefinitions=module.params['job_definition_arns'],
                    status=module.params['job_definition_status'],
                ), True
            else:
                return client.describe_job_definitions(
                    jobDefinitions=module.params['job_definition_arns'],
                    status=module.params['job_definition_status'],
                ), False
        elif module.params['describe_compute_environments']:
            if client.can_paginate('describe_compute_environments'):
                paginator = client.get_paginator('describe_compute_environments')
                return paginator.paginate(
                    computeEnvironments=module.params['compute_environment_arns'],
                ), True
            else:
                return client.describe_compute_environments(
                    computeEnvironments=module.params['compute_environment_arns'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws batch details')


def main():
    argument_spec = dict(
        job_queue=dict(required=False, aliases=['job_queue_arn']),
        job_queues=dict(required=False, type=list, default=[], aliases=['job_queue_arns']),
        job_definition_arns=dict(required=False, type=list, default=[], aliases=['job_definition_names']),
        job_definition_status=dict(required=False, default='ACTIVE'),
        compute_environment_arns=dict(required=False, type=list, default=[], aliases=['compute_environment_names']),
        job_status=dict(
            required=False,
            choices=['SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING', 'RUNNING', 'SUCCEEDED', 'FAILED'],
            default='RUNNING'
        ),
        job_ids=dict(required=False, type=list),
        list_jobs=dict(required=False, type=bool),
        describe_jobs=dict(required=False, type=bool),
        describe_job_queues=dict(required=False, type=bool),
        describe_job_definitions=dict(required=False, type=bool),
        describe_compute_environments=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_jobs', True, ['job_queue']),
            ('describe_jobs', True, ['job_ids']),
        ],
        mutually_exclusive=[
            (
                'list_jobs',
                'describe_jobs',
                'describe_job_queues',
                'describe_job_definitions',
                'describe_compute_environments',
            ),
        ],
    )

    client = module.client('batch', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _batch(client, module)

    if module.params['list_jobs']:
        module.exit_json(job_summary_list=aws_response_list_parser(paginate, _it, 'jobSummaryList'))
    elif module.params['describe_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, _it, 'jobs'))
    elif module.params['describe_job_queues']:
        module.exit_json(job_queues=aws_response_list_parser(paginate, _it, 'jobQueues'))
    elif module.params['describe_job_definitions']:
        module.exit_json(job_definitions=aws_response_list_parser(paginate, _it, 'jobDefinitions'))
    elif module.params['describe_compute_environments']:
        module.exit_json(compute_environments=aws_response_list_parser(paginate, _it, 'computeEnvironments'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
