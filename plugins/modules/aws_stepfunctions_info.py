#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_stepfunctions_info
short_description: Get Information about AWS Step Functions (SFN).
description:
  - Get Information about AWS Step Functions (SFN).
  - U(https://docs.aws.amazon.com/step-functions/latest/apireference/API_Operations.html)
version_added: 0.0.9
options:
  arn:
    description:
      - arn of the state machine.
    required: false
    type: str
    aliases: ['state_machine_arn']
  status_filter:
    description:
      - filter to list executions?
    required: false
    type: str
    choices: ['RUNNING', 'SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']
    default: 'RUNNING'
  list_activities:
    description:
      - do you want to get list of activities?
    required: false
    type: bool
  list_executions:
    description:
      - do you want to get executions for given I(arn) and I(status_filter)?
    required: false
    type: bool
  list_state_machines:
    description:
      - do you want to get list of state_machines?
    type: bool
  describe_state_machine:
    description:
      - do you want to get state_machine for given I(arn)?
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
- name: "get list of activities"
  aws_stepfunctions_info:
    list_activities: true

- name: "get executions"
  aws_stepfunctions_info:
    list_executions: true
    arn: 'state_machine_arn'
    status_filter: 'RUNNING'

- name: "get list of state_machines"
  aws_stepfunctions_info:
    list_state_machines: true

- name: "get state_machine details"
  aws_stepfunctions_info:
    describe_state_machine: true
    arn: 'state_machine_arn'
"""

RETURN = """
activities:
  description: list of activities.
  returned: when `list_activities` is defined and success.
  type: list
executions:
  description: list of executions.
  returned: when `list_executions` is defined and success.
  type: list
state_machines:
  description: list of state_machines.
  returned: when `list_state_machines` is defined and success.
  type: list
state_machine:
  description: get details of state_machine.
  returned: when `describe_state_machine` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _stepfunctions(client, module):
    try:
        if module.params['list_activities']:
            if client.can_paginate('list_activities'):
                paginator = client.get_paginator('list_activities')
                return paginator.paginate(), True
            else:
                return client.list_activities(), False
        elif module.params['list_executions']:
            if client.can_paginate('list_executions'):
                paginator = client.get_paginator('list_executions')
                return paginator.paginate(
                    stateMachineArn=module.params['arn'],
                    statusFilter=module.params['status_filter']
                ), True
            else:
                return client.list_executions(
                    stateMachineArn=module.params['arn'],
                    statusFilter=module.params['status_filter']
                ), False
        elif module.params['list_state_machines']:
            if client.can_paginate('list_state_machines'):
                paginator = client.get_paginator('list_state_machines')
                return paginator.paginate(), True
            else:
                return client.list_state_machines(), False
        elif module.params['describe_state_machine']:
            if client.can_paginate('describe_state_machine'):
                paginator = client.get_paginator('describe_state_machine')
                return paginator.paginate(
                    stateMachineArn=module.params['arn'],
                ), True
            else:
                return client.describe_state_machine(
                    stateMachineArn=module.params['arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Step Functions (SFN) details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['state_machine_arn']),
        status_filter=dict(
            required=False,
            choices=['RUNNING', 'SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED'],
            default='RUNNING'
        ),
        list_activities=dict(required=False, type=bool),
        list_executions=dict(required=False, type=bool),
        list_state_machines=dict(required=False, type=bool),
        describe_state_machine=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_executions', True, ['arn']),
            ('describe_state_machine', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_activities',
                'list_executions',
                'list_state_machines',
                'describe_state_machine',
            )
        ],
    )

    client = module.client('stepfunctions', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _stepfunctions(client, module)

    if module.params['list_activities']:
        module.exit_json(activities=aws_response_list_parser(paginate, it, 'activities'))
    elif module.params['list_executions']:
        module.exit_json(executions=aws_response_list_parser(paginate, it, 'executions'))
    elif module.params['list_state_machines']:
        module.exit_json(state_machines=aws_response_list_parser(paginate, it, 'stateMachines'))
    elif module.params['describe_state_machine']:
        module.exit_json(state_machine=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
