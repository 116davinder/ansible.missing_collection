#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_api_gateway_management_api
short_description: Manage Resources of Amazon API Gateway Management API.
description:
  - Manage Resources of Amazon API Gateway Management API.
  - U(https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html)
version_added: 0.0.2
options:
  connection_id:
    description:
      - connection id of api gateway management api.
    required: false
    type: str
  delete_connection:
    description:
      - do you want to delete given I(connection_id)?
    required: false
    type: bool
  data:
    description:
      - data
    required: false
    type: bytes
  post_to_connection:
    description:
      - do you want to delete given I(connection_id) and I(data)?
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
- name: "details about given connection id"
  aws_api_gateway_management_api:
    connection_id: 'test'
    delete_connection: true

- name: "send data to given connection id"
  aws_api_gateway_management_api:
    connection_id: 'test'
    data: "<bytes>"
    post_to_connection: true
"""

RETURN = """
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def _apigatewaymanagementapi(client, module):
    try:
        if module.params['delete_connection']:
            client.delete_connection(
                ConnectionId=module.params['connection_id']
            )
            module.exit_json(msg="connection got deleted")
        elif module.params['post_to_connection']:
            client.post_to_connection(
                ConnectionId=module.params['connection_id'],
                Data=module.params['data']
            )
            module.exit_json(msg="data sent to specified connection id")
        else:
            module.fail_json("unknown options are passed")
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws api gateway management api details')


def main():
    argument_spec = dict(
        connection_id=dict(required=False),
        delete_connection=dict(required=False, type=bool),
        data=dict(required=False, type=bytes),
        post_to_connection=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('delete_connection', True, ['connection_id']),
            ('post_to_connection', True, ['connection_id', 'data'])
        ],
        mutually_exclusive=[
            (
                'delete_connection',
                'post_to_connection'
            )
        ],
    )

    _gateway = module.client('apigatewaymanagementapi', retry_decorator=AWSRetry.exponential_backoff())
    _apigatewaymanagementapi(_gateway, module)


if __name__ == '__main__':
    main()
