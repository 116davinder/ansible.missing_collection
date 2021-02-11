#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_glue_info
short_description: Get Information about Amazon Glue.
description:
  - Get Information about Amazon Glue.
  - U(https://docs.aws.amazon.com/glue/latest/webapi/API_Operations.html)
version_added: 0.0.6
options:
  name:
    description:
      - can be name of registry?
      - can be name of database?
    required: false
    type: str
    aliases: ['registry_name', 'database_name']
  table_name:
    description:
      - name of table.
    required: false
    type: str
  list_workflows:
    description:
      - do you want to get list of workflows?
    required: false
    type: bool
  list_triggers:
    description:
      - do you want to get list of triggers?
    required: false
    type: bool
  list_schemas:
    description:
      - do you want to get list of schemas for given registry I(name)?
    required: false
    type: bool
  list_registries:
    description:
      - do you want to get list of registries?
    required: false
    type: bool
  list_ml_transforms:
    description:
      - do you want to get list of ml transforms?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs?
    required: false
    type: bool
  list_dev_endpoints:
    description:
      - do you want to get list of dev endpoints?
    required: false
    type: bool
  list_crawlers:
    description:
      - do you want to get list of crawlers?
    required: false
    type: bool
  get_databases:
    description:
      - do you want to get list of databases?
    required: false
    type: bool
  get_tables:
    description:
      - do you want to get list of tables for given database I(name)?
    required: false
    type: bool
  get_partitions:
    description:
      - do you want to get list of partitions for given database I(name) and I(table_name)?
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
- name: "get list of workflows"
  aws_glue_info:
    list_workflows: true

- name: "get list of triggers"
  aws_glue_info:
    list_triggers: true

- name: "get list of schemas"
  aws_glue_info:
    list_schemas: true
    registry_name: 'test'

- name: "get list of registries"
  aws_glue_info:
    list_registries: true

- name: "get list of ml transforms"
  aws_glue_info:
    list_ml_transforms: true

- name: "get list of jobs"
  aws_glue_info:
    list_jobs: true

- name: "get list of dev_endpoints"
  aws_glue_info:
    list_dev_endpoints: true

- name: "get list of crawlers"
  aws_glue_info:
    list_crawlers: true

- name: "get list of databases"
  aws_glue_info:
    get_databases: true

- name: "get list of tables"
  aws_glue_info:
    get_tables: true
    database_name: 'test'

- name: "get list of partitions"
  aws_glue_info:
    get_partitions: true
    database_name: 'test'
    table_name: 'test'
"""

RETURN = """
workflows:
  description: list of workflows.
  returned: when `list_workflows` is defined and success.
  type: list
triggers:
  description: list of triggers.
  returned: when `list_triggers` is defined and success.
  type: list
schemas:
  description: list of schemas.
  returned: when `list_schemas` is defined and success.
  type: list
registries:
  description: list of registries.
  returned: when `list_registries` is defined and success.
  type: list
ml_transforms:
  description: list of ml transforms.
  returned: when `list_ml_transforms` is defined and success.
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
dev_endpoints:
  description: list of dev endpoints.
  returned: when `list_dev_endpoints` is defined and success.
  type: list
crawlers:
  description: list of crawlers.
  returned: when `list_crawlers` is defined and success.
  type: list
databases:
  description: list of databases.
  returned: when `get_databases` is defined and success.
  type: list
tables:
  description: list of tables.
  returned: when `get_tables` is defined and success.
  type: list
partitions:
  description: list of partitions.
  returned: when `get_partitions` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _glue(client, module):
    try:
        if module.params['list_workflows']:
            if client.can_paginate('list_workflows'):
                paginator = client.get_paginator('list_workflows')
                return paginator.paginate(), True
            else:
                return client.list_workflows(), False
        elif module.params['list_triggers']:
            if client.can_paginate('list_triggers'):
                paginator = client.get_paginator('list_triggers')
                return paginator.paginate(), True
            else:
                return client.list_triggers(), False
        elif module.params['list_schemas']:
            if client.can_paginate('list_schemas'):
                paginator = client.get_paginator('list_schemas')
                return paginator.paginate(
                    RegistryId={
                        'RegistryName': module.params['name'],
                    }
                ), True
            else:
                return client.list_schemas(
                    RegistryId={
                        'RegistryName': module.params['name'],
                    }
                ), False
        elif module.params['list_registries']:
            if client.can_paginate('list_registries'):
                paginator = client.get_paginator('list_registries')
                return paginator.paginate(), True
            else:
                return client.list_registries(), False
        elif module.params['list_ml_transforms']:
            if client.can_paginate('list_ml_transforms'):
                paginator = client.get_paginator('list_ml_transforms')
                return paginator.paginate(), True
            else:
                return client.list_ml_transforms(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(), True
            else:
                return client.list_jobs(), False
        elif module.params['list_dev_endpoints']:
            if client.can_paginate('list_dev_endpoints'):
                paginator = client.get_paginator('list_dev_endpoints')
                return paginator.paginate(), True
            else:
                return client.list_dev_endpoints(), False
        elif module.params['list_crawlers']:
            if client.can_paginate('list_crawlers'):
                paginator = client.get_paginator('list_crawlers')
                return paginator.paginate(), True
            else:
                return client.list_crawlers(), False
        elif module.params['get_databases']:
            if client.can_paginate('get_databases'):
                paginator = client.get_paginator('get_databases')
                return paginator.paginate(
                    ResourceShareType=module.params['resource_share_type']
                ), True
            else:
                return client.get_databases(
                    ResourceShareType=module.params['resource_share_type']
                ), False
        elif module.params['get_tables']:
            if client.can_paginate('get_tables'):
                paginator = client.get_paginator('get_tables')
                return paginator.paginate(
                    DatabaseName=module.params['name']
                ), True
            else:
                return client.get_tables(
                    DatabaseName=module.params['name']
                ), False
        elif module.params['get_partitions']:
            if client.can_paginate('get_partitions'):
                paginator = client.get_paginator('get_partitions')
                return paginator.paginate(
                    DatabaseName=module.params['name'],
                    TableName=module.params['table_name']
                ), True
            else:
                return client.get_partitions(
                    DatabaseName=module.params['name'],
                    TableName=module.params['table_name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Glue details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['registry_name', 'schema_name', 'database_name']),
        table_name=dict(required=False),
        resource_share_type=dict(required=False, choices=['FOREIGN', 'ALL'], default='ALL'),
        list_workflows=dict(required=False, type=bool),
        list_triggers=dict(required=False, type=bool),
        list_schemas=dict(required=False, type=bool),
        list_registries=dict(required=False, type=bool),
        list_ml_transforms=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
        list_dev_endpoints=dict(required=False, type=bool),
        list_crawlers=dict(required=False, type=bool),
        get_databases=dict(required=False, type=bool),
        get_tables=dict(required=False, type=bool),
        get_partitions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_schemas', True, ['name']),
            ('get_tables', True, ['name']),
            ('get_partitions', True, ['name', 'table_name']),
        ),
        mutually_exclusive=[
            (
                'list_workflows',
                'list_triggers',
                'list_schemas',
                'list_schema_versions',
                'list_registries',
                'list_ml_transforms',
                'list_jobs',
                'list_dev_endpoints',
                'list_crawlers',
                'get_databases',
                'get_tables',
                'get_partitions',
            )
        ],
    )

    client = module.client('glue', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _glue(client, module)

    if module.params['list_workflows']:
        module.exit_json(workflows=aws_response_list_parser(paginate, it, 'Workflows'))
    elif module.params['list_triggers']:
        module.exit_json(triggers=aws_response_list_parser(paginate, it, 'TriggerNames'))
    elif module.params['list_schemas']:
        module.exit_json(schemas=aws_response_list_parser(paginate, it, 'Schemas'))
    elif module.params['list_registries']:
        module.exit_json(registries=aws_response_list_parser(paginate, it, 'Registries'))
    elif module.params['list_ml_transforms']:
        module.exit_json(ml_transforms=aws_response_list_parser(paginate, it, 'TransformIds'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'JobNames'))
    elif module.params['list_dev_endpoints']:
        module.exit_json(dev_endpoints=aws_response_list_parser(paginate, it, 'DevEndpointNames'))
    elif module.params['list_crawlers']:
        module.exit_json(crawlers=aws_response_list_parser(paginate, it, 'CrawlerNames'))
    elif module.params['get_databases']:
        module.exit_json(databases=aws_response_list_parser(paginate, it, 'DatabaseList'))
    elif module.params['get_tables']:
        module.exit_json(tables=aws_response_list_parser(paginate, it, 'TableList'))
    elif module.params['get_partitions']:
        module.exit_json(partitions=aws_response_list_parser(paginate, it, 'Partitions'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
