#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cognito_identity_info
short_description: Get Information about Amazon Cognito Identity.
description:
  - Get Information about Amazon Cognito Identity.
  - U(https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  id:
    description:
      - can be cognito identity pool id.
      - can be cognito identity id.
    required: false
    type: str
  list_identities:
    description:
      - do you want to get list of cognito identities for given pool I(id)?
    required: false
    type: bool
  describe_identity_pool:
    description:
      - do you want to get details of cognito identity pool for given I(id)?
    required: false
    type: bool
  describe_identity:
    description:
      - do you want to get details of cognito identity for given I(id)?
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
- name: "get list of cognito identity pools"
  aws_cognito_identity_info:

- name: "get list of cognito identities for given pool"
  aws_cognito_identity_info:
    list_identities: true
    id: 'test-pool-id'

- name: "get details about cognito identity pool"
  aws_cognito_identity_info:
    describe_identity_pool: true
    id: 'test-pool-id'

- name: "get details about cognito identity"
  aws_cognito_identity_info:
    describe_identity: true
    id: 'test-identity-id'
"""

RETURN = """
pools:
  description: get list of cognito identity pools.
  returned: when no argument and success
  type: list
  sample: [
    {
        'identity_pool_id': 'string',
        'identity_pool_name': 'string'
    },
  ]
identities:
  description: get list of cognito identities.
  returned: when `list_identities` and `id` are defined and success
  type: list
  sample: [
    {
        'identity_id': 'string',
        'logins': [
            'string',
        ],
        'creation_date': datetime(2015, 1, 1),
        'last_modified_date': datetime(2016, 6, 6)
    },
  ]
pool:
  description: get details of identity pool.
  returned: when `describe_identity_pool` and `id` are defined and success
  type: dict
  sample: {
    'identity_pool_id': 'string',
    'identity_pool_name': 'string',
    'allow_unauthenticated_identities': True,
    'allow_classic_flow': True,
    'supported_login_providers': {
        'string': 'string'
    },
    'developer_provider_name': 'string',
    'open_id_connect_provider_arns': [
        'string',
    ],
    'cognito_identity_providers': [
        {
            'provider_name': 'string',
            'client_id': 'string',
            'serverS_side_token_check': True|False
        },
    ],
    'saml_provider_arns': [
        'string',
    ],
    'identity_pool_tags': {
        'string': 'string'
    }
  }
identity:
  description: get details of identity.
  returned: when `describe_identity` and `id` are defined and success
  type: dict
  sample: {
    'identity_id': 'string',
    'logins': [
        'string',
    ],
    'creation_date': datetime(2015, 1, 1),
    'last_modified_date': datetime(2016, 6, 6)
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


def _cognito(client, module):
    try:
        if module.params['list_identities']:
            if client.can_paginate('list_identities'):
                paginator = client.get_paginator('list_identities')
                return paginator.paginate(
                    IdentityPoolId=module.params['id'],
                    MaxResults=100,
                ), True
            else:
                return client.list_identities(
                    IdentityPoolId=module.params['id'],
                    MaxResults=100,
                ), False
        elif module.params['describe_identity_pool']:
            return client.describe_identity_pool(
                IdentityPoolId=module.params['id'],
            ), False
        elif module.params['describe_identity']:
            return client.describe_identity(
                IdentityId=module.params['id']
            ), False
        else:
            if client.can_paginate('list_identity_pools'):
                paginator = client.get_paginator('list_identity_pools')
                return paginator.paginate(
                    MaxResults=60,
                ), True
            else:
                return client.list_identity_pools(
                    MaxResults=60,
                ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cognito identity details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        list_identities=dict(required=False, type=bool),
        describe_identity_pool=dict(required=False, type=bool),
        describe_identity=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_identities', True, ['id']),
            ('describe_identity_pool', True, ['id']),
            ('describe_identity', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_identities',
                'describe_identity_pool',
                'describe_identity',
            )
        ],
    )

    client = module.client('cognito-identity', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cognito(client, module)

    if module.params['list_identities']:
        module.exit_json(identities=aws_response_list_parser(paginate, _it, 'Identities'))
    elif module.params['describe_identity_pool']:
        module.exit_json(pool=camel_dict_to_snake_dict(_it))
    elif module.params['describe_identity']:
        module.exit_json(identity=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(pools=aws_response_list_parser(paginate, _it, 'IdentityPools'))


if __name__ == '__main__':
    main()
