#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dynamodb_info
short_description: Get Information about Amazon DynamoDB.
description:
  - Get Information about Amazon DynamoDB.
  - U(https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB.html)
version_added: 0.0.5
options:
  arn:
    description:
      - arn of table.
    required: false
    type: str
    aliases: ['table_arn']
  name:
    description:
      - name of table.
    required: false
    type: str
    aliases: ['table_name']
  backup_type:
    description:
      - type of backup.
    required: false
    type: str
    choices: ['USER', 'SYSTEM', 'AWS_BACKUP', 'ALL']
    default: 'ALL'
  list_global_tables:
    description:
      - do you want to get list of global tables?
    required: false
    type: bool
  list_exports:
    description:
      - do you want to get list of export jobs for given I(arn)?
    required: false
    type: bool
  list_contributor_insights:
    description:
      - do you want to get list of contributor insights for given I(name)?
    required: false
    type: bool
  list_backups:
    description:
      - do you want to get list of backups for given I(name) and I(backup_type)?
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
- name: "get list of tables"
  aws_dynamodb_info:

- name: "get list of global tables"
  aws_dynamodb_info:
    list_global_tables: true

- name: "get list of export jobs"
  aws_dynamodb_info:
    list_exports: true
    arn: 'test-arn'

- name: "get list of contributor insights"
  aws_dynamodb_info:
    list_contributor_insights: true
    name: 'test-name'

- name: "get list of backups"
  aws_dynamodb_info:
    list_backups: true
    name: 'test-name'
"""

RETURN = """
table_names:
  description: list of tables.
  returned: when no arguments are defined and success
  type: list
global_tables:
  description: list of global tables.
  returned: when `list_global_tables` is defined and success
  type: list
exports:
  description: list of exports.
  returned: when `list_exports` is defined and success
  type: list
contributor_insights:
  description: list of contributor insights.
  returned: when `list_contributor_insights` is defined and success
  type: list
backups:
  description: list of backups.
  returned: when `list_backups` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
    else:
        for _app in iterator[resource_field]:
            try:
                _return.append(camel_dict_to_snake_dict(_app))
            except AttributeError:
                _return.append(_app)
    return _return


def _dynamodb(client, module):
    try:
        if module.params['list_global_tables']:
            if client.can_paginate('list_global_tables'):
                paginator = client.get_paginator('list_global_tables')
                return paginator.paginate(), True
            else:
                return client.list_global_tables(), False
        elif module.params['list_exports']:
            if client.can_paginate('list_exports'):
                paginator = client.get_paginator('list_exports')
                return paginator.paginate(
                    TableArn=module.params['arn'],
                ), True
            else:
                return client.list_exports(
                    TableArn=module.params['arn'],
                ), False
        elif module.params['list_contributor_insights']:
            if client.can_paginate('list_exports'):
                paginator = client.get_paginator('list_exports')
                return paginator.paginate(
                    TableName=module.params['name'],
                ), True
            else:
                return client.list_exports(
                    TableName=module.params['name'],
                ), False
        elif module.params['list_backups']:
            if client.can_paginate('list_backups'):
                paginator = client.get_paginator('list_backups')
                return paginator.paginate(
                    TableName=module.params['name'],
                    BackupType=module.params['backup_type'],
                ), True
            else:
                return client.list_backups(
                    TableName=module.params['name'],
                    BackupType=module.params['backup_type'],
                ), False
        else:
            if client.can_paginate('list_tables'):
                paginator = client.get_paginator('list_tables')
                return paginator.paginate(), True
            else:
                return client.list_tables(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Dynamo DB details')


def main():
    argument_spec = dict(
        arn=dict(required=False, type=list, aliases=['table_arn']),
        name=dict(required=False, type=list, aliases=['table_name']),
        backup_type=dict(
            required=False,
            choices=['USER', 'SYSTEM', 'AWS_BACKUP', 'ALL'],
            default='ALL'
        ),
        list_global_tables=dict(required=False, type=bool),
        list_exports=dict(required=False, type=bool),
        list_contributor_insights=dict(required=False, type=bool),
        list_backups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_exports', True, ['arn']),
            ('list_contributor_insights', True, ['name']),
            ('list_backups', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_global_tables',
                'list_exports',
                'list_contributor_insights',
                'list_backups',
            )
        ],
    )

    client = module.client('dynamodb', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _dynamodb(client, module)

    if module.params['list_global_tables']:
        module.exit_json(global_tables=aws_response_list_parser(paginate, it, 'GlobalTables'))
    elif module.params['list_exports']:
        module.exit_json(exports=aws_response_list_parser(paginate, it, 'ExportSummaries'))
    elif module.params['list_contributor_insights']:
        module.exit_json(contributor_insights=aws_response_list_parser(paginate, it, 'ContributorInsightsSummaries'))
    elif module.params['list_backups']:
        module.exit_json(backups=aws_response_list_parser(paginate, it, 'BackupSummaries'))
    else:
        module.exit_json(table_names=aws_response_list_parser(paginate, it, 'TableNames'))


if __name__ == '__main__':
    main()
