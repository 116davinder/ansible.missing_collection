#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: aws_api_gateway_management_api_info
short_description: Get details about Amazon API Gateway Management API.
description:
  - Get Information about Amazon API Gateway Management API.
  - U(https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-how-to-call-websocket-api-connections.html)
version_added: 0.0.2
options:
  connection_id:
    description:
      - connection id of api gateway management api.
    required: false
    type: str
  get_connection:
    description:
      - do you want to fetch details about given I(connection_id)?
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
  aws_api_gateway_management_api_info:
    connection_id: 'test'
    get_connection: true
"""

RETURN = """
connection:
  description: details about given connection id.
  returned: when `get_connection` and `connection_id` and success
  type: dict
  sample: {
    'connected_at': datetime(2017, 7, 7),
    'identity': {
        'source_ip': 'string',
        'user_agent': 'string'
    },
    'last_acctive_at': datetime(2015, 1, 1)
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import (
    camel_dict_to_snake_dict,
)
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def _apigatewaymanagementapi(client, module):
    try:
        if module.params["get_connection"]:
            return (
                client.get_connection(ConnectionId=module.params["connection_id"]),
                False,
            )
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(
            e, msg="Failed to fetch aws api gateway management api details"
        )


def main():
    argument_spec = dict(
        connection_id=dict(required=False),
        get_connection=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[("get_connection", True, ["connection_id"])],
        mutually_exclusive=[],
    )

    _gateway = module.client(
        "apigatewaymanagementapi", retry_decorator=AWSRetry.exponential_backoff()
    )
    _it, _ = _apigatewaymanagementapi(_gateway, module)

    if module.params["get_connection"]:
        module.exit_json(connection=camel_dict_to_snake_dict(_it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == "__main__":
    main()
