#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_athena_info
short_description: Get Information about AWS Athena.
description:
  - Get Information about AWS Athena.
version_added: 0.0.1
options:
  name:
    description:
      - name of the athena catalog.
      - Mutually Exclusive: I(list_work_groups) and I(name).
    required: false
    type: str
    aliases: ['catalog_name']
  list_databases:
    description:
      - do you want to fetch all databases for given athena catalog.
      - Mutually Exclusive I(list_databases) , I(list_database_tables) and I(list_work_groups).
    required: false
    type: bool
  list_database_tables:
    description:
      - do you want to fetch all tables and there metadata for given athena database.
      - I(database_name) is required for it.
      - Mutually Exclusive I(list_databases) , I(list_database_tables) and I(list_work_groups).
    required: false
    type: bool
  list_work_groups:
    description:
      - do you want to fetch all the athena work groups.
      - Mutually Exclusive I(list_databases) , I(list_database_tables) and I(list_work_groups).
    required: false
    type: bool
  database_name:
    description:
      - name of the athena database.
    required: false
    type: str
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
- name: "get list of athena catalogs"
  aws_athena_info:
  register: __c

- name: "get list of athena database for given catalog"
  aws_athena_info:
    name: "{{ __c.catalogs[0].catalog_name }}"
    list_databases: True
  register: __db

- name: "get list of tables for given database"
  aws_athena_info:
    name: "{{ __c.catalogs[0].catalog_name }}"
    database_name: "{{ __db.databases[0].name }}"
    list_database_tables: true
  register: __tb

- name: "get list of athena work groups"
  aws_athena_info:
    list_work_groups: true
  register: __wg
"""

RETURN = """
catalogs:
  description: List of Athena Catalogs.
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        "catalog_name": "AwsDataCatalog",
        "type": "GLUE"
    }
  ]

databases:
  description: List of athena database for given catalog.
  returned: when I(list_databases) and success
  type: list
  sample: [
    {
        "description": "Sample database",
        "name": "sampledb",
        "parameters": {
            "created_by": "Athena",
            "external": "TRUE"
        }
    }
  ]

tables:
  description: List of database tables with metadata.
  returned: when I(list_database_tables) and success
  type: list
  sample: [
    {
        "columns": [
            {
                "name": "request_timestamp",
                "type": "string"
            }
        ],
        "create_time": "2020-12-19T23:39:38+02:00",
        "last_access_time": "2020-12-19T23:39:38+02:00",
        "name": "elb_logs",
        "parameters": {},
        "partition_keys": [],
        "table_type": "EXTERNAL_TABLE"
    }
  ]

work_groups:
  description: List of Athena Work Groups.
  returned: when I(list_work_groups) and success
  type: list
  sample: [
    {
        "creation_time": "2020-12-19T23:39:31.222000+02:00",
        "description": "",
        "name": "primary",
        "state": "ENABLED"
    }
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _athena(module):
    try:
        athena = module.client('athena')

        if module.params['list_databases']:
            if athena.can_paginate('list_databases'):
                paginator = athena.get_paginator('list_databases')
                return paginator.paginate(
                    CatalogName=module.params['name']
                ), True
            else:
                return athena.list_databases(
                    CatalogName=module.params['name']
                ), False
        elif module.params['list_database_tables']:
            if athena.can_paginate('list_table_metadata'):
                paginator = athena.get_paginator('list_table_metadata')
                return paginator.paginate(
                    CatalogName=module.params['name'],
                    DatabaseName=module.params['database_name']
                ), True
            else:
                return athena.list_table_metadata(
                    CatalogName=module.params['name'],
                    DatabaseName=module.params['database_name']
                ), False
        elif module.params['list_work_groups']:
            if athena.can_paginate('list_work_groups'):
                paginator = athena.get_paginator('list_work_groups')
                return paginator.paginate(), True
            else:
                return athena.list_work_groups(), False
        else:
            if athena.can_paginate('list_data_catalogs'):
                paginator = athena.get_paginator('list_data_catalogs')
                return paginator.paginate(), True
            else:
                return athena.list_data_catalogs(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws athena details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['catalog_name']),
        list_databases=dict(required=False, type=bool),
        database_name=dict(required=False),
        list_database_tables=dict(required=False, type=bool),
        list_work_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_databases', True, ['name']),
            ('list_database_tables', True, ['name', 'database_name'])
        ),
        mutually_exclusive=[
            ('list_databases', 'list_database_tables', 'list_work_groups'),
            ('name', 'list_work_groups'),
            ('database_name', 'list_work_groups')
        ],
    )

    __default_return = []

    _it, _paginate = _athena(module)
    if _it is not None:
        if module.params['list_databases']:
            module.exit_json(databases=aws_response_list_parser(_paginate, _it, 'DatabaseList'))
        elif module.params['list_database_tables']:
            module.exit_json(tables=aws_response_list_parser(_paginate, _it, 'TableMetadataList'))
        elif module.params['list_work_groups']:
            module.exit_json(work_groups=aws_response_list_parser(_paginate, _it, 'WorkGroups'))
        else:
            module.exit_json(catalogs=aws_response_list_parser(_paginate, _it, 'DataCatalogsSummary'))


if __name__ == '__main__':
    main()
