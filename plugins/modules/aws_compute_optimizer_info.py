#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_compute_optimizer_info
short_description: Get Information about AWS Compute Optimizer.
description:
  - Get Information about AWS Compute Optimizer.
  - U(https://docs.aws.amazon.com/compute-optimizer/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  get_auto_scaling_group_recommendations:
    description:
      - do you want to get list of auto scaling group recommendations?
    required: false
    type: bool
  get_ebs_volume_recommendations:
    description:
      - do you want to get list of ebs volume recommendations?
    required: false
    type: bool
  get_ec2_instance_recommendations:
    description:
      - do you want to get list of ec2 instance recommendations?
    required: false
    type: bool
  get_lambda_function_recommendations:
    description:
      - do you want to get list of lambda function recommendations?
    required: false
    type: bool
  describe_recommendation_export_jobs:
    description:
      - do you want to get list of export jobs for recommendations?
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
- name: "get status of compute optimizer"
  aws_compute_optimizer_info:

- name: "get list of recommendation for auto scaling group"
  aws_compute_optimizer_info:
    get_auto_scaling_group_recommendations: true

- name: "get list of recommendation for ebs volume"
  aws_compute_optimizer_info:
    get_ebs_volume_recommendations: true

- name: "get list of recommendation for ec2"
  aws_compute_optimizer_info:
    get_ec2_instance_recommendations: true

- name: "get list of recommendation for lambda"
  aws_compute_optimizer_info:
    get_lambda_function_recommendations: true

- name: "get details about all recommendation export jobs"
  aws_compute_optimizer_info:
    describe_recommendation_export_jobs: true
"""

RETURN = """
status:
  description: status of compute optimizer.
  returned: when no argument are defined and success
  type: dict
auto_scaling_group_recommendations:
  description: list of recommendation for auto scaling group.
  returned: when `get_auto_scaling_group_recommendations` is defined and success
  type: list
volume_recommendations:
  description: list of recommendation for ebs volume.
  returned: when `get_ebs_volume_recommendations` is defined and success
  type: list
instance_recommendations:
  description: list of recommendation for ec2.
  returned: when `get_ec2_instance_recommendations` is defined and success
  type: list
lambda_function_recommendations:
  description: list of recommendation for lambda.
  returned: when `get_lambda_function_recommendations` is defined and success
  type: list
recommendation_export_jobs:
  description: details about all recommendation export jobs.
  returned: when `describe_recommendation_export_jobs` is defined and success
  type: list
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


def _compute(client, module):
    try:
        if module.params['get_auto_scaling_group_recommendations']:
            if client.can_paginate('get_auto_scaling_group_recommendations'):
                paginator = client.get_paginator('get_auto_scaling_group_recommendations')
                return paginator.paginate(), True
            else:
                return client.get_auto_scaling_group_recommendations(), False
        elif module.params['get_ebs_volume_recommendations']:
            if client.can_paginate('get_ebs_volume_recommendations'):
                paginator = client.get_paginator('get_ebs_volume_recommendations')
                return paginator.paginate(), True
            else:
                return client.get_ebs_volume_recommendations(), False
        elif module.params['get_ec2_instance_recommendations']:
            if client.can_paginate('get_ec2_instance_recommendations'):
                paginator = client.get_paginator('get_ec2_instance_recommendations')
                return paginator.paginate(), True
            else:
                return client.get_ec2_instance_recommendations(), False
        elif module.params['get_lambda_function_recommendations']:
            if client.can_paginate('get_lambda_function_recommendations'):
                paginator = client.get_paginator('get_lambda_function_recommendations')
                return paginator.paginate(), True
            else:
                return client.get_lambda_function_recommendations(), False
        elif module.params['describe_recommendation_export_jobs']:
            if client.can_paginate('describe_recommendation_export_jobs'):
                paginator = client.get_paginator('describe_recommendation_export_jobs')
                return paginator.paginate(), True
            else:
                return client.describe_recommendation_export_jobs(), False
        else:
            return client.get_enrollment_status(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws compute optimizer details')


def main():
    argument_spec = dict(
        get_auto_scaling_group_recommendations=dict(required=False, type=bool),
        get_ebs_volume_recommendations=dict(required=False, type=bool),
        get_ec2_instance_recommendations=dict(required=False, type=bool),
        get_lambda_function_recommendations=dict(required=False, type=bool),
        describe_recommendation_export_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(),
        mutually_exclusive=[
            (
                'get_auto_scaling_group_recommendations',
                'get_ebs_volume_recommendations',
                'get_ec2_instance_recommendations',
                'get_lambda_function_recommendations',
                'describe_recommendation_export_jobs',
            )
        ],
    )

    client = module.client('compute-optimizer', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _compute(client, module)

    if module.params['get_auto_scaling_group_recommendations']:
        module.exit_json(auto_scaling_group_recommendations=aws_response_list_parser(paginate, _it, 'autoScalingGroupRecommendations'))
    elif module.params['get_ebs_volume_recommendations']:
        module.exit_json(volume_recommendations=aws_response_list_parser(paginate, _it, 'volumeRecommendations'))
    elif module.params['get_ec2_instance_recommendations']:
        module.exit_json(instance_recommendations=aws_response_list_parser(paginate, _it, 'instanceRecommendations'))
    elif module.params['get_lambda_function_recommendations']:
        module.exit_json(lambda_function_recommendations=aws_response_list_parser(paginate, _it, 'lambdaFunctionRecommendations'))
    elif module.params['describe_recommendation_export_jobs']:
        module.exit_json(recommendation_export_jobs=aws_response_list_parser(paginate, _it, 'recommendationExportJobs'))
    else:
        module.exit_json(status=camel_dict_to_snake_dict(_it))


if __name__ == '__main__':
    main()
