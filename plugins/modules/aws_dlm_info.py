#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dlm_info
short_description: Get Information about Amazon Data Lifecycle Manager.
description:
  - Get Information about Amazon Data Lifecycle Manager.
  - U(https://docs.aws.amazon.com/dlm/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  id:
    description:
      - id of the policy.
    required: false
    type: str
  state:
    description:
      - state of policy.
    required: false
    type: str
    choices: ['ENABLED', 'DISABLED', 'ERROR']
    default: 'ENABLED'
  resource_types:
    description:
      - list of resource types.
    required: false
    type: list
  get_lifecycle_policy:
    description:
      - do you want to get details about given I(id)?
    required: false
    type: bool
  get_lifecycle_policies:
    description:
      - do you want to get details about given I(state) and I(resource_types)?
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
- name: "Gets detailed information about the specified lifecycle policy."
  aws_dlm_info:
    get_lifecycle_policy: true
    id: 'test-id'

- name: "Gets summary information about all or the specified data lifecycle policies."
  aws_dlm_info:
    get_lifecycle_policies: true
    state: 'ENABLED'
    resource_types: ['VOLUME']
"""

RETURN = """
policy:
  description: detailed information about the specified lifecycle policy.
  returned: when `get_lifecycle_policy` and `id` are defined and success
  type: dict
  sample: {
    'policy_id': 'string',
    'description': 'string',
    'state': 'ENABLED',
    'status_message': 'string',
    'execution_role_arn': 'string',
    'date_created': datetime(2015, 1, 1),
    'date_modified': datetime(2016, 6, 6),
    'policy_details': {
        'policy_type': 'EBS_SNAPSHOT_MANAGEMENT',
        'resource_types': [
            'VOLUME',
        ],
        'target_tags': [],
        'schedules': [],
        'parameters': {},
        'eventSource': {},
        'actions': []
    },
    'tags': {
        'string': 'string'
    },
    'policy_arn': 'string'
  }
policies:
  description: summary information about all or the specified data lifecycle policies.
  returned: when `get_lifecycle_policies`, `state`, and `resource_types` are defined and success
  type: list
  sample: [
    {
        'policy_id': 'string',
        'description': 'string',
        'state': 'ENABLED',
        'tags': {
            'string': 'string'
        },
        'policy_type': 'EBS_SNAPSHOT_MANAGEMENT'
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
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _dlm(client, module):
    try:
        if module.params['get_lifecycle_policy']:
            return client.get_lifecycle_policy(
                PolicyId=module.params['id']
            ), False
        elif module.params['get_lifecycle_policies']:
            if client.can_paginate('get_lifecycle_policies'):
                paginator = client.get_paginator('get_lifecycle_policies')
                return paginator.paginate(
                    State=module.params['state'],
                    ResourceTypes=module.params['resource_types'],
                ), True
            else:
                return client.get_lifecycle_policies(
                    State=module.params['state'],
                    ResourceTypes=module.params['resource_types'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS DLM details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        state=dict(required=False, choices=['ENABLED', 'DISABLED', 'ERROR'], default='ENABLED'),
        resource_types=dict(required=False, type=list),
        get_lifecycle_policy=dict(required=False, type=bool),
        get_lifecycle_policies=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_lifecycle_policy', True, ['id']),
            ('get_lifecycle_policies', True, ['resource_types']),
        ),
        mutually_exclusive=[
            (
                'get_lifecycle_policy',
                'get_lifecycle_policies',
            )
        ],
    )

    client = module.client('dlm', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _dlm(client, module)

    if module.params['get_lifecycle_policy']:
        module.exit_json(policy=camel_dict_to_snake_dict(it['Policy']))
    elif module.params['get_lifecycle_policies']:
        module.exit_json(policies=aws_response_list_parser(paginate, it, 'Policies'))
    else:
        module.fail_json_aws("unknown options are passed")


if __name__ == '__main__':
    main()
