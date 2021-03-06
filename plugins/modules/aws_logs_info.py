#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_logs_info
short_description: Get Information about Amazon CloudWatch Logs.
description:
  - Get Information about Amazon CloudWatch Logs.
  - U(https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  name:
    description:
      - name of log group.
    required: false
    type: str
    aliases: ['log_stream_name']
  describe_log_groups:
    description:
      - do you want to get list of log_groups?
    required: false
    type: bool
  describe_destinations:
    description:
      - do you want to get list of destinations?
    required: false
    type: bool
  describe_export_tasks:
    description:
      - do you want to get list of export_tasks for given I(task_status)?
    required: false
    type: bool
  describe_log_streams:
    description:
      - do you want to get list of log_streams for given log group name I(name)?
    required: false
    type: bool
  describe_metric_filters:
    description:
      - do you want to get list of metric_filters for given log group name I(name)?
    required: false
    type: bool
  describe_queries:
    description:
      - do you want to get list of queries for given log group name I(name)?
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
- name: "get list of log_groups"
  aws_logs_info:
    describe_log_groups: true
  register: _reg

- name: "get list of destinations"
  aws_logs_info:
    describe_destinations: true

- name: "get list of export_tasks"
  aws_logs_info:
    describe_export_tasks: true
    task_status: 'COMPLETED'

- name: "get list of log_streams"
  aws_logs_info:
    describe_log_streams: true
    name: '{{ _reg.log_groups[0].logGroupName }}'

- name: "get list of metric_filters"
  aws_logs_info:
    describe_metric_filters: true
    name: '{{ _reg.log_groups[0].logGroupName }}'

- name: "get list of queries"
  aws_logs_info:
    describe_queries: true
    name: '{{ _reg.log_groups[0].logGroupName }}'
    query_status: 'Complete'
"""

RETURN = """
log_groups:
  description: list of log_groups.
  returned: when `describe_log_groups` is defined and success.
  type: list
destinations:
  description: list of destinations.
  returned: when `describe_destinations` is defined and success.
  type: list
export_tasks:
  description: list of export_tasks.
  returned: when `describe_export_tasks` is defined and success.
  type: list
log_streams:
  description: list of log_streams.
  returned: when `describe_log_streams` is defined and success.
  type: list
metric_filters:
  description: list of metric_filters.
  returned: when `describe_metric_filters` is defined and success.
  type: list
queries:
  description: list of queries.
  returned: when `describe_queries` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _logs(client, module):
    try:
        if module.params['describe_log_groups']:
            if client.can_paginate('describe_log_groups'):
                paginator = client.get_paginator('describe_log_groups')
                return paginator.paginate(), True
            else:
                return client.describe_log_groups(), False
        elif module.params['describe_destinations']:
            if client.can_paginate('describe_destinations'):
                paginator = client.get_paginator('describe_destinations')
                return paginator.paginate(), True
            else:
                return client.describe_destinations(), False
        elif module.params['describe_export_tasks']:
            if client.can_paginate('describe_export_tasks'):
                paginator = client.get_paginator('describe_export_tasks')
                return paginator.paginate(
                    statusCode=module.params['task_status']
                ), True
            else:
                return client.describe_export_tasks(
                    statusCode=module.params['task_status']
                ), False
        elif module.params['describe_log_streams']:
            if client.can_paginate('describe_log_streams'):
                paginator = client.get_paginator('describe_log_streams')
                return paginator.paginate(
                    logGroupName=module.params['name']
                ), True
            else:
                return client.describe_log_streams(
                    logGroupName=module.params['name']
                ), False
        elif module.params['describe_metric_filters']:
            if client.can_paginate('describe_metric_filters'):
                paginator = client.get_paginator('describe_metric_filters')
                return paginator.paginate(
                    logGroupName=module.params['name']
                ), True
            else:
                return client.describe_metric_filters(
                    logGroupName=module.params['name']
                ), False
        elif module.params['describe_queries']:
            if client.can_paginate('describe_queries'):
                paginator = client.get_paginator('describe_queries')
                return paginator.paginate(
                    logGroupName=module.params['name'],
                    status=module.params['query_status']
                ), True
            else:
                return client.describe_queries(
                    logGroupName=module.params['name'],
                    status=module.params['query_status']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon CloudWatch Logs details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['log_stream_name']),
        task_status=dict(
            required=False,
            choices=['CANCELLED', 'COMPLETED', 'FAILED', 'PENDING', 'PENDING_CANCEL', 'RUNNING'],
            default='COMPLETED'
        ),
        query_status=dict(
            required=False,
            choices=['Scheduled', 'Running', 'Complete', 'Failed', 'Cancelled'],
            default='Complete'
        ),
        describe_log_groups=dict(required=False, type=bool),
        describe_destinations=dict(required=False, type=bool),
        describe_export_tasks=dict(required=False, type=bool),
        describe_log_streams=dict(required=False, type=bool),
        describe_metric_filters=dict(required=False, type=bool),
        describe_queries=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_log_streams', True, ['name']),
            ('describe_metric_filters', True, ['name']),
            ('describe_queries', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'describe_log_groups',
                'describe_destinations',
                'describe_export_tasks',
                'describe_log_streams',
                'describe_metric_filters',
                'describe_queries',
            )
        ],
    )

    client = module.client('logs', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _logs(client, module)

    if module.params['describe_log_groups']:
        module.exit_json(log_groups=aws_response_list_parser(paginate, it, 'logGroups'))
    elif module.params['describe_destinations']:
        module.exit_json(destinations=aws_response_list_parser(paginate, it, 'destinations'))
    elif module.params['describe_export_tasks']:
        module.exit_json(export_tasks=aws_response_list_parser(paginate, it, 'exportTasks'))
    elif module.params['describe_log_streams']:
        module.exit_json(log_streams=aws_response_list_parser(paginate, it, 'logStreams'))
    elif module.params['describe_metric_filters']:
        module.exit_json(metric_filters=aws_response_list_parser(paginate, it, 'metricFilters'))
    elif module.params['describe_queries']:
        module.exit_json(queries=aws_response_list_parser(paginate, it, 'queries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
