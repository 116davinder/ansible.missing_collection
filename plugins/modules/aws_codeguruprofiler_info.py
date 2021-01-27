#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codeguruprofiler_info
short_description: Get Information about Amazon CodeGuru Profiler.
description:
  - Get Information about Amazon CodeGuru Profiler
  - U(https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_Operations.html)
version_added: 0.0.3
options:
  include_description:
    description:
      - do you want to include a description in I(list_profiling_groups)?
    required: false
    type: bool
  daily_reports_only:
    description:
      - do you want to include a daily reports in I(list_findings_reports)?
    required: false
    type: bool
  end_time:
    description:
      - Time to filter results? Example: I(2021-12-01)
    required: false
    type: str
  start_time:
    description:
      - Time to filter results? Example: I(2021-12-01)
    required: false
    type: str
  profiling_group_name:
    description:
      - name of the profiling group?
    required: false
    type: str
  locale:
    description:
      - name of the locale used in I(get_recommendations).
      - Example: I(en-GB) for English, United Kingdom.
      - U(https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_GetRecommendations.html#API_GetRecommendations_RequestSyntax)
    required: false
    type: str
  list_profiling_groups:
    description:
      - do you want to get list all profiling groups?
    required: false
    type: bool
  list_findings_reports:
    description:
      - do you want to get list all finding reports for given I(profiling_group_name)?
    required: false
    type: bool
  describe_profiling_group:
    description:
      - do you want get details about given I(profiling_group_name)?
    required: false
    type: bool
  get_notification_configuration:
    description:
      - do you want to get list of notification configs for given I(profiling_group_name)?
    required: false
    type: bool
  get_recommendations:
    description:
      - do you want to list recommendations for given I(profiling_group_name)?
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
- name: "get list of profiling groups."
  aws_codeguruprofiler_info:
    list_profiling_groups: true
    include_description: true

- name: "get list of finding reports."
  aws_codeguruprofiler_info:
    list_findings_reports: true
    daily_reports_only: true
    start_time: '2020-01-01'
    end_time: '2021-01-01'
    profiling_group_name: 'test'

- name: "get details about given profiling name"
  aws_codeguruprofiler_info:
    describe_profiling_group: true
    profiling_group_name: 'test'

- name: "get list of notifications configs for profiling group name."
  aws_codeguruprofiler_info:
    get_notification_configuration: true
    profiling_group_name: 'test'

- name: "get list of profiling groups."
  aws_codeguruprofiler_info:
    get_recommendations: true
    end_time: '2021-01-01'
    start_time: '2020-01-01'
    profiling_group_name: 'test'
    locale: 'en-GB'
"""

RETURN = """
profiling_groups:
  description: get of profiling groups.
  returned: when `list_profiling_groups`, and `include_description` are defined and success
  type: list
  sample: [
    {
        'agent_orchestration_config': {
            'profiling_enabled': True
        },
        'arn': 'string',
        'compute_platform': 'AWSLambda',
        'created_at': datetime(2016, 6, 6),
        'name': 'string',
        'profiling_status': {},
        'tags': {},
        'updated_at': datetime(2015, 1, 1)
    },
  ]
findings_report_summaries:
  description: get list of findings for given report group name.
  returned: when `list_findings_reports`, `daily_reports_only`, `end_time`, `profiling_group_name`, and `start_time` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'profile_end_time': datetime(2016, 6, 6),
        'profile_start_time': datetime(2015, 1, 1),
        'profiling_group_name': 'string',
        'total_number_of_findings': 123
    },
  ]
profiling_group:
  description: get details about given report group name.
  returned: when `describe_profiling_group`, and `profiling_group_name` are defined and success
  type: dict
  sample: {
    'agent_orchestration_config': {
        'profiling_enabled': True
    },
    'arn': 'string',
    'compute_platform': 'AWSLambda',
    'created_at': datetime(2016, 6, 6),
    'name': 'string',
    'profiling_status': {},
    'tags': {},
    'updated_at': datetime(2015, 1, 1)
  }
notification_configuration:
  description: get notifications details about given report group name.
  returned: when `get_notification_configuration`, and `profiling_group_name` are defined and success
  type: dict
  sample: {
    'channels': [
        {
            'event_publishers': [
                'AnomalyDetection',
            ],
            'id': 'string',
            'uri': 'string'
        },
    ]
  }
