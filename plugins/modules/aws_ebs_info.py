#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ebs_info
short_description: Get Information about Amazon Elastic Block Store (EBS).
description:
  - Get Information about Amazon Elastic Block Store (EBS).
  - U(https://docs.aws.amazon.com/ebs/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of the snapshot.
    required: false
    type: str
  list_snapshot_blocks:
    description:
      - do you want to get details of snapshot blocks for given I(id)?
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
- name: "Gets detailed information about the snapshot blocks."
  aws_ebs_info:
    list_snapshot_blocks: true
    id: 'test-id'
"""

RETURN = """
snapshot_blocks:
  description: detailed information about the snapshot blocks.
  returned: when `list_snapshot_blocks` and `id` are defined and success
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
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _ebs(client, module):
    try:
        if module.params['list_snapshot_blocks']:
            if client.can_paginate('list_snapshot_blocks'):
                paginator = client.get_paginator('list_snapshot_blocks')
                return paginator.paginate(
                    SnapshotId=module.params['id'],
                ), True
            else:
                return client.list_snapshot_blocks(
                    SnapshotId=module.params['id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS ebs details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        list_snapshot_blocks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_snapshot_blocks', True, ['id']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('ebs', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ebs(client, module)

    if module.params['list_snapshot_blocks']:
        module.exit_json(snapshot_blocks=aws_response_list_parser(paginate, it, 'Blocks'))
    else:
        module.fail_json_aws("unknown options are passed")


if __name__ == '__main__':
    main()
