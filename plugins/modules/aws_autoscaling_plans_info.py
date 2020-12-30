#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_autoscaling_plans_info
short_description: Get details about AWS Auto Scaling Plans.
description:
  - Get Information about AWS Auto Scaling Plans.
  - U(https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  scaling_plan_name:
    description:
      - name of scaling plan.
    required: false
    type: str
  scaling_plan_names:
    description:
      - list of scaling plan names.
    required: false
    type: list
    default: []
  scaling_plan_version:
    description:
      - version of scaling plan.
    required: false
    type: int
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
- name: "Describes one or more of your scaling plans."
  aws_autoscaling_plans_info:
    scaling_plan_names: []  #all plans
    describe_scaling_plans: true

- name: "Describes the scalable resources in the specified scaling plan."
  aws_autoscaling_plans_info:
    scaling_plan_name: 'test'
    scaling_plan_version: 1
    describe_scaling_plan_resources: true
"""

RETURN = """
scaling_plans:
  description: Describes one or more of your scaling plans.
  returned: when `scaling_plan_names` and `describe_scaling_plans` are defined and success
  type: list
  sample: [
    {
      'scaling_plan_name': 'string',
      'scaling_plan_version': 123,
      'application_source': {},
      'scaling_instructions': [
        {
          'service_namespace': 'autoscaling',
          'resource_id': 'string',
          'scalable_dimension': 'autoscaling:autoScalingGroup:DesiredCapacity',
          'min_capacity': 123,
          'max_capacity': 123,
          'target_tracking_configurations': [],
          'predefined_load_metric_specification': {},
          'customized_load_metric_specification': {},
          'scheduled_action_buffer_time': 123,
          'predictive_scaling_max_capacity_behavior': 'SetForecastCapacityToMaxCapacity',
          'predictive_scaling_max_capacity_buffer': 123,
          'predictive_scaling_mode': 'ForecastAndScale',
          'scaling_policy_update_behavior': 'KeepExternalPolicies',
          'disable_dynamic_scaling': True
        }
      ],
      'status_code': 'Active',
      'status_message': 'string',
      'status_start_time': 'xxxxxx',
      'creation_time': 'yyyyyyyyyy'
    }
  ]
scaling_plan_resources:
  description: Describes the scalable resources in the specified scaling plan.
  returned: when `describe_scaling_plan_resources` and `scaling_plan_name` and `scaling_plan_version` are defined and success
  type: list
  sample: [
    {
      'scaling_plan_name': 'string',
      'scaling_plan_version': 123,
      'service_namespace': 'autoscaling',
      'resource_id': 'string',
      'scalable_dimension': 'autoscaling:autoScalingGroup:DesiredCapacity',
      'scaling_policies': [
        {
          'policy_name': 'string',
          'policy_type': 'TargetTrackingScaling',
          'target_tracking_configuration': {
            'predefined_scaling_metric_specification': {},
            'customized_scaling_metric_specification': {},
            'target_value': 123.0,
            'disable_scale_in': True,
            'scale_out_cooldown': 123,
            'scale_in_cooldown': 123,
            'estimated_instance_warmup': 123
          }
        }
      ],
      'scaling_status_code': 'Inactive',
      'scaling_status_message': 'string'
    }
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _autoscaling(client, module):
    try:
        if module.params['describe_scaling_plans']:
            if client.can_paginate('describe_scaling_plans'):
                paginator = client.get_paginator('describe_scaling_plans')
                return paginator.paginate(
                    ScalingPlanNames=module.params['scaling_plan_names']
                ), True
            else:
                return client.describe_scaling_plans(
                    ScalingPlanNames=module.params['scaling_plan_names']
                ), False
        elif module.params['describe_scaling_plan_resources']:
            if client.can_paginate('describe_scaling_plan_resources'):
                paginator = client.get_paginator('describe_scaling_plan_resources')
                return paginator.paginate(
                    ScalingPlanName=module.params['scaling_plan_name'],
                    ScalingPlanVersion=module.params['scaling_plan_version'],
                ), True
            else:
                return client.describe_scaling_plan_resources(
                    ScalingPlanName=module.params['scaling_plan_name'],
                    ScalingPlanVersion=module.params['scaling_plan_version'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws autoscaling plans details')


def main():
    argument_spec = dict(
        scaling_plan_name=dict(required=False),
        scaling_plan_names=dict(required=False, type=list, default=[]),
        scaling_plan_version=dict(required=False, type=int),
        describe_scaling_plans=dict(required=False, type=bool),
        describe_scaling_plan_resources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_scaling_plans', True, ['scaling_plan_names']),
            ('describe_scaling_plan_resources', True, ['scaling_plan_name', 'scaling_plan_version']),
        ],
        mutually_exclusive=[
            (
                'describe_scaling_plans',
                'describe_scaling_plan_resources'
            ),
        ],
    )

    client = module.client('autoscaling-plans', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _autoscaling(client, module)

    if module.params['describe_scaling_plans']:
        module.exit_json(scaling_plans=aws_response_list_parser(paginate, _it, 'ScalingPlans'))
    elif module.params['describe_scaling_plan_resources']:
        module.exit_json(scaling_plan_resources=aws_response_list_parser(paginate, _it, 'ScalingPlanResources'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
