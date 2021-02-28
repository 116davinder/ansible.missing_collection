#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_lakeformation_info
short_description: Get Information about AWS Lake Formation.
description:
  - Get Information about AWS Lake Formation.
  - U(https://docs.aws.amazon.com/lakeformation/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  id:
    description:
      - catalog id.
    required: false
    type: str
    aliases: ['catalog_id']
  data_lake_principal_identifier:
    description:
      - An identifier for the AWS Lake Formation principal.
    required: false
    type: str
  resource_type:
    description:
      - type of resource to filter list permissions.
    required: false
    type: str
    choices: ['CATALOG', 'DATABASE', 'TABLE', 'DATA_LOCATION']
    default: 'CATALOG'
  list_resources:
    description:
      - do you want to get list of resources?
    required: false
    type: bool
  list_permissions:
    description:
      - do you want to get list of permissions for given key I(resource_type) & I(data_lake_principal_identifier)?
    required: false
    type: bool
  get_data_lake_settings:
    description:
      - do you want to get data_lake_settings for given key I(id)?
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
- name: "get list of resources"
  aws_lakeformation_info:
    list_resources: true

- name: "get list of permissions"
  aws_lakeformation_info:
    list_permissions: true
    data_lake_principal_identifier: 'test'
    resource_type: 'CATALOG'

- name: "get data_lake_settings"
  aws_lakeformation_info:
    get_data_lake_settings: true
    id: 'catalog-id'
"""

RETURN = """
resources:
  description: list of resources.
  returned: when `list_resources` is defined and success.
  type: list
permissions:
  description: list of permissions.
  returned: when `list_permissions`is defined and success.
  type: list
data_lake_settings:
  description: get data_lake_settings.
  returned: when `get_data_lake_settings` is defined and success.
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


def _lakeformation(client, module):
    try:
        if module.params['list_resources']:
            if client.can_paginate('list_resources'):
                paginator = client.get_paginator('list_resources')
                return paginator.paginate(), True
            else:
                return client.list_resources(), False
        elif module.params['list_permissions']:
            if client.can_paginate('list_permissions'):
                paginator = client.get_paginator('list_permissions')
                return paginator.paginate(
                    ResourceType=module.params['resource_type'],
                    Principal={
                        'DataLakePrincipalIdentifier': module.params['data_lake_principal_identifier']
                    }
                ), True
            else:
                return client.list_permissions(
                    KeyId=module.params['id'],
                ), False
        elif module.params['get_data_lake_settings']:
            return client.get_data_lake_settings(
                CatalogId=module.params['id'],
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon lakeformation details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['catalog_id']),
        data_lake_principal_identifier=dict(required=False),
        resource_type=dict(required=False, choices=['CATALOG', 'DATABASE', 'TABLE', 'DATA_LOCATION'], default='CATALOG'),
        list_resources=dict(required=False, type=bool),
        list_permissions=dict(required=False, type=bool),
        get_data_lake_settings=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_permissions', True, ['data_lake_principal_identifier']),
            ('get_data_lake_settings', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_resources',
                'list_permissions',
                'get_data_lake_settings',
            )
        ],
    )

    client = module.client('lakeformation', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _lakeformation(client, module)

    if module.params['list_resources']:
        module.exit_json(resources=aws_response_list_parser(paginate, it, 'ResourceInfoList'))
    elif module.params['list_permissions']:
        module.exit_json(permissions=aws_response_list_parser(paginate, it, 'PrincipalResourcePermissions'))
    elif module.params['get_data_lake_settings']:
        module.exit_json(data_lake_settings=camel_dict_to_snake_dict(it['DataLakeSettings']))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
