#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_emr_containers_info
short_description: Get Information about Amazon EMR Containers.
description:
  - Get Information about Amazon EMR Containers.
  - U(https://docs.aws.amazon.com/emr-on-eks/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of emr virtual cluster.
    required: false
    type: str
  job_run_states:
    description:
      - list of job run states to filter results.
      - can be combination of following 'PENDING', 'SUBMITTED',
        'RUNNING', 'FAILED', 'CANCELLED', 'CANCEL_PENDING', 'COMPLETED'.
    required: false
    type: list
  managed_endpoint_states:
    description:
      - list of job managed endpoints states to filter results.
      - can be combination of following 'CREATING', 'ACTIVE', 'TERMINATING',
        'TERMINATED', 'TERMINATED_WITH_ERRORS'.
    required: false
    type: list
  list_job_runs:
    description:
      - do you want to get list of job runs for given I(id)?
    required: false
    type: bool
  list_managed_endpoints:
    description:
      - do you want to get list of managed endpoints for given I(id)?
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
- name: "get list of all emr virtual clusters"
  aws_emr_containers_info:

- name: "get list of job runs"
  aws_emr_containers_info:
    list_job_runs: true
    id: 'test'
    job_run_states: ['PENDING', 'SUBMITTED', 'RUNNING']

- name: "get list of managed endpoints"
  aws_emr_containers_info:
    list_managed_endpoints: true
    id: 'test'
    managed_endpoint_states: ['CREATING', 'ACTIVE']
"""

RETURN = """
clusters:
  description: list of all emr virtual clusters.
  returned: when no arguments are defined and success
  type: list
job_runs:
  description: list of job runs.
  returned: when `list_job_runs` is defined and success
  type: list
managed_endpoints:
  description: list of managed endpoints.
  returned: when `list_managed_endpoints` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _emr_containers(client, module):
    try:
        if module.params['list_job_runs']:
            if client.can_paginate('list_job_runs'):
                paginator = client.get_paginator('list_job_runs')
                return paginator.paginate(
                    virtualClusterId=module.params['id'],
                    states=module.params['job_run_states']
                ), True
            else:
                return client.list_job_runs(
                    virtualClusterId=module.params['id'],
                    states=module.params['job_run_states']
                ), False
        elif module.params['list_managed_endpoints']:
            if client.can_paginate('list_managed_endpoints'):
                paginator = client.get_paginator('list_managed_endpoints')
                return paginator.paginate(
                    virtualClusterId=module.params['id'],
                    states=module.params['managed_endpoint_states']
                ), True
            else:
                return client.list_managed_endpoints(
                    virtualClusterId=module.params['id'],
                    states=module.params['managed_endpoint_states']
                ), False
        else:
            if client.can_paginate('list_virtual_clusters'):
                paginator = client.get_paginator('list_virtual_clusters')
                return paginator.paginate(), True
            else:
                return client.list_virtual_clusters(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon EMR Containers details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        job_run_states=dict(
            required=False,
            type=list,
            default=[]
        ),
        managed_endpoint_states=dict(
            required=False,
            type=list,
            default=[]
        ),
        list_job_runs=dict(required=False, type=bool),
        list_managed_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_job_runs', True, ['id']),
            ('list_managed_endpoints', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_job_runs',
                'list_managed_endpoints',
            )
        ],
    )

    client = module.client('emr-containers', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _emr_containers(client, module)

    if module.params['list_job_runs']:
        module.exit_json(job_runs=aws_response_list_parser(paginate, it, 'jobRuns'))
    elif module.params['list_managed_endpoints']:
        module.exit_json(managed_endpoints=aws_response_list_parser(paginate, it, 'endpoints'))
    else:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'virtualClusters'))


if __name__ == '__main__':
    main()
