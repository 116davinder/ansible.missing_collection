#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_qldb_info
short_description: Get Information about Amazon QLDB.
description:
  - Get Information about Amazon QLDB.
  - U(https://docs.aws.amazon.com/qldb/latest/developergunamee/API_Operations_Amazon_QLDB.html)
version_added: 0.0.8
options:
  name:
    description:
      - name of the ledger.
    required: false
    type: str
    aliases: ['ledger_name']
  list_ledgers:
    description:
      - do you want to get list of ledgers?
    required: false
    type: bool
  list_journal_s3_exports_for_ledger:
    description:
      - do you want to get list of journal_s3_exports_for_ledger for given ledger I(name)?
    required: false
    type: bool
  list_journal_s3_exports:
    description:
      - do you want to get list of journal_s3_exports?
    required: false
    type: bool
  list_journal_kinesis_streams_for_ledger:
    description:
      - do you want to get journal_kinesis_streams_for_ledger for given ledger I(name)?
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
- name: "get list of ledgers"
  aws_qldb_info:
    list_ledgers: true

- name: "get journal_s3_exports_for_ledger"
  aws_qldb_info:
    list_journal_s3_exports_for_ledger: true
    name: 'ledger-name'

- name: "get list of journal_s3_exports"
  aws_qldb_info:
    list_journal_s3_exports: true

- name: "get journal_kinesis_streams_for_ledger"
  aws_qldb_info:
    list_journal_kinesis_streams_for_ledger: true
    name: 'ledger-name'
"""

RETURN = """
ledgers:
  description: list of ledgers.
  returned: when `list_ledgers` is defined and success.
  type: list
journal_s3_exports_for_ledger:
  description: get of journal_s3_exports_for_ledger.
  returned: when `list_journal_s3_exports_for_ledger` is defined and success.
  type: list
journal_s3_exports:
  description: list of journal_s3_exports.
  returned: when `list_journal_s3_exports` is defined and success.
  type: list
journal_kinesis_streams_for_ledger:
  description: list of journal_kinesis_streams_for_ledger.
  returned: when `list_journal_kinesis_streams_for_ledger` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _qldb(client, module):
    try:
        if module.params['list_ledgers']:
            if client.can_paginate('list_ledgers'):
                paginator = client.get_paginator('list_ledgers')
                return paginator.paginate(), True
            else:
                return client.list_ledgers(), False
        elif module.params['list_journal_s3_exports_for_ledger']:
            if client.can_paginate('list_journal_s3_exports_for_ledger'):
                paginator = client.get_paginator('list_journal_s3_exports_for_ledger')
                return paginator.paginate(
                    Name=module.params['name']
                ), True
            else:
                return client.list_journal_s3_exports_for_ledger(
                    Name=module.params['name']
                ), False
        elif module.params['list_journal_s3_exports']:
            if client.can_paginate('list_journal_s3_exports'):
                paginator = client.get_paginator('list_journal_s3_exports')
                return paginator.paginate(), True
            else:
                return client.list_journal_s3_exports(), False
        elif module.params['list_journal_kinesis_streams_for_ledger']:
            if client.can_paginate('list_journal_kinesis_streams_for_ledger'):
                paginator = client.get_paginator('list_journal_kinesis_streams_for_ledger')
                return paginator.paginate(
                    Name=module.params['name']
                ), True
            else:
                return client.list_journal_kinesis_streams_for_ledger(
                    Name=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon qldb details')


def main():
    argument_spec = dict(
        name=dict(
            required=False,
            aliases=['ledger_name']
        ),
        list_ledgers=dict(required=False, type=bool),
        list_journal_s3_exports_for_ledger=dict(required=False, type=bool),
        list_journal_s3_exports=dict(required=False, type=bool),
        list_journal_kinesis_streams_for_ledger=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_journal_s3_exports_for_ledger', True, ['name']),
            ('list_journal_kinesis_streams_for_ledger', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_ledgers',
                'list_journal_s3_exports_for_ledger',
                'list_journal_s3_exports',
                'list_journal_kinesis_streams_for_ledger',
            )
        ],
    )

    client = module.client('qldb', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _qldb(client, module)

    if module.params['list_ledgers']:
        module.exit_json(ledgers=aws_response_list_parser(paginate, it, 'Ledgers'))
    elif module.params['list_journal_s3_exports_for_ledger']:
        module.exit_json(journal_s3_exports_for_ledger=aws_response_list_parser(paginate, it, 'JournalS3Exports'))
    elif module.params['list_journal_s3_exports']:
        module.exit_json(journal_s3_exports=aws_response_list_parser(paginate, it, 'JournalS3Exports'))
    elif module.params['list_journal_kinesis_streams_for_ledger']:
        module.exit_json(journal_kinesis_streams_for_ledger=aws_response_list_parser(paginate, it, 'Streams'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
