#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_wellarchitected_info
short_description: Get Information about AWS Well-Architected Tool.
description:
  - Get Information about AWS Well-Architected Tool.
  - U(https://docs.aws.amazon.com/wellarchitected/latest/APIReference/API_Operations.html)
version_added: 0.1.0
options:
  id:
    description:
      - id of workload.
    required: false
    type: str
    aliases: ['workload_id']
  prefix:
    description:
      - workload name prefix.
    required: false
    type: str
    aliases: ['workload_name_prefix']
  list_lenses:
    description:
      - do you want to get list of lenses?
    required: false
    type: bool
  list_milestones:
    description:
      - do you want to get milestones for given I(id)?
    required: false
    type: bool
  list_notifications:
    description:
      - do you want to get notifications for given I(id)?
    required: false
    type: bool
  list_workloads:
    description:
      - do you want to get workloads for given I(prefix)?
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
- name: "get list of lenses"
  aws_wellarchitected_info:
    list_lenses: true

- name: "get milestones"
  aws_wellarchitected_info:
    list_milestones: true
    id: 'workload_id'

- name: "get notifications"
  aws_wellarchitected_info:
    list_notifications: true
    id: 'workload_id'

- name: "get workloads"
  aws_wellarchitected_info:
    list_workloads: true
    prefix: 'workload_name_prefix'
"""

RETURN = """
lenses:
  description: list of lenses.
  returned: when `list_lenses` is defined and success.
  type: list
milestones:
  description: list of milestones.
  returned: when `list_milestones` is defined and success.
  type: list
notifications:
  description: list of notifications.
  returned: when `list_notifications` is defined and success.
  type: list
workloads:
  description: list of workloads.
  returned: when `list_workloads` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _wellarchitected(client, module):
    try:
        if module.params['list_lenses']:
            if client.can_paginate('list_lenses'):
                paginator = client.get_paginator('list_lenses')
                return paginator.paginate(), True
            else:
                return client.list_lenses(), False
        elif module.params['list_milestones']:
            if client.can_paginate('list_milestones'):
                paginator = client.get_paginator('list_milestones')
                return paginator.paginate(
                    WorkloadId=module.params['id']
                ), True
            else:
                return client.list_milestones(
                    WorkloadId=module.params['id']
                ), False
        elif module.params['list_notifications']:
            if client.can_paginate('list_notifications'):
                paginator = client.get_paginator('list_notifications')
                return paginator.paginate(
                    WorkloadId=module.params['id']
                ), True
            else:
                return client.list_notifications(
                    WorkloadId=module.params['id']
                ), False
        elif module.params['list_workloads']:
            if client.can_paginate('list_workloads'):
                paginator = client.get_paginator('list_workloads')
                return paginator.paginate(
                    WorkloadNamePrefix=module.params['prefix']
                ), True
            else:
                return client.list_workloads(
                    WorkloadNamePrefix=module.params['prefix']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Well-Architected Tool details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['workload_id']),
        prefix=dict(required=False, aliases=['workload_name_prefix']),
        list_lenses=dict(required=False, type=bool),
        list_milestones=dict(required=False, type=bool),
        list_notifications=dict(required=False, type=bool),
        list_workloads=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_milestones', True, ['id']),
            ('list_notifications', True, ['id']),
            ('list_workloads', True, ['prefix']),
        ),
        mutually_exclusive=[
            (
                'list_lenses',
                'list_milestones',
                'list_notifications',
                'list_workloads',
            )
        ],
    )

    client = module.client('wellarchitected', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _wellarchitected(client, module)

    if module.params['list_lenses']:
        module.exit_json(lenses=aws_response_list_parser(paginate, it, 'LensSummaries'))
    elif module.params['list_milestones']:
        module.exit_json(milestones=aws_response_list_parser(paginate, it, 'MilestoneSummaries'))
    elif module.params['list_notifications']:
        module.exit_json(notifications=aws_response_list_parser(paginate, it, 'NotificationSummaries'))
    elif module.params['list_workloads']:
        module.exit_json(workloads=aws_response_list_parser(paginate, it, 'WorkloadSummaries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
