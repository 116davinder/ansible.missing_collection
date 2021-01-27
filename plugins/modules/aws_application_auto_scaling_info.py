#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_application_auto_scaling_info
short_description: Get details about AWS Application Auto Scaling.
description:
  - Get Information about AWS Application Auto Scaling.
  - U(https://docs.aws.amazon.com/autoscaling/application/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  service_namespace:
    description:
      - The namespace of the AWS service that provides the resource.
    required: true
    type: str
  describe_scalable_targets:
    description:
      - do you want to describe/fetch list of aws application autoscaling targets for given I(service_namespace)?
    required: false
    type: bool
  describe_scaling_activities:
    description:
      - do you want to describe/fetch list of aws application autoscaling activities for given I(service_namespace)?
    required: false
    type: bool
  describe_scaling_policies:
    description:
      - do you want to describe/fetch list of aws application autoscaling policies for given I(service_namespace)?
    required: false
    type: bool
  describe_scheduled_actions:
    description:
      - do you want to describe/fetch list of aws application autoscaling scheduled actions for given I(service_namespace)?
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
- name: "Gets information about the scalable targets in the specified namespace"
  aws_application_auto_scaling_info:
    service_namespace: 'ecs'
    describe_scalable_targets: true

- name: "descriptive information about the scaling activities in the specified namespace"
  aws_application_auto_scaling_info:
    service_namespace: 'elasticmapreduce'
    describe_scaling_activities: true

- name: "Describes the Application Auto Scaling scaling policies for the specified service namespace"
  aws_application_auto_scaling_info:
    service_namespace: 'appstream'
    describe_scaling_policies: true

- name: "Describes the Application Auto Scaling scheduled actions for the specified service namespace"
  aws_application_auto_scaling_info:
    service_namespace: 'rds'
    describe_scheduled_actions: true
"""

RETURN = """
scalable_targets:
  description: Gets information about the scalable targets in the specified namespace.
  returned: when `service_namespace` is defined and `describe_scalable_targets=true` and success
  type: list
  sample: [
    {
      'service_namespace': 'ecs',
      'resource_id': 'string',
      'scalable_dimension': 'ecs:service:DesiredCount',
      'min_capacity': 123,
      'max_capacity': 123,
      'role_arn': 'string',
      'creation_time': datetime(2015, 1, 10),
      'suspended_state': {}
    },
  ]
scaling_activities:
  description: Provides descriptive information about the scaling activities in the specified namespace from the previous six weeks.
  returned: when `service_namespace` is defined and `describe_scaling_activities=true` and success
  type: list
  sample: [
    {
      'activity_id': 'string',
      'service_namespace': 'kafka',
      'resource_id': 'string',
      'scalable_dimension': 'kafka:broker-storage:VolumeSize',
      'description': 'string',
      'cause': 'string',
      'start_time': datetime(2015, 1, 5),
      'end_time': datetime(2018, 8, 8),
      'status_code': 'InProgress',
      'status_message': 'string',
      'details': 'string'
    },
  ]
scaling_policies:
  description: Describes the Application Auto Scaling scaling policies for the specified service namespace.
  returned: when `service_namespace` is defined and `describe_scaling_policies=true` and success
  type: list
  sample: [
    {
      'policy_arn': 'string',
      'policy_name': 'string',
      'service_namespace': 'dynamodb',
      'resource_id': 'string',
      'scalable_dimension': 'dynamodb:table:ReadCapacityUnits',
      'policy_type': 'StepScaling',
      'step_scaling_policy_configuration': {},
      'target_tracking_scaling_policy_configuration': {},
      'alarms': [],
      'creation_time': datetime(2016, 9, 9)
    },
  ]
scheduled_actions:
  description: Describes the Application Auto Scaling scheduled actions for the specified service namespace.
  returned: when `service_namespace` is defined and `describe_scheduled_actions=true` and success
  type: list
  sample: [
    {
      'scheduled_action_name': 'string',
      'scheduled_action_arn': 'string',
      'service_namespace': 'ecs',
      'schedule': 'string',
      'resource_id': 'string',
      'scalable_dimension': 'ecs:service:DesiredCount',
      'start_time': datetime(2017, 1, 4),
      'end_time': datetime(2016, 2, 2),
      'scalable_target_action': {},
      'creation_time': datetime(2010, 10, 7)
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


def _app_autoscaling(client, module):
    try:
        if module.params['describe_scalable_targets']:
            if client.can_paginate('describe_scalable_targets'):
                paginator = client.get_paginator('describe_scalable_targets')
                return paginator.paginate(
                    ServiceNamespace=module.params['service_namespace'],
                ), True
            else:
                return client.describe_scalable_targets(
                    ServiceNamespace=module.params['service_namespace'],
                ), False
        elif module.params['describe_scaling_activities']:
            if client.can_paginate('describe_scaling_activities'):
                paginator = client.get_paginator('describe_scaling_activities')
                return paginator.paginate(
                    ServiceNamespace=module.params['service_namespace'],
                ), True
            else:
                return client.describe_scaling_activities(
                    ServiceNamespace=module.params['service_namespace'],
                ), False
        elif module.params['describe_scaling_policies']:
            if client.can_paginate('describe_scaling_policies'):
                paginator = client.get_paginator('describe_scaling_policies')
                return paginator.paginate(
                    ServiceNamespace=module.params['service_namespace'],
                ), True
            else:
                return client.describe_scaling_policies(
                    ServiceNamespace=module.params['service_namespace'],
                ), False
        elif module.params['describe_scheduled_actions']:
            if client.can_paginate('describe_scheduled_actions'):
                paginator = client.get_paginator('describe_scheduled_actions')
                return paginator.paginate(
                    ServiceNamespace=module.params['service_namespace'],
                ), True
            else:
                return client.describe_scheduled_actions(
                    ServiceNamespace=module.params['service_namespace'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws application autoscaling details')


def main():
    argument_spec = dict(
        service_namespace=dict(required=True),
        describe_scalable_targets=dict(required=False, type=bool),
        describe_scaling_activities=dict(required=False, type=bool),
        describe_scaling_policies=dict(required=False, type=bool),
        describe_scheduled_actions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_scalable_targets', True, ['service_namespace']),
            ('describe_scaling_activities', True, ['service_namespace']),
            ('describe_scaling_policies', True, ['service_namespace']),
            ('describe_scheduled_actions', True, ['service_namespace']),
        ],
        mutually_exclusive=[
            (
                'describe_scalable_targets',
                'describe_scaling_activities'
                'describe_scaling_policies',
                'describe_scheduled_actions',
            ),
        ],
    )

    client = module.client('application-autoscaling', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _app_autoscaling(client, module)

    if module.params['describe_scalable_targets']:
        module.exit_json(scalable_targets=aws_response_list_parser(paginate, _it, 'ScalableTargets'))
    elif module.params['describe_scaling_activities']:
        module.exit_json(scaling_activities=aws_response_list_parser(paginate, _it, 'ScalingActivities'))
    elif module.params['describe_scaling_policies']:
        module.exit_json(scaling_policies=aws_response_list_parser(paginate, _it, 'ScalingPolicies'))
    elif module.params['describe_scheduled_actions']:
        module.exit_json(scheduled_actions=aws_response_list_parser(paginate, _it, 'ScheduledActions'))
    else:
        module.fail_json("unknown options passed to module")


if __name__ == '__main__':
    main()
