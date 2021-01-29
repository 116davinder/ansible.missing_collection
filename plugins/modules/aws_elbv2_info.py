#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_elbv2_info
short_description: Get Information about Amazon Elastic Load Balancing (Elastic Load Balancing v2).
description:
  - Get Information about Amazon Elastic Load Balancing (Elastic Load Balancing v2).
  - U(https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of pipeline.
    required: false
    type: str
  status:
    description:
      - status of job.
    required: false
    type: str
    choices: ['Submitted', 'Progressing', 'Complete', 'Canceled', 'Error']
    default: 'Submitted'
  list_presets:
    description:
      - do you want to get list of presets?
    required: false
    type: bool
  list_jobs_by_pipeline:
    description:
      - do you want to get list of jobs for given pipeline I(id)?
    required: false
    type: bool
  list_jobs_by_status:
    description:
      - do you want to get list of jobs for given I(status)?
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
- name: "get details of all load balancers"
  aws_elbv2_info:

- name: "get details of given load balancers."
  aws_elbv2_info:
    names: ['test']

- name: "get list of listeners for given elb"
  aws_elbv2_info:
    describe_listeners: true
    arn: 'test-arn-elb'

- name: "get list of listener certificates for given listener arn"
  aws_elbv2_info:
    describe_listener_certificates: true
    arn: 'test-listener-arn'

- name: "get list of rules for given listener arn"
  aws_elbv2_info:
    describe_rules: true
    arn: 'test-listener-arn'

- name: "get list of target groups"
  aws_elbv2_info:
    describe_target_groups: true
"""

RETURN = """
load_balancers:
  description: list of all load balancers.
  returned: when no arguments are defined and success
  type: list
listeners:
  description: list of listeners.
  returned: when `describe_listeners` is defined and success
  type: list
listener_certificates:
  description: list of listener certificates.
  returned: when `describe_listener_certificates` is defined and success
  type: list
rules:
  description: list of rules.
  returned: when `describe_rules` is defined and success
  type: list
target_groups:
  description: list of target groups.
  returned: when `describe_target_groups` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _elbv2(client, module):
    try:
        if module.params['describe_listeners']:
            if client.can_paginate('describe_listeners'):
                paginator = client.get_paginator('describe_listeners')
                return paginator.paginate(
                    LoadBalancerArn=module.params['arn']
                ), True
            else:
                return client.describe_listeners(
                    LoadBalancerArn=module.params['arn']
                ), False
        elif module.params['describe_listener_certificates']:
            if client.can_paginate('describe_listener_certificates'):
                paginator = client.get_paginator('describe_listener_certificates')
                return paginator.paginate(
                    ListenerArn=module.params['arn']
                ), True
            else:
                return client.describe_listener_certificates(
                    ListenerArn=module.params['arn']
                ), False
        elif module.params['describe_rules']:
            if client.can_paginate('describe_rules'):
                paginator = client.get_paginator('describe_rules')
                return paginator.paginate(
                    ListenerArn=module.params['arn']
                ), True
            else:
                return client.describe_rules(
                    ListenerArn=module.params['arn']
                ), False
        elif module.params['describe_target_groups']:
            if client.can_paginate('describe_target_groups'):
                paginator = client.get_paginator('describe_target_groups')
                return paginator.paginate(), True
            else:
                return client.describe_target_groups(), False
        else:
            if client.can_paginate('describe_load_balancers'):
                paginator = client.get_paginator('describe_load_balancers')
                return paginator.paginate(
                    Names=module.params['names']
                ), True
            else:
                return client.describe_load_balancers(
                    Names=module.params['names']
                ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS ElBv2 details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        names=dict(required=False, type=list, default=[]),
        describe_listeners=dict(required=False, type=bool),
        describe_listener_certificates=dict(required=False, type=bool),
        describe_rules=dict(required=False, type=bool),
        describe_target_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_listeners', True, ['arn']),
            ('describe_listener_certificates', True, ['arn']),
            ('describe_rules', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'describe_listeners',
                'describe_listener_certificates',
                'describe_rules',
                'describe_target_groups',
            )
        ],
    )

    client = module.client('elbv2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _elbv2(client, module)

    if module.params['describe_listeners']:
        module.exit_json(listeners=aws_response_list_parser(paginate, it, 'Listeners'))
    elif module.params['describe_listener_certificates']:
        module.exit_json(listener_certificates=aws_response_list_parser(paginate, it, 'Certificates'))
    elif module.params['describe_rules']:
        module.exit_json(rules=aws_response_list_parser(paginate, it, 'Rules'))
    elif module.params['describe_target_groups']:
        module.exit_json(target_groups=aws_response_list_parser(paginate, it, 'TargetGroups'))
    else:
        module.exit_json(load_balancers=aws_response_list_parser(paginate, it, 'LoadBalancers'))


if __name__ == '__main__':
    main()
