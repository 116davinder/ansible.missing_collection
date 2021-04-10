#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_redshift_data_info
short_description: Get Information about Amazon Redshift Data API Service.
description:
  - Get Information about Amazon Redshift Data API Service.
  - U(https://docs.aws.amazon.com/redshift-data/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of the cluster.
    required: false
    type: str
    aliases: ['cluster_identifier']
  database:
    description:
      - name of the database.
    required: false
    type: str
    aliases: ['database_name']
  database_user:
    description:
      - name of the database user.
    required: false
    type: str
  status:
    description:
      - status of statements.
    required: false
    type: str
    choices: ['SUBMITTED', 'PICKED', 'STARTED', 'FINISHED', 'ABORTED', 'FAILED', 'ALL']
    default: 'ALL'
  list_databases:
    description:
      - do you want to get list of databases for given I(id) and I(database_user)?
    required: false
    type: bool
  list_schemas:
    description:
      - do you want to get schemas for given I(id), database I(name), and I(database_user)??
    required: false
    type: bool
  list_statements:
    description:
      - do you want to get list of statements for given I(status)?
    required: false
    type: bool
  list_tables:
    description:
      - do you want to get tables for given I(id), database I(name), and I(database_user)??
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
- name: "get list of databases"
  aws_redshift_data_info:
    list_databases: true
    id: 'cluster_id'
    database_user: 'dpal'

- name: "get list of schemas"
  aws_redshift_data_info:
    list_schemas: true
    id: 'cluster_id'
    database: 'database_name'
    database_user: 'dpal'

- name: "get list of statements"
  aws_redshift_data_info:
    list_statements: true
    status: 'ALL'

- name: "get list of tables"
  aws_redshift_data_info:
    list_tables: true
    id: 'cluster_id'
    database: 'database_name'
    database_user: 'dpal'
"""

RETURN = """
databases:
  description: list of databases.
  returned: when `list_databases` is defined and success.
  type: list
schemas:
  description: get of schemas.
  returned: when `list_schemas` is defined and success.
  type: list
statements:
  description: list of statements.
  returned: when `list_statements` is defined and success.
  type: list
tables:
  description: list of tables.
  returned: when `list_tables` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _redshift_data(client, module):
    try:
        if module.params['list_databases']:
            if client.can_paginate('list_databases'):
                paginator = client.get_paginator('list_databases')
                return paginator.paginate(
                    ClusterIdentifier=module.params['id'],
                    DbUser=module.params['database_user']
                ), True
            else:
                return client.list_databases(
                    ClusterIdentifier=module.params['id'],
                    DbUser=module.params['database_user']
                ), False
        elif module.params['list_schemas']:
            if client.can_paginate('list_schemas'):
                paginator = client.get_paginator('list_schemas')
                return paginator.paginate(
                    ClusterIdentifier=module.params['id'],
                    Database=module.params['database'],
                    DbUser=module.params['database_user']
                ), True
            else:
                return client.list_schemas(
                    ClusterIdentifier=module.params['id'],
                    Database=module.params['database'],
                    DbUser=module.params['database_user']
                ), False
        elif module.params['list_statements']:
            if client.can_paginate('list_statements'):
                paginator = client.get_paginator('list_statements')
                return paginator.paginate(
                    Status=module.params['status']
                ), True
            else:
                return client.list_statements(
                    Status=module.params['status']
                ), False
        elif module.params['list_tables']:
            if client.can_paginate('list_tables'):
                paginator = client.get_paginator('list_tables')
                return paginator.paginate(
                    ClusterIdentifier=module.params['id'],
                    Database=module.params['database'],
                    DbUser=module.params['database_user']
                ), True
            else:
                return client.list_tables(
                    ClusterIdentifier=module.params['id'],
                    Database=module.params['database'],
                    DbUser=module.params['database_user']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Redshift Data API Service details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['cluster_identifier']),
        database=dict(required=False, aliases=['database_name']),
        database_user=dict(required=False),
        status=dict(required=False, choices=['SUBMITTED', 'PICKED', 'STARTED', 'FINISHED', 'ABORTED', 'FAILED', 'ALL'], default='ALL'),
        list_databases=dict(required=False, type=bool),
        list_schemas=dict(required=False, type=bool),
        list_statements=dict(required=False, type=bool),
        list_tables=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_databases', True, ['id', 'database_user']),
            ('list_schemas', True, ['id', 'database', 'database_user']),
            ('list_tables', True, ['id', 'database', 'database_user']),
        ),
        mutually_exclusive=[
            (
                'list_databases',
                'list_schemas',
                'list_statements',
                'list_tables',
            )
        ],
    )

    client = module.client('redshift-data', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _redshift_data(client, module)

    if module.params['list_databases']:
        module.exit_json(databases=aws_response_list_parser(paginate, it, 'Databases'))
    elif module.params['list_schemas']:
        module.exit_json(schemas=aws_response_list_parser(paginate, it, 'Schemas'))
    elif module.params['list_statements']:
        module.exit_json(statements=aws_response_list_parser(paginate, it, 'Statements'))
    elif module.params['list_tables']:
        module.exit_json(tables=aws_response_list_parser(paginate, it, 'Tables'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
