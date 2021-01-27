#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_connections_info
short_description: Get Information about AWS CodeStar Connections.
description:
  - Get Information about AWS CodeStar Connections.
  - U(https://docs.aws.amazon.com/codestar-connections/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  arn:
    description:
      - can be arn of codestar connection?
      - can be arn of codestar host?
    required: false
    type: str
  provider_type_filter:
    description:
      - type of provider.
    required: false
    type: str
    choices: ['Bitbucket', 'GitHub', 'GitHubEnterpriseServer']
    default: 'Bitbucket'
  list_connections:
    description:
      - do you want to get list of codestar connections for given I(provider_type_filter)?
    required: false
    type: bool
  list_hosts:
    description:
      - do you want to get list of codestar hosts?
    required: false
    type: bool
  get_connection:
    description:
      - do you want to get details about codestar connections I(arn)?
    required: false
    type: bool
  get_host:
    description:
      - do you want to get details about codestar host I(arn)?
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
- name: "get list of codestar connections"
  aws_codestar_connections_info:
    list_connections: true
    provider_type_filter: 'Bitbucket'

- name: "get list of codestar hosts"
  aws_codestar_connections_info:
    list_hosts: true

- name: "get detail about connection"
  aws_codestar_connections_info:
    get_connection: true
    arn: 'connection-test-arn'

- name: "get detail about host"
  aws_codestar_connections_info:
    get_host: true
    arn: 'host-test-arn'
"""

RETURN = """
connections:
  description: list of codestar connections.
  returned: when `list_connections` and `provider_type_filter` are defined and success
  type: list
  sample: [
    {
        'connection_name': 'string',
        'connection_arn': 'string',
        'provider_type': 'Bitbucket',
        'owner_account_id': 'string',
        'connection_Status': 'PENDING',
        'host_arn': 'string'
    },
  ]
hosts:
  description: list of codestar hosts.
  returned: when `list_hosts` is defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'hostArn': 'string',
        'provider_type': 'Bitbucket',
        'provider_endpoint': 'string',
        'vpc_configuration': {},
        'status': 'string',
        'statusMessage': 'string'
    },
  ]
connection:
  description: get details about codestar connection.
  returned: when `get_connection` and `arn` are defined and success
  type: dict
  sample: {
    'connection_name': 'string',
    'connection_arn': 'string',
    'provider_type': 'Bitbucket',
    'owner_account_id': 'string',
    'connection_status': 'PENDING',
    'host_arn': 'string'
  }
host:
  description: get details about codestar host.
  returned: when `get_host` and `arn` are defined and success
  type: dict
  sample: {
    'name': 'string',
    'status': 'string',
    'provider_type': 'Bitbucket',
    'provider_endpoint': 'string',
    'vpc_configuration': {}
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _codestar(client, module):
    try:
        if module.params['list_connections']:
            if client.can_paginate('list_connections'):
                paginator = client.get_paginator('list_connections')
                return paginator.paginate(
                    ProviderTypeFilter=module.params['provider_type_filter']
                ), True
            else:
                return client.list_connections(
                    ProviderTypeFilter=module.params['provider_type_filter']
                ), False
        elif module.params['list_hosts']:
            if client.can_paginate('list_hosts'):
                paginator = client.get_paginator('list_hosts')
                return paginator.paginate(), True
            else:
                return client.list_hosts(), False
        elif module.params['get_connection']:
            return client.get_connection(
                ConnectionArn=module.params['arn']
            ), False
        elif module.params['get_host']:
            return client.get_host(
                HostArn=module.params['arn']
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codestar connections details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        provider_type_filter=dict(required=False, choices=['Bitbucket', 'GitHub', 'GitHubEnterpriseServer'], default='Bitbucket'),
        list_connections=dict(required=False, type=bool),
        list_hosts=dict(required=False, type=bool),
        get_connection=dict(required=False, type=bool),
        get_host=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_connection', True, ['arn']),
            ('get_host', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_connections',
                'list_hosts',
                'get_connection',
                'get_host',
            )
        ],
    )

    client = module.client('codestar-connections', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codestar(client, module)

    if module.params['list_connections']:
        module.exit_json(connections=aws_response_list_parser(paginate, _it, 'Connections'))
    elif module.params['list_hosts']:
        module.exit_json(hosts=aws_response_list_parser(paginate, _it, 'Hosts'))
    elif module.params['get_connection']:
        module.exit_json(connection=camel_dict_to_snake_dict(_it['Connection']))
    elif module.params['get_host']:
        module.exit_json(host=camel_dict_to_snake_dict(_it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
