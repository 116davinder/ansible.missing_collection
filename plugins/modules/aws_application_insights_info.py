#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_application_insights_info
short_description: Get details about Amazon CloudWatch Application Insights.
description:
  - Get Information about Amazon CloudWatch Application Insights.
  - U(https://docs.aws.amazon.com/appinsights/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  name:
    description:
      - name of resource group.
    required: false
    type: str
    aliases: ['resource_group_name']
  list_components:
    description:
      - do you want to fetch all components of given group name I(name)?
    required: false
    type: bool
  list_configuration_history:
    description:
      - do you want to fetch history of given group name I(name)?
      - I(list_configuration_history_event_status) is required for it.
    required: false
    type: bool
  list_configuration_history_event_status:
    description:
      - which type of history event?
    required: false
    type: str
    choices: ['INFO', 'WARN', 'ERROR']
  list_log_pattern_sets:
    description:
      - do you want to fetch all log pattern sets for given group name I(name)?
    required: false
    type: bool
  list_log_patterns:
    description:
      - do you want to fetch all log patterns for given group name I(name)?
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
- name: "list of all aws insights applications"
  aws_application_insights_info:

- name: "list of applications components for given group name"
  aws_application_insights_info:
    name: 'test'
    list_components: true

- name: "list history of events for given group name"
  aws_application_insights_info:
    name: 'test'
    list_configuration_history: true
    list_configuration_history_event_status: 'INFO'

- name: "list log patterns sets for given group name"
  aws_application_insights_info:
    name: 'test'
    list_log_pattern_sets: true

- name: "list of log patterns for given group name"
  aws_application_insights_info:
    name: 'test'
    list_log_patterns: true
"""

RETURN = """
application_list:
  description: List of applications.
  returned: when no argument and success
  type: list
  sample: [
    {
        'resource_group_name': 'string',
        'life_cycle': 'string',
        'ops_item_sns_topic_arn': 'string',
        'ops_center_enabled': True,
        'cwe_monitor_enabled': True,
        'remarks': 'string'
    },
  ]
component_list:
  description: List of application components.
  returned: when `name` is defined and `list_components=true` and success
  type: list
  sample: [
    {
        'component_name': 'string',
        'component_remarks': 'string',
        'resource_type': 'string',
        'os_type': 'LINUX',
        'tier': 'CUSTOM',
        'monitor': True,
        'detected_workload': {
            'string': {
                'string': 'string'
            }
        }
    },
  ]
event_list:
  description: List of configuration history events for group name.
  returned: when `name` and `list_configuration_history_event_status` is defined and `list_configuration_history=true` and success
  type: list
  sample: [
    {
        'monitored_resource_arn': 'string',
        'event_status': 'INFO',
        'event_resource_type': 'CLOUDWATCH_ALARM',
        'event_time': datetime(2015, 1, 1),
        'event_detail': 'string',
        'event_resource_name': 'string'
    },
  ]
list_log_pattern_sets:
  description: List of log pattern sets for group name.
  returned: when `name` and `list_log_pattern_sets=true` and success
  type: list
  sample: [
        'string',
  ]
list_log_patterns:
  description: List of log patterns for group name.
  returned: when `name` and `list_log_patterns=true` and success
  type: list
  sample: [
    {
        'pattern_set_name': 'string',
        'pattern_name': 'string',
        'pattern': 'string',
        'rank': 123
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


def _app_insights(client, module):
    try:
        if module.params['list_components']:
            if client.can_paginate('list_components'):
                paginator = client.get_paginator('list_components')
                return paginator.paginate(
                    ResourceGroupName=module.params['name']
                ), True
            else:
                return client.list_components(
                    ResourceGroupName=module.params['name']
                ), False
        elif module.params['list_configuration_history']:
            if client.can_paginate('list_configuration_history'):
                paginator = client.get_paginator('list_configuration_history')
                return paginator.paginate(
                    ResourceGroupName=module.params['name'],
                    EventStatus=module.params['list_configuration_history_event_status']
                ), True
            else:
                return client.list_configuration_history(
                    ResourceGroupName=module.params['name'],
                    EventStatus=module.params['list_configuration_history_event_status']
                ), False
        elif module.params['list_log_pattern_sets']:
            if client.can_paginate('list_log_pattern_sets'):
                paginator = client.get_paginator('list_log_pattern_sets')
                return paginator.paginate(
                    ResourceGroupName=module.params['name'],
                ), True
            else:
                return client.list_log_pattern_sets(
                    ResourceGroupName=module.params['name'],
                ), False
        elif module.params['list_log_patterns']:
            if client.can_paginate('list_log_patterns'):
                paginator = client.get_paginator('list_log_patterns')
                return paginator.paginate(
                    ResourceGroupName=module.params['name'],
                ), True
            else:
                return client.list_log_patterns(
                    ResourceGroupName=module.params['name'],
                ), False
        else:
            if client.can_paginate('list_applications'):
                paginator = client.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return client.list_applications(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws application insights details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['resource_group_name']),
        list_components=dict(required=False, type=bool),
        list_configuration_history=dict(required=False, type=bool),
        list_configuration_history_event_status=dict(required=False, choices=['INFO', 'WARN', 'ERROR']),
        list_log_pattern_sets=dict(required=False, type=bool),
        list_log_patterns=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_components', True, ['name']),
            ('list_log_pattern_sets', True, ['name']),
            ('list_log_patterns', True, ['name']),
            ('list_configuration_history', True, ['name', 'list_configuration_history_event_status']),
        ],
        mutually_exclusive=[
            (
                'list_components',
                'list_configuration_history',
                'list_log_pattern_sets',
                'list_log_patterns'
            ),
        ],
    )

    client = module.client('application-insights', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _app_insights(client, module)

    if module.params['list_components']:
        module.exit_json(component_list=aws_response_list_parser(paginate, _it, 'ApplicationComponentList'))
    elif module.params['list_configuration_history']:
        module.exit_json(event_list=aws_response_list_parser(paginate, _it, 'EventList'))
    elif module.params['list_log_pattern_sets']:
        module.exit_json(log_pattern_sets=aws_response_list_parser(paginate, _it, 'LogPatternSets'))
    elif module.params['list_log_patterns']:
        module.exit_json(log_patterns=aws_response_list_parser(paginate, _it, 'LogPatterns'))
    else:
        module.exit_json(application_list=aws_response_list_parser(paginate, _it, 'ApplicationInfoList'))


if __name__ == '__main__':
    main()
