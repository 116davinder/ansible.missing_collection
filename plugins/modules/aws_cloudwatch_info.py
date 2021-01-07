#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudwatch_info
short_description: Get Information about AWS CloudWatch.
description:
  - Get Information about AWS CloudWatch.
  - U(https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  alarm_names:
    description:
      - list of alarm names.
    required: false
    type: list
    default: []
  dashboard_name:
    description:
      - name of the cloudwatch dashboard.
    required: false
    type: str
  alarm_types:
    description:
      - list of alarm types.
      - can be combination of following 'CompositeAlarm', 'MetricAlarm'.
    required: false
    type: list
    default: []
  alarm_state:
    description:
      - alarm state.
    required: false
    type: str
    choices: ['OK', 'ALARM', 'INSUFFICIENT_DATA']
    default: 'OK'
  name_space:
    description:
      - name of cloudwatch namespace example: AWS/EC2.
    required: false
    type: str
  metric_name:
    description:
      - name of cloudwatch metric example: CPUUtilization.
    required: false
    type: str
  describe_alarms:
    description:
      - do you want to fetch details about alarms for given I(alarm_names), I(alarm_types) and I(alarm_state)?
    required: false
    type: bool
  get_dashboard:
    description:
      - do you want to fetch details about cloudwatch dashboards for given I(dashboard_name)?
    required: false
    type: bool
  describe_anomaly_detectors:
    description:
      - do you want to fetch details about cloudwatch anomaly detectors for given I(name_space) and I(metric_name)?
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
- name: "get all the cloudwatch dashboards"
  aws_cloudwatch_info:

- name: "describe given cloudwatch alarms"
  aws_cloudwatch_info:
    describe_alarms: true
    alarm_names: ['test']
    alarm_state: 'OK'
    alarm_types: []

- name: "describe cloudwatch dashboard"
  aws_cloudwatch_info:
    get_dashboard: true
    dashboard_name: 'GOL'

- name: "describe anomaly detectors"
  aws_cloudwatch_info:
    describe_anomaly_detectors: true
    name_space: 'AWS/EC2'
    metric_name: 'CPUUtilization'
"""

RETURN = """
dashboards:
  description: List of cloudwatch dashboards
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        'dashboard_name': 'string',
        'dashboard_arn': 'string',
        'last_modified': datetime(2015, 1, 1),
        'size': 123
    },
  ]
alarms:
  description: get details about alarms
  returned: when `alarm_names`, `alarm_types`, `alarm_state` and `describe_alarms` are defined and success
  type: dict
  sample: {
    composite_alarms: [],
    metric_alarms: []
  }
dashboard:
  description: get details about given cloudwatch dashboard
  returned: when `dashboard_name` and `get_dashboard` are defined and success
  type: dict
  sample: {
    'dashboard_arn': 'string',
    'dashboard_body': 'string',
    'dashboard_name': 'string'
  }
anomaly_detectors:
  description: get details about given cloudwatch anomaly detectors
  returned: when `name_space` and `metric_name` and `describe_anomaly_detectors` are defined and success
  type: list
  sample: [
    {
        'namespace': 'string',
        'metric_name': 'string',
        'dimensions': [],
        'stat': 'string',
        'configuration': {
            'excluded_time_ranges': [],
            'metric_timezone': 'string'
        },
        'state_value': 'PENDING_TRAINING'
    },
  ]
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
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _cloudtrail(client, module):
    try:
        if module.params['describe_alarms']:
            if client.can_paginate('describe_alarms'):
                paginator = client.get_paginator('describe_alarms')
                return paginator.paginate(
                    AlarmNames=module.params['alarm_names'],
                    AlarmTypes=module.params['alarm_types'],
                    StateValue=module.params['alarm_state']
                ), True
            else:
                return client.describe_alarms(
                    AlarmNames=module.params['alarm_names'],
                    AlarmTypes=module.params['alarm_types'],
                    StateValue=module.params['alarm_state']
                ), False
        elif module.params['get_dashboard']:
            return client.get_dashboard(
                DashboardName=module.params['dashboard_name'],
            ), False
        elif module.params['describe_anomaly_detectors']:
            if client.can_paginate('describe_anomaly_detectors'):
                paginator = client.get_paginator('describe_anomaly_detectors')
                return paginator.paginate(
                    Namespace=module.params['name_space'],
                    MetricName=module.params['metric_name'],
                ), True
            else:
                return client.describe_anomaly_detectors(
                    Namespace=module.params['name_space'],
                    MetricName=module.params['metric_name'],
                ), False
        else:
            if client.can_paginate('list_dashboards'):
                paginator = client.get_paginator('list_dashboards')
                return paginator.paginate(), True
            else:
                return client.list_dashboards(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudtrail details')


def main():
    argument_spec = dict(
        alarm_names=dict(required=False, type=list, default=[]),
        dashboard_name=dict(required=False),
        alarm_types=dict(required=False, type=list, default=[]),
        alarm_state=dict(required=False, choices=['OK', 'ALARM', 'INSUFFICIENT_DATA'], default='OK'),
        name_space=dict(required=False),
        metric_name=dict(required=False),
        describe_alarms=dict(required=False, type=bool),
        get_dashboard=dict(required=False, type=bool),
        describe_anomaly_detectors=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_alarms', True, ['alarm_names', 'alarm_types', 'alarm_state']),
            ('get_dashboard', True, ['dashboard_name']),
            ('describe_anomaly_detectors', True, ['name_space', 'metric_name']),
        ),
        mutually_exclusive=[
            (
                'describe_alarms',
                'get_dashboard',
                'describe_anomaly_detectors'
            ),
            (
                'alarm_names',
                'dashboard_name'
            )
        ],
    )

    client = module.client('cloudwatch', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudtrail(client, module)

    if module.params['describe_alarms']:
        composite_alarms = aws_response_list_parser(paginate, _it, 'CompositeAlarms')
        metric_alarms = aws_response_list_parser(paginate, _it, 'MetricAlarms')
        module.exit_json(
            alarms={
                "composite_alarms": composite_alarms,
                "metric_alarms": metric_alarms
            }
        )
    elif module.params['get_dashboard']:
        module.exit_json(dashboard=camel_dict_to_snake_dict(_it))
    elif module.params['describe_anomaly_detectors']:
        module.exit_json(anomaly_detectors=aws_response_list_parser(paginate, _it, 'AnomalyDetectors'))
    else:
        module.exit_json(dashboards=aws_response_list_parser(paginate, _it, 'DashboardEntries'))


if __name__ == '__main__':
    main()
