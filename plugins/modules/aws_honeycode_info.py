#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_honeycode_info
short_description: Get Information about Amazon Honey Code.
description:
  - Get Information about Amazon Honey Code.
  - U(https://docs.aws.amazon.com/honeycode/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of workbook.
    required: false
    type: str
  table_id:
    description:
      - id of table.
    required: false
    type: str
  row_ids:
    description:
      - list of row ids to filter results.
    required: false
    type: list
  list_tables:
    description:
      - do you want to get list of tables for given workbook I(id)?
    required: false
    type: bool
  list_table_rows:
    description:
      - do you want to get list of table_rows for given workbook I(id) and I(table_id)?
    required: false
    type: bool
  list_table_columns:
    description:
      - do you want to get list of table_columns for workbook I(id) and I(table_id)?
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
  aws_honeycode_info:
    list_tables: true
    id: 'workbook-id-test'

- name: "get list of table_rows"
  aws_honeycode_info:
    list_table_rows: true
    id: 'workbook-id-test'
    table_id: 'test-table-id'
    row_ids: []

- name: "get list of table_columns"
  aws_honeycode_info:
    list_table_columns: true
    id: 'workbook-id-test'
    table_id: 'test-table-id'
"""

RETURN = """
tables:
  description: list of tables.
  returned: when `list_tables` is defined and success.
  type: list
table_rows:
  description: list of table_rows.
  returned: when `list_table_rows` is defined and success.
  type: list
table_columns:
  description: list of table_columns.
  returned: when `list_table_columns` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _honeycode(client, module):
    try:
        if module.params['list_tables']:
            if client.can_paginate('list_tables'):
                paginator = client.get_paginator('list_tables')
                return paginator.paginate(
                    workbookId=module.params['id']
                ), True
            else:
                return client.list_tables(
                    workbookId=module.params['id']
                ), False
        elif module.params['list_table_rows']:
            if client.can_paginate('list_table_rows'):
                paginator = client.get_paginator('list_table_rows')
                return paginator.paginate(
                    workbookId=module.params['id'],
                    tableId=module.params['table_id'],
                    rowIds=module.params['row_ids'],
                ), True
            else:
                return client.list_table_rows(
                    workbookId=module.params['id'],
                    tableId=module.params['table_id'],
                    rowIds=module.params['row_ids'],
                ), False
        elif module.params['list_table_columns']:
            if client.can_paginate('list_table_columns'):
                paginator = client.get_paginator('list_table_columns')
                return paginator.paginate(
                    workbookId=module.params['id'],
                    tableId=module.params['table_id'],
                ), True
            else:
                return client.list_table_columns(
                    workbookId=module.params['id'],
                    tableId=module.params['table_id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Honey Code details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        table_id=dict(required=False),
        row_ids=dict(required=False, type=list, default=[]),
        list_tables=dict(required=False, type=bool),
        list_table_rows=dict(required=False, type=bool),
        list_table_columns=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_tables', True, ['id']),
            ('list_table_rows', True, ['id', 'table_id', 'row_ids']),
            ('list_table_columns', True, ['id', 'table_id']),
        ),
        mutually_exclusive=[
            (
                'list_tables',
                'list_table_rows',
                'list_table_columns',
            )
        ],
    )

    client = module.client('honeycode', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _honeycode(client, module)

    if module.params['list_tables']:
        module.exit_json(tables=aws_response_list_parser(paginate, it, 'tables'))
    elif module.params['list_table_rows']:
        module.exit_json(table_rows=aws_response_list_parser(paginate, it, 'rows'))
    elif module.params['list_table_columns']:
        module.exit_json(table_columns=aws_response_list_parser(paginate, it, 'tableColumns'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
