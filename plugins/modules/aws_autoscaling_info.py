#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_autoscaling_info
short_description: Get details about Amazon EC2 Auto Scaling.
description:
  - Get Information about Amazon EC2 Auto Scaling.
  - U(https://docs.aws.amazon.com/autoscaling/ec2/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  asg_name:
    description:
      - name of the autoscaling group.
    required: false
    type: str
  asg_names:
    description:
      - list of the autoscaling group names.
    required: false
    type: list
    default: []
  instance_ids:
    description:
      - list of the ec2 instance ids.
    required: false
    type: list
    default: []
  launch_config_names:
    description:
      - list of the autoscaling launch configuration names.
    required: false
    type: list
    default: []
  policy_types:
    description:
      - list of the autoscaling policy types.
      - Combination of SimpleScaling, StepScaling, TargetTrackingScaling.
    required: false
    type: list
    default: []
  describe_auto_scaling_groups:
    description:
      - do you want to describe given asg names I(asg_names)?
    required: false
    type: bool
  describe_auto_scaling_instances:
    description:
      - do you want to describe given instance ids I(instance_ids)?
    required: false
    type: bool
  describe_launch_configurations:
    description:
      - do you want to describe given launch configurations names I(launch_config_names)?
    required: false
    type: bool
  describe_load_balancers:
    description:
      - do you want to describe load balances for given asg name I(asg_name)?
    required: false
    type: bool
  describe_load_balancer_target_groups:
    description:
      - do you want to describe load balances target groups for given asg name I(asg_name)?
    required: false
    type: bool
  describe_notification_configurations:
    description:
      - do you want to describe asg notifications for given group names I(asg_names)?
    required: false
    type: bool
  describe_policies:
    description:
      - do you want to describe asg policies for given asg name I(asg_name) and policy types I(policy_types)?
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
- name: "describe all asgs"
    aws_autoscaling_info:
    describe_auto_scaling_groups: true
    asg_names: []

- name: "describe all asgs instances"
    aws_autoscaling_info:
    describe_auto_scaling_instances: true
    instance_ids: []

- name: "describe all launch configs"
    aws_autoscaling_info:
    describe_launch_configurations: true
    launch_config_names: []

- name: "describe all load balancers related with give asg"
    aws_autoscaling_info:
    describe_load_balancers: true
    asg_name: "test"

- name: "describe all load balancer target groups related with give asg"
    aws_autoscaling_info:
    describe_load_balancer_target_groups: true
    asg_name: "test"

- name: "describe all notifications related to given asgs"
    aws_autoscaling_info:
    describe_notification_configurations: true
    asg_names: []

- name: "describe all asg polices for given asg"
    aws_autoscaling_info:
    describe_policies: true
    asg_name: "test"
    policy_types: []
"""

RETURN = """
auto_scaling_groups:
  description: Describes one or more Auto Scaling groups.
  returned: when `describe_auto_scaling_groups` is defined and success
  type: list
  sample: [
    {
        'auto_scaling_group_name': 'string',
        'auto_scaling_group_arn': 'string',
        'launch_configuration_name': 'string',
        'launch_template': {},
        'mixed_instances_policy': {},
        'min_size': 123,
        'max_size': 123,
        'desired_capacity': 123,
        'default_cooldown': 123,
        'availability_zones': [],
        'load_balancer_names': [],
        'target_group_arns': [],
        'health_check_type': 'string',
        'health_check_grace_period': 123,
        'instances': [],
        'created_time': 'xxxxxxxx',
        'suspended_processes': [],
        'placement_group': 'string',
        'vpc_zone_identifier': 'string',
        'enabled_metrics': [],
        'status': 'string',
        'tags': [],
        'termination_policies': [],
        'new_instances_protected_from_scale_in': True,
        'service_linked_role_arn': 'string',
        'max_instance_lifetime': 123,
        'capacity_rebalance': True
    },
  ]
auto_scaling_instances:
  description: Describes one or more Auto Scaling groups.
  returned: when `describe_auto_scaling_instances` is defined and success
  type: list
  sample: [
    {
        'instance_id': 'string',
        'instance_type': 'string',
        'auto_scaling_group_name': 'string',
        'availability_zone': 'string',
        'lifecycle_state': 'string',
        'health_status': 'string',
        'launch_configuration_name': 'string',
        'launch_template': {},
        'protected_from_scale_in': True,
        'weighted_capacity': 'string'
    },
  ]
launch_configurations:
  description: Describes one or more launch configurations.
  returned: when `describe_launch_configurations` is defined and success
  type: list
  sample: [
    {
        'launch_configuration_name': 'string',
        'launch_configuration_arn': 'string',
        'image_id': 'string',
        'key_name': 'string',
        'security_groups': [],
        'classic_link_vpc_id': 'string',
        'classic_link_vpc_security_groups': [],
        'user_data': 'string',
        'instance_type': 'string',
        'kernel_id': 'string',
        'ramdisk_id': 'string',
        'block_device_mappings': [],
        'instance_monitoring': {},
        'spot_price': 'string',
        'iam_instance_profile': 'string',
        'created_time': 'xxxx',
        'ebs_optimized': True,
        'associate_public_ip_address': True,
        'placement_tenancy': 'string',
        'metadata_options': {}
    }
  ]
load_balancers:
  description: Describes the load balancers for the specified Auto Scaling group.
  returned: when `describe_load_balancers` is defined and success
  type: list
  sample: [
    {
        'load_balancer_name': 'string',
        'state': 'string'
    },
  ]
load_balancer_target_groups:
  description: Describes the target groups for the specified Auto Scaling group.
  returned: when `describe_load_balancer_target_groups` is defined and success
  type: list
  sample: [
    {
        'load_balancer_target_group_arn': 'string',
        'state': 'string'
    },
  ]
notification_configurations:
  description: Describes the notification actions associated with the specified Auto Scaling group.
  returned: when `describe_notification_configurations` is defined and success
  type: list
  sample: [
    {
        'auto_scaling_group_name': 'string',
        'topic_arn': 'string',
        'notification_type': 'string'
    },
  ]
scaling_policies:
  description: Describes the policies for the specified Auto Scaling group.
  returned: when `describe_policies` is defined and success
  type: list
  sample: [
        {
            'auto_scaling_group_name': 'string',
            'policy_name': 'string',
            'policy_arn': 'string',
            'policy_type': 'string',
            'adjustment_type': 'string',
            'min_adjustment_step': 123,
            'min_adjustment_magnitude': 123,
            'scaling_adjustment': 123,
            'cooldown': 123,
            'step_adjustments': [],
            'metric_aggregation_type': 'string',
            'estimated_instance_warmup': 123,
            'alarms': [],
            'target_tracking_configuration': {},
            'enabled': True
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


def _autoscaling(client, module):
    try:
        if module.params['describe_auto_scaling_groups']:
            if client.can_paginate('describe_auto_scaling_groups'):
                paginator = client.get_paginator('describe_auto_scaling_groups')
                return paginator.paginate(
                    AutoScalingGroupNames=module.params['asg_names']
                ), True
            else:
                return client.describe_auto_scaling_groups(
                    AutoScalingGroupNames=module.params['asg_names']
                ), False
        elif module.params['describe_auto_scaling_instances']:
            if client.can_paginate('describe_auto_scaling_instances'):
                paginator = client.get_paginator('describe_auto_scaling_instances')
                return paginator.paginate(
                    InstanceIds=module.params['instance_ids']
                ), True
            else:
                return client.describe_auto_scaling_instances(
                    InstanceIds=module.params['instance_ids']
                ), False
        elif module.params['describe_launch_configurations']:
            if client.can_paginate('describe_launch_configurations'):
                paginator = client.get_paginator('describe_launch_configurations')
                return paginator.paginate(
                    LaunchConfigurationNames=module.params['launch_config_names']
                ), True
            else:
                return client.describe_auto_scaling_instances(
                    LaunchConfigurationNames=module.params['launch_config_names']
                ), False
        elif module.params['describe_load_balancers']:
            if client.can_paginate('describe_load_balancers'):
                paginator = client.get_paginator('describe_load_balancers')
                return paginator.paginate(
                    AutoScalingGroupName=module.params['asg_name']
                ), True
            else:
                return client.describe_load_balancers(
                    AutoScalingGroupName=module.params['asg_name']
                ), False
        elif module.params['describe_load_balancer_target_groups']:
            if client.can_paginate('describe_load_balancer_target_groups'):
                paginator = client.get_paginator('describe_load_balancer_target_groups')
                return paginator.paginate(
                    AutoScalingGroupName=module.params['asg_name']
                ), True
            else:
                return client.describe_load_balancer_target_groups(
                    AutoScalingGroupName=module.params['asg_name']
                ), False
        elif module.params['describe_notification_configurations']:
            if client.can_paginate('describe_notification_configurations'):
                paginator = client.get_paginator('describe_notification_configurations')
                return paginator.paginate(
                    AutoScalingGroupNames=module.params['asg_names']
                ), True
            else:
                return client.describe_notification_configurations(
                    AutoScalingGroupNames=module.params['asg_names']
                ), False
        elif module.params['describe_policies']:
            if client.can_paginate('describe_policies'):
                paginator = client.get_paginator('describe_policies')
                return paginator.paginate(
                    AutoScalingGroupName=module.params['asg_name'],
                    PolicyTypes=module.params['policy_types'],
                ), True
            else:
                return client.describe_policies(
                    AutoScalingGroupName=module.params['asg_name'],
                    PolicyTypes=module.params['policy_types'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws audit manager details')


def main():
    argument_spec = dict(
        asg_names=dict(required=False, type=list, default=[]),
        asg_name=dict(required=False),
        instance_ids=dict(required=False, type=list, default=[]),
        launch_config_names=dict(required=False, type=list, default=[]),
        policy_types=dict(required=False, type=list, default=[]),
        describe_auto_scaling_groups=dict(required=False, type=bool),
        describe_auto_scaling_instances=dict(required=False, type=bool),
        describe_launch_configurations=dict(required=False, type=bool),
        describe_load_balancers=dict(required=False, type=bool),
        describe_load_balancer_target_groups=dict(required=False, type=bool),
        describe_notification_configurations=dict(required=False, type=bool),
        describe_policies=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_auto_scaling_groups', True, ['asg_names']),
            ('describe_auto_scaling_instances', True, ['instance_ids']),
            ('describe_launch_configurations', True, ['launch_config_names']),
            ('describe_load_balancers', True, ['asg_name']),
            ('describe_load_balancer_target_groups', True, ['asg_name']),
            ('describe_notification_configurations', True, ['asg_names']),
            ('describe_policies', True, ['asg_name', 'policy_types']),
        ],
        mutually_exclusive=[
            (
                'describe_auto_scaling_groups',
                'describe_auto_scaling_instances',
                'describe_launch_configurations',
                'describe_load_balancers',
                'describe_load_balancer_target_groups',
                'describe_notification_configurations',
                'describe_policies',
            ),
        ],
    )

    client = module.client('autoscaling', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _autoscaling(client, module)

    if module.params['describe_auto_scaling_groups']:
        module.exit_json(auto_scaling_groups=aws_response_list_parser(paginate, _it, 'AutoScalingGroups'))
    elif module.params['describe_auto_scaling_instances']:
        module.exit_json(auto_scaling_instances=aws_response_list_parser(paginate, _it, 'AutoScalingInstances'))
    elif module.params['describe_launch_configurations']:
        module.exit_json(launch_configurations=aws_response_list_parser(paginate, _it, 'LaunchConfigurations'))
    elif module.params['describe_load_balancers']:
        module.exit_json(load_balancers=aws_response_list_parser(paginate, _it, 'LoadBalancers'))
    elif module.params['describe_load_balancer_target_groups']:
        module.exit_json(load_balancer_target_groups=aws_response_list_parser(paginate, _it, 'LoadBalancerTargetGroups'))
    elif module.params['describe_notification_configurations']:
        module.exit_json(notification_configurations=aws_response_list_parser(paginate, _it, 'NotificationConfigurations'))
    elif module.params['describe_policies']:
        module.exit_json(scaling_policies=aws_response_list_parser(paginate, _it, 'ScalingPolicies'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
