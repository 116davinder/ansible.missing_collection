#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cognito_idp_info
short_description: Get Information about Amazon Cognito Identity Provider.
description:
  - Get Information about Amazon Cognito Identity Provider.
  - U(https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  access_token:
    description:
      - access token for cognito devices.
    required: false
    type: str
  user_pool_id:
    description:
      - cognito user pool id.
    required: false
    type: str
  group_name:
    description:
      - cognito group name.
    required: false
    type: str
  list_devices:
    description:
      - do you want to get list of devices for given access token I(access_token)?
    required: false
    type: bool
  list_groups:
    description:
      - do you want to get list of cognito groups for given I(user_pool_id)?
    required: false
    type: bool
  list_identity_providers:
    description:
      - do you want to get list of cognito identity providers for given I(user_pool_id)?
    required: false
    type: bool
  list_resource_servers:
    description:
      - do you want to get list of cognito resource servers for given I(user_pool_id)?
    required: false
    type: bool
  list_user_import_jobs:
    description:
      - do you want to get list of cognito user import jobs for given I(user_pool_id)?
    required: false
    type: bool
  list_user_pool_clients:
    description:
      - do you want to get list of cognito user pool clients for given I(user_pool_id)?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get list of cognito users for given I(user_pool_id)?
    required: false
    type: bool
  list_users_in_group:
    description:
      - do you want to get list of cognito groups for given I(user_pool_id) and I(group_name)?
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
- name: "get list of cognito user pools"
  aws_cognito_idp_info:

- name: "get list of cognito devices"
  aws_cognito_idp_info:
    list_devices: true
    access_token: 'test'

- name: "get list of cognito user groups"
  aws_cognito_idp_info:
    list_groups: true
    user_pool_id: 'test'

- name: "get list of cognito providers"
  aws_cognito_idp_info:
    list_identity_providers: true
    user_pool_id: 'test'

- name: "get list of cognito resource servers"
  aws_cognito_idp_info:
    list_resource_servers: true
    user_pool_id: 'test'

- name: "get list of cognito import jobs"
  aws_cognito_idp_info:
    list_user_import_jobs: true
    user_pool_id: 'test'

- name: "get list of cognito user pool clients"
  aws_cognito_idp_info:
    list_user_pool_clients: true
    user_pool_id: 'test'

- name: "get list of cognito users in a pool"
  aws_cognito_idp_info:
    list_users: true
    user_pool_id: 'test'

- name: "get list of cognito users in group"
  aws_cognito_idp_info:
    list_users_in_group: true
    user_pool_id: 'test'
    group_name: 'test-group'
"""

RETURN = """
user_pools:
  description: get list of cognito user pools.
  returned: when no argument and success
  type: list
  sample: [
    {
        'id': 'string',
        'name': 'string',
        'lambda_config': {},
        'status': 'Enabled',
        'last_modified_date': datetime(2015, 1, 1),
        'creation_date': datetime(2016, 6, 6)
    },
  ]
devices:
  description: get list of devices.
  returned: when `list_devices` and `access_token` are defined and success
  type: list
  sample: [
    {
        'device_key': 'string',
        'device_attributes': [],
        'device_create_date': datetime(2016, 6, 6),
        'device_last_modified_date': datetime(2017, 7, 7),
        'device_last_authenticated_date': datetime(2015, 1, 1)
    },
  ]
groups:
  description: get list of groups.
  returned: when `list_groups` and `user_pool_id` are defined and success
  type: list
  sample: [
    {
        'group_name': 'string',
        'user_pool_id': 'string',
        'description': 'string',
        'role_arn': 'string',
        'precedence': 123,
        'last_modified_date': datetime(2015, 1, 1),
        'creation_date': datetime(2016, 6, 6)
    },
]
providers:
  description: get list of providers.
  returned: when `list_identity_providers` and `user_pool_id` are defined and success
  type: list
  sample: [
    {
        'provider_name': 'string',
        'provider_type': 'SAML',
        'last_modified_date': datetime(2015, 1, 1),
        'creation_date': datetime(2016, 6, 6)
    },
  ]
resource_servers:
  description: get list of resource servers.
  returned: when `list_resource_servers` and `user_pool_id` are defined and success
  type: list
  sample: [
    {
        'user_pool_id': 'string',
        'identifier': 'string',
        'name': 'string',
        'scopes': [
            {
                'scope_name': 'string',
                'scope_description': 'string'
            },
        ]
    },
  ]
user_import_jobs:
  description: get list of user import jobs.
  returned: when `list_user_import_jobs` and `user_pool_id` are defined and success
  type: list
  sample: [
    {
        'job_name': 'string',
        'job_id': 'string',
        'user_pool_id': 'string',
        'pre_signed_url': 'string',
        'creation_date': datetime(2016, 6, 6),
        'startDate': datetime(2017, 7, 7),
        'completion_date': datetime(2015, 1, 1),
        'status': 'Created',
        'cloud_watch_logs_role_arn': 'string',
        'imported_users': 1234,
        'skipped_users': 12345,
        'failed_users': 123,
        'completion_message': 'string'
    },
  ]
user_pool_clients:
  description: get list of user pool clients.
  returned: when `list_user_pool_clients` and `user_pool_id` are defined and success
  type: list
  sample: [
    {
        'client_id': 'string',
        'user_pool_id': 'string',
        'client_name': 'string'
    },
  ]
users:
  description: get list of users.
  returned: when `list_users` or `list_users_in_group` with `user_pool_id` and `group_name` are defined and success
  type: list
  sample: [
    {
        'username': 'string',
        'attributes': [],
        'user_create_date': datetime(2016, 6, 6),
        'user_last_modified_date': datetime(2015, 1, 1),
        'enabled': True,
        'user_status': 'UNCONFIRMED',
        'mfs_options': []
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _cognito(client, module):
    try:
        if module.params['list_devices']:
            if client.can_paginate('list_devices'):
                paginator = client.get_paginator('list_devices')
                return paginator.paginate(
                    AccessToken=module.params['access_token'],
                ), True
            else:
                return client.list_devices(
                    AccessToken=module.params['access_token'],
                ), False
        elif module.params['list_groups']:
            if client.can_paginate('list_groups'):
                paginator = client.get_paginator('list_groups')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                ), True
            else:
                return client.list_groups(
                    UserPoolId=module.params['user_pool_id'],
                ), False
        elif module.params['list_identity_providers']:
            if client.can_paginate('list_identity_providers'):
                paginator = client.get_paginator('list_identity_providers')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                ), True
            else:
                return client.list_identity_providers(
                    UserPoolId=module.params['user_pool_id'],
                ), False
        elif module.params['list_resource_servers']:
            if client.can_paginate('list_resource_servers'):
                paginator = client.get_paginator('list_resource_servers')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                    MaxResults=50           # hard limit from AWS
                ), True
            else:
                return client.list_resource_servers(
                    UserPoolId=module.params['user_pool_id'],
                    MaxResults=50           # hard limit from AWS
                ), False
        elif module.params['list_user_import_jobs']:
            if client.can_paginate('list_user_import_jobs'):
                paginator = client.get_paginator('list_user_import_jobs')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                    MaxResults=60           # hard limit from AWS
                ), True
            else:
                return client.list_user_import_jobs(
                    UserPoolId=module.params['user_pool_id'],
                    MaxResults=60           # hard limit from AWS
                ), False
        elif module.params['list_user_pool_clients']:
            if client.can_paginate('list_user_pool_clients'):
                paginator = client.get_paginator('list_user_pool_clients')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                ), True
            else:
                return client.list_user_pool_clients(
                    UserPoolId=module.params['user_pool_id'],
                ), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                ), True
            else:
                return client.list_users(
                    UserPoolId=module.params['user_pool_id'],
                ), False
        elif module.params['list_users_in_group']:
            if client.can_paginate('list_users_in_group'):
                paginator = client.get_paginator('list_users_in_group')
                return paginator.paginate(
                    UserPoolId=module.params['user_pool_id'],
                    GroupName=module.params['group_name']
                ), True
            else:
                return client.list_users_in_group(
                    UserPoolId=module.params['user_pool_id'],
                    GroupName=module.params['group_name']
                ), False
        else:
            if client.can_paginate('list_user_pools'):
                paginator = client.get_paginator('list_user_pools')
                return paginator.paginate(
                    MaxResults=60       # hard limit from AWS
                ), True
            else:
                return client.list_user_pools(
                    MaxResults=60       # hard limit from AWS
                ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cognito idp details')


def main():
    argument_spec = dict(
        user_pool_id=dict(required=False),
        group_name=dict(required=False),
        access_token=dict(required=False),
        list_devices=dict(required=False, type=bool),
        list_groups=dict(required=False, type=bool),
        describe_identity=dict(required=False, type=bool),
        list_identity_providers=dict(required=False, type=bool),
        list_resource_servers=dict(required=False, type=bool),
        list_user_import_jobs=dict(required=False, type=bool),
        list_user_pool_clients=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
        list_users_in_group=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_devices', True, ['access_token']),
            ('list_groups', True, ['user_pool_id']),
            ('list_identity_providers', True, ['user_pool_id']),
            ('list_resource_servers', True, ['user_pool_id']),
            ('list_user_import_jobs', True, ['user_pool_id']),
            ('list_user_pool_clients', True, ['user_pool_id']),
            ('list_users', True, ['user_pool_id']),
            ('list_users_in_group', True, ['user_pool_id', 'group_name']),

        ),
        mutually_exclusive=[
            (
                'list_devices',
                'list_groups',
                'list_identity_providers',
                'list_resource_servers',
                'list_user_import_jobs',
                'list_user_pool_clients',
                'list_users',
                'list_users_in_group',
            )
        ],
    )

    client = module.client('cognito-idp', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cognito(client, module)

    if module.params['list_devices']:
        module.exit_json(devices=aws_response_list_parser(paginate, _it, 'Devices'))
    elif module.params['list_groups']:
        module.exit_json(groups=aws_response_list_parser(paginate, _it, 'Groups'))
    elif module.params['list_identity_providers']:
        module.exit_json(providers=aws_response_list_parser(paginate, _it, 'Providers'))
    elif module.params['list_resource_servers']:
        module.exit_json(resource_servers=aws_response_list_parser(paginate, _it, 'ResourceServers'))
    elif module.params['list_user_import_jobs']:
        module.exit_json(user_import_jobs=aws_response_list_parser(paginate, _it, 'UserImportJobs'))
    elif module.params['list_user_pool_clients']:
        module.exit_json(user_pool_clients=aws_response_list_parser(paginate, _it, 'UserPoolClients'))
    elif module.params['list_users'] or module.params['list_users_in_group']:
        module.exit_json(users=aws_response_list_parser(paginate, _it, 'Users'))
    else:
        module.exit_json(user_pools=aws_response_list_parser(paginate, _it, 'UserPools'))


if __name__ == '__main__':
    main()
