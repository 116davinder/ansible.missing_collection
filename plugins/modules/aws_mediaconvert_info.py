#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediaconvert_info
short_description: Get Information about AWS Elemental MediaConvert.
description:
  - Get Information about AWS Elemental MediaConvert.
  - U(https://docs.aws.amazon.com/mediaconvert/latest/api/resources.html)
version_added: 0.0.7
options:
  list_job_templates:
    description:
      - do you want to get list of job_templates?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs for given I(job_status)?
    required: false
    type: bool
  list_presets:
    description:
      - do you want to get list of presets?
    required: false
    type: bool
  list_queues:
    description:
      - do you want to get list of queues?
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
- name: "get list of job_templates"
  aws_mediaconvert_info:
    list_job_templates: true

- name: "get list of jobs"
  aws_mediaconvert_info:
    list_jobs: true
    job_status: 'COMPLETE'

- name: "get list of presets"
  aws_mediaconvert_info:
    list_presets: true

- name: "get list of queues"
  aws_mediaconvert_info:
    list_queues: true
"""

RETURN = """
job_templates:
  description: list of job_templates.
  returned: when `list_job_templates` is defined and success.
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
presets:
  description: list of presets.
  returned: when `list_presets` is defined and success.
  type: list
queues:
  description: list of queues.
  returned: when `list_queues` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediaconvert(client, module):
    try:
        if module.params['list_job_templates']:
            if client.can_paginate('list_job_templates'):
                paginator = client.get_paginator('list_job_templates')
                return paginator.paginate(), True
            else:
                return client.list_job_templates(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    Status=module.params['job_status']
                ), True
            else:
                return client.list_jobs(
                    Status=module.params['job_status']
                ), False
        elif module.params['list_presets']:
            if client.can_paginate('list_presets'):
                paginator = client.get_paginator('list_presets')
                return paginator.paginate(), True
            else:
                return client.list_presets(), False
        elif module.params['list_queues']:
            if client.can_paginate('list_queues'):
                paginator = client.get_paginator('list_queues')
                return paginator.paginate(), True
            else:
                return client.list_queues(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental MediaConvert details')


def main():
    argument_spec = dict(
        job_status=dict(
            required=False,
            choices=['SUBMITTED', 'PROGRESSING', 'COMPLETE', 'CANCELED', 'ERROR'],
            default='COMPLETE'
        ),
        list_job_templates=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
        list_presets=dict(required=False, type=bool),
        list_queues=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_job_templates',
                'list_jobs',
                'list_presets',
                'list_queues',
            )
        ],
    )

    client = module.client('mediaconvert', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediaconvert(client, module)

    if module.params['list_job_templates']:
        module.exit_json(job_templates=aws_response_list_parser(paginate, it, 'JobTemplates'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'Jobs'))
    elif module.params['list_presets']:
        module.exit_json(presets=aws_response_list_parser(paginate, it, 'Presets'))
    elif module.params['list_queues']:
        module.exit_json(queues=aws_response_list_parser(paginate, it, 'Queues'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
