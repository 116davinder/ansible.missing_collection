#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_elastictranscoder_info
short_description: Get Information about Amazon Elastic Transcoder.
description:
  - Get Information about Amazon Elastic Transcoder.
  - U(https://docs.aws.amazon.com/elastictranscoder/latest/developerguide/operations-jobs.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of pipeline.
    required: false
    type: str
  status:
    description:
      - status of job.
    required: false
    type: str
    choices: ['Submitted', 'Progressing', 'Complete', 'Canceled', 'Error']
    default: 'Submitted'
  list_presets:
    description:
      - do you want to get list of presets?
    required: false
    type: bool
  list_jobs_by_pipeline:
    description:
      - do you want to get list of jobs for given pipeline I(id)?
    required: false
    type: bool
  list_jobs_by_status:
    description:
      - do you want to get list of jobs for given I(status)?
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
- name: "get list of all pipelines."
  aws_elastictranscoder_info:

- name: "get list of presets."
  aws_elastictranscoder_info:
    list_presets: true

- name: "get list of jobs by pipelineId"
  aws_elastictranscoder_info:
    list_jobs_by_pipeline: true
    id: 'test-pipeline-id'

- name: "get list of jobs by status"
  aws_elastictranscoder_info:
    list_jobs_by_status: true
    status: 'Submitted'
"""

RETURN = """
pipelines:
  description: list of all pipelines.
  returned: when no arguments are defined and success
  type: list
presets:
  description: list of presets.
  returned: when `list_presets` is defined and success
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs_by_pipeline` or `list_jobs_by_status` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _elastictranscoder(client, module):
    try:
        if module.params['list_presets']:
            if client.can_paginate('list_presets'):
                paginator = client.get_paginator('list_presets')
                return paginator.paginate(), True
            else:
                return client.list_presets(), False
        elif module.params['list_jobs_by_pipeline']:
            if client.can_paginate('list_jobs_by_pipeline'):
                paginator = client.get_paginator('list_jobs_by_pipeline')
                return paginator.paginate(
                    PipelineId=module.params['id'],
                ), True
            else:
                return client.list_jobs_by_pipeline(
                    PipelineId=module.params['id'],
                ), False
        elif module.params['list_jobs_by_status']:
            if client.can_paginate('list_jobs_by_status'):
                paginator = client.get_paginator('list_jobs_by_status')
                return paginator.paginate(
                    Status=module.params['status'],
                ), True
            else:
                return client.list_jobs_by_status(
                    Status=module.params['status'],
                ), False
        else:
            if client.can_paginate('list_pipelines'):
                paginator = client.get_paginator('list_pipelines')
                return paginator.paginate(), True
            else:
                return client.list_pipelines(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elastic Transcoder details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        status=dict(
            required=False,
            choices=['Submitted', 'Progressing', 'Complete', 'Canceled', 'Error'],
            default='Submitted'
        ),
        list_presets=dict(required=False, type=bool),
        list_jobs_by_pipeline=dict(required=False, type=bool),
        list_jobs_by_status=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_jobs_by_pipeline', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_presets',
                'list_jobs_by_pipeline',
                'list_jobs_by_status',
            )
        ],
    )

    client = module.client('elastictranscoder', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _elastictranscoder(client, module)

    if module.params['list_presets']:
        module.exit_json(presets=aws_response_list_parser(paginate, it, 'Presets'))
    elif module.params['list_jobs_by_pipeline'] or module.params['list_jobs_by_status']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'Jobs'))
    else:
        module.exit_json(pipelines=aws_response_list_parser(paginate, it, 'Pipelines'))


if __name__ == '__main__':
    main()
