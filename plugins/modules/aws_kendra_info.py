#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kendra_info
short_description: Get Information about AWS KendraFrontendService.
description:
  - Get Information about AWS KendraFrontendService.
  - U(https://docs.aws.amazon.com/kendra/latest/dg/API_Operations.html)
version_added: 0.0.7
options:
  id:
    description:
      - datasource id.
    required: false
    type: str
    aliases: ['datasource_id']
  index_id:
    description:
      - index id.
    required: false
    type: str
  status_filter:
    description:
      - status to filter data source sync jobs.
    required: false
    type: str
    choices: ['FAILED', 'SUCCEEDED', 'SYNCING', 'INCOMPLETE', 'STOPPING', 'ABORTED', 'SYNCING_INDEXING']
    default: 'SUCCEEDED'
  list_data_source_sync_jobs:
    description:
      - do you want to get list of data_source_sync_jobs for given index I(index_id)?
    required: false
    type: bool
  list_data_sources:
    description:
      - do you want to get list of data_sources for given index I(index_id)?
    required: false
    type: bool
  list_faqs:
    description:
      - do you want to get list of configuration revisions for given index I(index_id)?
    required: false
    type: bool
  list_indices:
    description:
      - do you want to get list of indices?
    required: false
    type: bool
  list_thesauri:
    description:
      - do you want to get list of thesauri for given index I(index_id)?
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
- name: "get list of data_source_sync_jobs"
  aws_kendra_info:
    list_data_source_sync_jobs: true
    id: 'datasource_id'
    index_id: 'index_id'
    status_filter: 'SUCCEEDED'

- name: "get list of data_sources"
  aws_kendra_info:
    list_data_sources: true
    index_id: 'test-index-id'

- name: "get list of faqs"
  aws_kendra_info:
    list_faqs: true
    index_id: 'test-index-id'

- name: "get list of indices"
  aws_kendra_info:
    list_indices: true

- name: "get list of thesauri"
  aws_kendra_info:
    list_thesauri: true
    index_id: 'test-index-id'
"""

RETURN = """
data_source_sync_jobs:
  description: list of data_source_sync_jobs.
  returned: when `list_data_source_sync_jobs` is defined and success.
  type: list
data_sources:
  description: list of data_sources.
  returned: when `list_data_sources` is defined and success.
  type: list
faqs:
  description: list of faqs.
  returned: when `list_faqs` is defined and success.
  type: list
indices:
  description: list of indices.
  returned: when `list_indices` is defined and success.
  type: list
thesauri:
  description: list of thesauri.
  returned: when `list_thesauri` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kendra(client, module):
    try:
        if module.params['list_data_source_sync_jobs']:
            if client.can_paginate('list_data_source_sync_jobs'):
                paginator = client.get_paginator('list_data_source_sync_jobs')
                return paginator.paginate(
                    Id=module.params['id'],
                    IndexId=module.params['index_id'],
                    StatusFilter=module.params['status_filter']
                ), True
            else:
                return client.list_data_source_sync_jobs(
                    Id=module.params['id'],
                    IndexId=module.params['index_id'],
                    StatusFilter=module.params['status_filter']
                ), False
        elif module.params['list_data_sources']:
            if client.can_paginate('list_data_sources'):
                paginator = client.get_paginator('list_data_sources')
                return paginator.paginate(
                    IndexId=module.params['index_id'],
                ), True
            else:
                return client.list_data_sources(
                    IndexId=module.params['index_id'],
                ), False
        elif module.params['list_faqs']:
            if client.can_paginate('list_faqs'):
                paginator = client.get_paginator('list_faqs')
                return paginator.paginate(
                    IndexId=module.params['index_id'],
                ), True
            else:
                return client.list_faqs(
                    IndexId=module.params['index_id'],
                ), False
        elif module.params['list_indices']:
            if client.can_paginate('list_indices'):
                paginator = client.get_paginator('list_indices')
                return paginator.paginate(), True
            else:
                return client.list_indices(), False
        elif module.params['list_thesauri']:
            if client.can_paginate('list_thesauri'):
                paginator = client.get_paginator('list_thesauri')
                return paginator.paginate(
                    IndexId=module.params['index_id'],
                ), True
            else:
                return client.list_thesauri(
                    IndexId=module.params['index_id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon kendra details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['datasource_id']),
        index_id=dict(required=False),
        status_filter=dict(
            required=False,
            choices=['FAILED', 'SUCCEEDED', 'SYNCING', 'INCOMPLETE', 'STOPPING', 'ABORTED', 'SYNCING_INDEXING'],
            default='SUCCEEDED'
        ),
        list_data_source_sync_jobs=dict(required=False, type=bool),
        list_data_sources=dict(required=False, type=bool),
        list_faqs=dict(required=False, type=bool),
        list_indices=dict(required=False, type=bool),
        list_thesauri=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_data_source_sync_jobs', True, ['id', 'index_id']),
            ('list_data_sources', True, ['index_id']),
            ('list_faqs', True, ['index_id']),
            ('list_thesauri', True, ['index_id']),
        ),
        mutually_exclusive=[
            (
                'list_data_source_sync_jobs',
                'list_data_sources',
                'list_faqs',
                'list_indices',
                'list_thesauri',
            )
        ],
    )

    client = module.client('kendra', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kendra(client, module)

    if module.params['list_data_source_sync_jobs']:
        module.exit_json(data_source_sync_jobs=aws_response_list_parser(paginate, it, 'History'))
    elif module.params['list_data_sources']:
        module.exit_json(data_sources=aws_response_list_parser(paginate, it, 'SummaryItems'))
    elif module.params['list_faqs']:
        module.exit_json(faqs=aws_response_list_parser(paginate, it, 'FaqSummaryItems'))
    elif module.params['list_indices']:
        module.exit_json(indices=aws_response_list_parser(paginate, it, 'IndexindicesummaryItems'))
    elif module.params['list_thesauri']:
        module.exit_json(thesauri=aws_response_list_parser(paginate, it, 'ThesaurusSummaryItems'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
