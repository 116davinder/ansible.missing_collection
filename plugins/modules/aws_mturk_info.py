#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mturk_info
short_description: Get Information about Amazon Mechanical Turk (MTurk).
description:
  - Get Information about Amazon Mechanical Turk (MTurk).
  - U(https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_OperationsArticle.html)
version_added: 0.0.7
options:
  id:
    description:
      - hit id.
    required: false
    type: str
    aliases: ['hit_id']
  list_assignments_for_hit:
    description:
      - do you want to get list of assignments_for_hit for given hit I(id)?
    required: false
    type: bool
  list_bonus_payments:
    description:
      - do you want to get bonus_payments for given hit I(id)?
    required: false
    type: bool
  list_hits:
    description:
      - do you want to get list of hits?
    required: false
    type: bool
  list_worker_blocks:
    description:
      - do you want to get worker_blocks?
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
- name: "get list of assignments_for_hit"
  aws_mturk_info:
    list_assignments_for_hit: true
    id: 'hit_id'

- name: "get bonus_payments"
  aws_mturk_info:
    list_bonus_payments: true
    id: 'hit_id'

- name: "get list of hits"
  aws_mturk_info:
    list_hits: true

- name: "get worker_blocks"
  aws_mturk_info:
    list_worker_blocks: true
"""

RETURN = """
assignments_for_hit:
  description: list of assignments_for_hit.
  returned: when `list_assignments_for_hit` is defined and success.
  type: list
bonus_payments:
  description: get of bonus_payments.
  returned: when `list_bonus_payments` is defined and success.
  type: list
hits:
  description: list of hits.
  returned: when `list_hits` is defined and success.
  type: list
worker_blocks:
  description: list of worker_blocks.
  returned: when `list_worker_blocks` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mturk(client, module):
    try:
        if module.params['list_assignments_for_hit']:
            if client.can_paginate('list_assignments_for_hit'):
                paginator = client.get_paginator('list_assignments_for_hit')
                return paginator.paginate(
                    HITId=module.params['id']
                ), True
            else:
                return client.list_assignments_for_hit(
                    HITId=module.params['id']
                ), False
        elif module.params['list_bonus_payments']:
            if client.can_paginate('list_bonus_payments'):
                paginator = client.get_paginator('list_bonus_payments')
                return paginator.paginate(
                    HITId=module.params['id']
                ), True
            else:
                return client.list_bonus_payments(
                    HITId=module.params['id']
                ), False
        elif module.params['list_hits']:
            if client.can_paginate('list_hits'):
                paginator = client.get_paginator('list_hits')
                return paginator.paginate(), True
            else:
                return client.list_hits(), False
        elif module.params['list_worker_blocks']:
            if client.can_paginate('list_worker_blocks'):
                paginator = client.get_paginator('list_worker_blocks')
                return paginator.paginate(), True
            else:
                return client.list_worker_blocks(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Mechanical Turk (MTurk) details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['hit_id']),
        list_assignments_for_hit=dict(required=False, type=bool),
        list_bonus_payments=dict(required=False, type=bool),
        list_hits=dict(required=False, type=bool),
        list_worker_blocks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_assignments_for_hit', True, ['id']),
            ('list_bonus_payments', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_assignments_for_hit',
                'list_bonus_payments',
                'list_hits',
                'list_worker_blocks',
            )
        ],
    )

    client = module.client('mturk', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mturk(client, module)

    if module.params['list_assignments_for_hit']:
        module.exit_json(assignments_for_hit=aws_response_list_parser(paginate, it, 'Assignments'))
    elif module.params['list_bonus_payments']:
        module.exit_json(bonus_payments=aws_response_list_parser(paginate, it, 'BonusPayments'))
    elif module.params['list_hits']:
        module.exit_json(hits=aws_response_list_parser(paginate, it, 'HITs'))
    elif module.params['list_worker_blocks']:
        module.exit_json(worker_blocks=aws_response_list_parser(paginate, it, 'WorkerBlocks'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
