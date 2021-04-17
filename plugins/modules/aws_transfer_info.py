#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_transfer_info
short_description: Get Information about AWS Transfer Family.
description:
  - Get Information about AWS Transfer Family.
  - U(https://docs.aws.amazon.com/transfer/latest/userguide/API_Operations.html)
version_added: 0.1.0
options:
  server_id:
    description:
      - system-assigned unique identifier for a server that has users assigned to it.
    required: false
    type: str
  list_security_policies:
    description:
      - do you want to get list of security_policies?
    required: false
    type: bool
  list_servers:
    description:
      - do you want to get servers?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get list of users for given I(server_id)?
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
- name: "get list of security_policies"
  aws_transfer_info:
    list_security_policies: true

- name: "get servers"
  aws_transfer_info:
    list_servers: true

- name: "get list of users"
  aws_transfer_info:
    list_users: true
    server_id: 'test'
"""

RETURN = """
security_policies:
  description: list of security_policies.
  returned: when `list_security_policies` is defined and success.
  type: list
servers:
  description: list of servers.
  returned: when `list_servers` is defined and success.
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


def _transfer(client, module):
    try:
        if module.params['list_security_policies']:
            if client.can_paginate('list_security_policies'):
                paginator = client.get_paginator('list_security_policies')
                return paginator.paginate(), True
            else:
                return client.list_security_policies(), False
        elif module.params['list_servers']:
            if client.can_paginate('list_servers'):
                paginator = client.get_paginator('list_servers')
                return paginator.paginate(), True
            else:
                return client.list_servers(), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    ServerId=module.params['server_id'],
                ), True
            else:
                return client.list_users(
                    ServerId=module.params['server_id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Transfer Family details')


def main():
    argument_spec = dict(
        server_id=dict(required=False),
        list_security_policies=dict(required=False, type=bool),
        list_servers=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_users', True, ['server_id']),
        ),
        mutually_exclusive=[
            (
                'list_security_policies',
                'list_servers',
                'list_users',
            )
        ],
    )

    client = module.client('transfer', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _transfer(client, module)

    if module.params['list_security_policies']:
        module.exit_json(security_policies=aws_response_list_parser(paginate, it, 'SecurityPolicyNames'))
    elif module.params['list_servers']:
        module.exit_json(servers=aws_response_list_parser(paginate, it, 'Servers'))
    elif module.params['list_users']:
        module.exit_json(users=aws_response_list_parser(paginate, it, 'Users'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
