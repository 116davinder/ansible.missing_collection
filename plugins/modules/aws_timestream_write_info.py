#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_timestream_write_info
short_description: Get Information about Amazon Timestream Write.
description:
  - Get Information about Amazon Timestream Write.
  - U(https://docs.aws.amazon.com/timestream/latest/developerguide/API_Operations_Amazon_Timestream_Write.html)
version_added: 0.1.0
options:
  database_name:
    description:
      - name of the database.
    required: false
    type: str
  list_databases:
    description:
      - do you want to get list of databases?
    required: false
    type: bool
  list_tables:
    description:
      - do you want to get tables for given I(database_name)?
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
  aws_timestream_write_info:
    list_databases: true

- name: "get tables"
  aws_timestream_write_info:
    list_tables: true
    database_name: 'test'
"""

RETURN = """
databases:
  description: list of the databases.
  returned: when `list_databases` is defined and success.
  type: list
tables:
  description: get of the tables.
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


def _timestream_write(client, module):
    try:
        if module.params['list_databases']:
            if client.can_paginate('list_databases'):
                paginator = client.get_paginator('list_databases')
                return paginator.paginate(), True
            else:
                return client.list_databases(), False
        elif module.params['list_tables']:
            if client.can_paginate('list_tables'):
                paginator = client.get_paginator('list_tables')
                return paginator.paginate(
                    DatabaseName=module.params['database_name'],
                ), True
            else:
                return client.list_tables(
                    DatabaseName=module.params['database_name'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Timestream Write details')


def main():
    argument_spec = dict(
        database_name=dict(required=False),
        list_databases=dict(required=False, type=bool),
        list_tables=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_tables', True, ['database_name']),
        ),
        mutually_exclusive=[
            (
                'list_databases',
                'list_tables',
            )
        ],
    )

    client = module.client('timestream-write', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _timestream_write(client, module)

    if module.params['list_databases']:
        module.exit_json(databases=aws_response_list_parser(paginate, it, 'Databases'))
    elif module.params['list_tables']:
        module.exit_json(tables=aws_response_list_parser(paginate, it, 'Tables'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
