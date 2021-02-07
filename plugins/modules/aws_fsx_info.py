#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_fsx_info
short_description: Get Information about Amazon FSx.
description:
  - Get Information about Amazon FSx.
  - U(https://docs.aws.amazon.com/fsx/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  ids:
    description:
      - can be list of backup ids?
      - can be list of file system ids?
      - can be list of task ids?
    required: false
    type: list
  describe_backups:
    description:
      - do you want to get details of backups for given I(ids)?
    required: false
    type: bool
  describe_file_systems:
    description:
      - do you want to get details of filesystems of given I(ids)?
    required: false
    type: bool
  describe_data_repository_tasks:
    description:
      - do you want to get details of data repository tasks of given I(ids)?
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
- name: "get details of backups"
  aws_fsx_info:
    describe_backups: true
    ids: []

- name: "get details of file systems"
  aws_fsx_info:
    describe_file_systems: true
    ids: []

- name: "get details of data repository tasks"
  aws_fsx_info:
    describe_data_repository_tasks: true
    ids: []
"""

RETURN = """
backups:
  description: details about backups.
  returned: when `describe_backups` is defined and success.
  type: list
file_systems:
  description: details about filesystems.
  returned: when `describe_file_systems` is defined and success.
  type: dict
data_repository_tasks:
  description: details about data repository tasks.
  returned: when `describe_data_repository_tasks` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _fsx(client, module):
    try:
        if module.params['describe_backups']:
            if client.can_paginate('describe_backups'):
                paginator = client.get_paginator('describe_backups')
                return paginator.paginate(
                    BackupIds=module.params['ids'],
                ), True
            else:
                return client.describe_backups(
                    BackupIds=module.params['ids'],
                ), False
        elif module.params['describe_file_systems']:
            if client.can_paginate('describe_file_systems'):
                paginator = client.get_paginator('describe_file_systems')
                return paginator.paginate(
                    FileSystemIds=module.params['ids'],
                ), True
            else:
                return client.describe_file_systems(
                    FileSystemIds=module.params['ids'],
                ), False
        elif module.params['describe_data_repository_tasks']:
            if client.can_paginate('describe_data_repository_tasks'):
                paginator = client.get_paginator('describe_data_repository_tasks')
                return paginator.paginate(
                    TaskIds=module.params['ids'],
                ), True
            else:
                return client.describe_data_repository_tasks(
                    TaskIds=module.params['ids'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon fsx details')


def main():
    argument_spec = dict(
        ids=dict(required=False, type=list, default=[]),
        describe_backups=dict(required=False, type=bool),
        describe_file_systems=dict(required=False, type=bool),
        describe_data_repository_tasks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'describe_backups',
                'describe_file_systems',
                'describe_data_repository_tasks',
            )
        ],
    )

    client = module.client('fsx', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _fsx(client, module)

    if module.params['describe_backups']:
        module.exit_json(backups=aws_response_list_parser(paginate, it, 'Backups'))
    elif module.params['describe_file_systems']:
        module.exit_json(file_systems=aws_response_list_parser(paginate, it, 'FileSystems'))
    elif module.params['describe_data_repository_tasks']:
        module.exit_json(data_repository_tasks=aws_response_list_parser(paginate, it, 'DataRepositoryTasks'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
