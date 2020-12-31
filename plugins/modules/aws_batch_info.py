#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
  scaling_plan_name:
    description:
      - name of scaling plan.
    required: false
    type: str
  describe_scaling_plans:
    description:
      - do you want to describe all scaling plans or given scaling names I(scaling_plan_names)?
    required: false
    type: bool
  describe_scaling_plan_resources:
    description:
      - do you want to describe all scaling plan resources for I(scaling_plan_name) and I(scaling_plan_version)?
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
scaling_plans:
  description: Describes one or more of your scaling plans.
  returned: when `scaling_plan_names` and `describe_scaling_plans` are defined and success
  type: list
  sample: 
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


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
        list_jobs=dict(required=False, type=bool),
        job_ids=dict(required=False, type=list),
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
