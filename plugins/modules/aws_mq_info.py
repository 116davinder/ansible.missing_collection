#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mq_info
short_description: Get Information about Amazon MQ.
description:
  - Get Information about Amazon MQ.
  - U(https://docs.aws.amazon.com/amazon-mq/latest/api-reference/resources.html)
version_added: 0.0.7
options:
  id:
    description:
      - broker id.
    required: false
    type: str
    aliases: ['broker_id']
  list_brokers:
    description:
      - do you want to get list of brokers?
    required: false
    type: bool
  list_configurations:
    description:
      - do you want to get configurations?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get list of users for given broker I(id)?
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
- name: "get list of brokers"
  aws_mq_info:
    list_brokers: true

- name: "get configurations"
  aws_mq_info:
    list_configurations: true

- name: "get list of users"
  aws_mq_info:
    list_users: true
    id: 'broker_id'
"""

RETURN = """
brokers:
  description: list of brokers.
  returned: when `list_brokers` is defined and success.
  type: list
configurations:
  description: get of configurations.
  returned: when `list_configurations` is defined and success.
  type: list
users:
  description: list of users.
  returned: when `list_users` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mq(client, module):
    try:
        if module.params['list_brokers']:
            if client.can_paginate('list_brokers'):
                paginator = client.get_paginator('list_brokers')
                return paginator.paginate(), True
            else:
                return client.list_brokers(), False
        elif module.params['list_configurations']:
            if client.can_paginate('list_configurations'):
                paginator = client.get_paginator('list_configurations')
                return paginator.paginate(), True
            else:
                return client.list_configurations(), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    BrokerId=module.params['id']
                ), True
            else:
                return client.list_users(
                    BrokerId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental MQ details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['broker_id']),
        list_brokers=dict(required=False, type=bool),
        list_configurations=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_users', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_brokers',
                'list_configurations',
                'list_users',
            )
        ],
    )

    client = module.client('mq', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mq(client, module)

    if module.params['list_brokers']:
        module.exit_json(brokers=aws_response_list_parser(paginate, it, 'BrokerSummaries'))
    elif module.params['list_configurations']:
        module.exit_json(configurations=aws_response_list_parser(paginate, it, 'Configurations'))
    elif module.params['list_users']:
        module.exit_json(users=aws_response_list_parser(paginate, it, 'Users'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
