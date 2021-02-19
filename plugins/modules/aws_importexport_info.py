#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_importexport_info
short_description: Get Information about AWS Import/Export.
description:
  - Get Information about AWS Import/Export.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html)
version_added: 0.0.6
options:
  job_id:
    description:
      - id of aws import/export job.
    required: false
    type: str
  job_ids:
    description:
      - list of job ids for shipping label.
    required: false
    type: list
  list_jobs:
    description:
      - do you want to get list of jobs?
    required: false
    type: bool
  get_shipping_label:
    description:
      - do you want to get shipping label for given I(job_ids)
    required: false
    type: bool
  get_status:
    description:
      - do you want to get job status for given I(job_id)?
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
- name: "get list of jobs"
  aws_importexport_info:
    list_jobs: true

- name: "get shipping label"
  aws_importexport_info:
    get_shipping_label: true
    job_ids: ['test-job-id']

- name: "get job status"
  aws_importexport_info:
    get_status: true
    job_id: 'test-id'
"""

RETURN = """
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
shipping_label:
  description: list of shipping_label.
  returned: when `get_shipping_label` is defined and success.
  type: dict
status:
  description: list of status.
  returned: when `get_status` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _importexport(client, module):
    try:
        if module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(), True
            else:
                return client.list_jobs(), False
        elif module.params['get_shipping_label']:
            return client.get_shipping_label(
                jobIds=module.params['job_ids'],
            ), False
        elif module.params['get_status']:
            return client.get_status(
                JobId=module.params['job_id'],
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Import/Export Jobs details')


def main():
    argument_spec = dict(
        job_id=dict(required=False),
        job_ids=dict(required=False, type=list),
        list_jobs=dict(required=False, type=bool),
        get_shipping_label=dict(required=False, type=bool),
        get_status=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_shipping_label', True, ['job_ids']),
            ('get_status', True, ['job_id']),
        ),
        mutually_exclusive=[
            (
                'list_jobs',
                'get_shipping_label',
                'get_status',
            )
        ],
    )

    client = module.client('importexport', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _importexport(client, module)

    if module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'Jobs'))
    elif module.params['get_shipping_label']:
        module.exit_json(shipping_label=it)
    elif module.params['get_status']:
        module.exit_json(status=it)
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