recommendations:
  description: get recommendations details about given report group name.
  returned: when `get_recommendations`, `locale`, `end_time`, `profiling_group_name`, and `start_time` are defined and success
  type: dict
  sample: {
    'anomalies': [
        {
            'instances': [],
            'metric': {},
            'reason': 'string'
        },
    ],
    'profile_end_time': datetime(2016, 6, 6),
    'profile_start_time': datetime(2017, 7, 7),
    'profiling_group_name': 'string',
    'recommendations': [
        {
            'all_matches_count': 123,
            'all_matches_sum': 123.0,
            'end_time': datetime(2018, 8, 8),
            'pattern': {},
            'start_time': datetime(2015, 1, 1),
            'top_matches': []
        },
    ]
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible_collections.community.missing_collection.plugins.module_utils.utils import convert_str_to_datetime


def _codeguruprofiler(client, module):
    try:
        if module.params['list_profiling_groups']:
            if client.can_paginate('list_profiling_groups'):
                paginator = client.get_paginator('list_profiling_groups')
                return paginator.paginate(
                    includeDescription=module.params['include_description'],
                ), True
            else:
                return client.list_profiling_groups(
                    includeDescription=module.params['include_description'],
                ), False
        elif module.params['list_findings_reports']:
            _end_time = convert_str_to_datetime(module.params['end_time'])
            _start_time = convert_str_to_datetime(module.params['start_time'])
            if _start_time is None or _end_time is None:
                module.fail_json("date format is wrong, please use correct format. Example: '2020-06-01'")
            if client.can_paginate('list_findings_reports'):
                paginator = client.get_paginator('list_findings_reports')
                return paginator.paginate(
                    dailyReportsOnly=module.params['daily_reports_only'],
                    endTime=_end_time,
                    profilingGroupName=module.params['profiling_group_name'],
                    startTime=_start_time,
                ), True
            else:
                return client.list_findings_reports(
                    dailyReportsOnly=module.params['daily_reports_only'],
                    endTime=_end_time,
                    profilingGroupName=module.params['profiling_group_name'],
                    startTime=_start_time,
                ), False
        elif module.params['describe_profiling_group']:
            return client.describe_profiling_group(
                profilingGroupName=module.params['profiling_group_name'],
            ), False
        elif module.params['get_notification_configuration']:
            return client.get_notification_configuration(
                profilingGroupName=module.params['profiling_group_name'],
            ), False
        elif module.params['get_recommendations']:
            _end_time = _convert_str_to_datetime(module.params['end_time'])
            _start_time = _convert_str_to_datetime(module.params['start_time'])
            if _start_time is None or _end_time is None:
                module.fail_json("date format is wrong, please correct format. Example: '2020-06-01'")
            return client.get_recommendations(
                locale=module.params['locale'],
                endTime=_end_time,
                profilingGroupName=module.params['profiling_group_name'],
                startTime=_start_time,
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws code guru profiler details')


def main():
    argument_spec = dict(
        include_description=dict(required=False, type=bool),
        daily_reports_only=dict(required=False, type=bool),
        end_time=dict(required=False),
        profiling_group_name=dict(required=False),
        start_time=dict(required=False),
        locale=dict(required=False),
        list_profiling_groups=dict(required=False, type=bool),
        list_findings_reports=dict(required=False, type=bool),
        describe_profiling_group=dict(required=False, type=bool),
        get_notification_configuration=dict(required=False, type=bool),
        get_recommendations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_profiling_groups', True, ['include_description']),
            ('list_findings_reports', True, ['daily_reports_only', 'end_time', 'profiling_group_name', 'start_time']),
            ('describe_profiling_group', True, ['profiling_group_name']),
            ('get_notification_configuration', True, ['profiling_group_name']),
            ('get_recommendations', True, ['locale', 'end_time', 'profiling_group_name', 'start_time']),
        ),
        mutually_exclusive=[
            (
                'list_profiling_groups',
                'list_findings_reports',
                'describe_profiling_group',
                'get_notification_configuration',
                'get_recommendations'
            )
        ],
    )

    client = module.client('codeguruprofiler', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codeguruprofiler(client, module)

    if module.params['list_profiling_groups']:
        module.exit_json(profiling_groups=aws_response_list_parser(paginate, _it, 'profilingGroups'))
    elif module.params['list_findings_reports']:
        module.exit_json(findings_report_summaries=aws_response_list_parser(paginate, _it, 'findingsReportSummaries'))
    elif module.params['describe_profiling_group']:
        module.exit_json(profiling_group=camel_dict_to_snake_dict(_it['profilingGroup']))
    elif module.params['get_notification_configuration']:
        module.exit_json(notification_configuration=camel_dict_to_snake_dict(_it['notificationConfiguration']))
    elif module.params['get_recommendations']:
        module.exit_json(recommendations=camel_dict_to_snake_dict(_it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
