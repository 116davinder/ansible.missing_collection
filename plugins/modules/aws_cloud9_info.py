#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloud9_info
short_description: Get details about AWS Cloud9 Environments.
description:
  - Get Information about AWS Cloud9 Environments.
  - U(https://docs.aws.amazon.com/cloud9/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  environment_id:
    description:
      - environment id of cloud9.
    required: false
    type: str
    aliases: ['id']
  environment_ids:
    description:
      - list of cloud9 environment ids.
    required: false
    type: list
  describe_environments:
    description:
      - do you want to describe cloud9 I(environment_ids) environments?
    required: false
    type: bool
  describe_environment_status:
    description:
      - do you want to describe status of cloud9 I(environment_id) environment?
    required: false
    type: bool
  describe_environment_memberships:
    description:
      - do you want to describe membership of cloud9 I(environment_id) environment?
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
- name: "list of all environment ids"
  aws_cloud9_info:

- name: "Gets information about AWS Cloud9 development environments."
  aws_cloud9_info:
    environment_ids: ['test']
    describe_environments: true

- name: "Gets information about AWS Cloud9 development environment status"
  aws_cloud9_info:
    environment_id: 'test'
    describe_environment_status: true

- name: "Gets information about AWS Cloud9 development environment memeberships"
  aws_cloud9_info:
    environment_id: 'test'
    describe_environment_memberships: true
"""

RETURN = """
environment_ids:
  description: Gets a list of AWS Cloud9 development environment identifiers.
  returned: when no argument and success
  type: list
  sample: [ 'string', ]
environments:
  description: Gets information about AWS Cloud9 development environments.
  returned: when `describe_environments` and `environment_ids` are defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'name': 'string',
          'description': 'string',
          'type': 'ssh',
          'connection_type': 'CONNECT_SSH',
          'arn': 'string',
          'owner_arn': 'string',
          'lifecycle': {
              'status': 'CREATING',
              'reason': 'string',
              'failure_resource': 'string'
          }
      },
  ]
status:
  description: Gets status information for an AWS Cloud9 development environment.
  returned: when `describe_environment_status` and `environment_id` are defined and success
  type: dict
  sample: {
    'status': 'creating',
    'message': 'string'
  }
memberships:
  description: Gets information about environment members for an AWS Cloud9 development environment.
  returned: when `describe_environment_memberships` and `environment_id` are defined and success
  type: list
  sample: [
      {
          'permissions': 'owner',
          'user_id': 'string',
          'user_arn': 'string',
          'environment_id': 'string',
          'last_access': datetime(2015, 1, 3)
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


def _cloud9(client, module):
    try:
        if module.params['describe_environments']:
            if client.can_paginate('describe_environments'):
                paginator = client.get_paginator('describe_environments')
                return paginator.paginate(
                    environmentIds=module.params['environment_ids']
                ), True
            else:
                return client.describe_environments(
                    environmentIds=module.params['environment_ids']
                ), False
        elif module.params['describe_environment_status']:
            if client.can_paginate('describe_environment_status'):
                paginator = client.get_paginator('describe_environment_status')
                return paginator.paginate(
                    environmentId=module.params['environment_id']
                ), True
            else:
                return client.describe_environment_status(
                    environmentId=module.params['environment_id']
                ), False
        elif module.params['describe_environment_memberships']:
            if client.can_paginate('describe_environment_memberships'):
                paginator = client.get_paginator('describe_environment_memberships')
                return paginator.paginate(
                    environmentId=module.params['environment_id']
                ), True
            else:
                return client.describe_environment_memberships(
                    environmentId=module.params['environment_id']
                ), False
        else:
            if client.can_paginate('list_environments'):
                paginator = client.get_paginator('list_environments')
                return paginator.paginate(), True
            else:
                return client.list_environments(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloud9 details')


def main():
    argument_spec = dict(
        environment_id=dict(required=False, aliases=['id']),
        environment_ids=dict(required=False, type=list),
        describe_environments=dict(required=False, type=bool),
        describe_environment_status=dict(required=False, type=bool),
        describe_environment_memberships=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_environments', True, ['environment_ids']),
            ('describe_environment_status', True, ['environment_id']),
            ('describe_environment_memberships', True, ['environment_id']),
        ],
        mutually_exclusive=[
            (
                'describe_environments',
                'describe_environment_status',
                'describe_environment_memberships'
            )
        ],
    )

    client = module.client('cloud9', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloud9(client, module)

    if module.params['describe_environments']:
        module.exit_json(environments=aws_response_list_parser(paginate, _it, 'environments'))
    elif module.params['describe_environment_status']:
        module.exit_json(status=camel_dict_to_snake_dict(_it))
    elif module.params['describe_environment_memberships']:
        module.exit_json(memberships=aws_response_list_parser(paginate, _it, 'memberships'))
    else:
        module.exit_json(environment_ids=aws_response_list_parser(paginate, _it, 'environmentIds'))


if __name__ == '__main__':
    main()
