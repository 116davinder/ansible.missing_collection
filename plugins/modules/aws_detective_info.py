#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_detective_info
short_description: Get Information about AWS detective.
description:
  - Get Information about AWS detective.
  - U(https://docs.aws.amazon.com/detective/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  graph_arn:
    description:
      -  arn of the graph.
    required: false
    type: str
  list_invitations:
    description:
      - do you want to get list of invitation of graphs?
    required: false
    type: bool
  list_members:
    description:
      - do you want to get list of members of given I(graph_arn)?
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
- name: "Lists all of graphs."
  aws_detective_info:

- name: "Lists all of graph invitations."
  aws_detective_info:
    list_invitations: true

- name: "Lists of the graph members."
  aws_detective_info:
    list_members: true
    graph_arn: 'test-arn'
"""

RETURN = """
graph_list:
  description: Lists all of graphs.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'arn': 'string',
        'created_time': datetime(2015, 1, 1)
    },
  ]
invitations:
  description: Lists all of graph invitations.
  returned: when `list_invitations` is defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'email_address': 'string',
        'graph_arn': 'string',
        'master_id': 'string',
        'status': 'INVITED',
        'disabled_reason': 'VOLUME_TOO_HIGH',
        'invited_time': datetime(2015, 1, 1),
        'updated_time': datetime(2017, 7, 7),
        'percent_of_graph_utilization': 123.0,
        'percent_of_graph_utilization_updated_time': datetime(2016, 6, 6)
    },
  ]
members:
  description: Lists of the graph members.
  returned: when `list_members`, and `graph_arn` are defined and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'email_address': 'string',
        'graph_arn': 'string',
        'master_id': 'string',
        'status': 'INVITED',
        'disabled_reason': 'VOLUME_TOO_HIGH',
        'invited_time': datetime(2015, 1, 1),
        'updated_time': datetime(2017, 7, 7),
        'percent_of_graph_utilization': 123.0,
        'percent_of_graph_utilization_updated_time': datetime(2016, 6, 6)
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _detective(client, module):
    try:
        if module.params['list_invitations']:
            if client.can_paginate('list_invitations'):
                paginator = client.get_paginator('list_invitations')
                return paginator.paginate(), True
            else:
                return client.list_invitations(), False
        elif module.params['list_members']:
            if client.can_paginate('list_members'):
                paginator = client.get_paginator('list_members')
                return paginator.paginate(
                    GraphArn=module.params['graph_arn'],
                ), True
            else:
                return client.list_members(
                    GraphArn=module.params['graph_arn'],
                ), False
        else:
            if client.can_paginate('list_graphs'):
                paginator = client.get_paginator('list_graphs')
                return paginator.paginate(), True
            else:
                return client.list_graphs(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS detective details')


def main():
    argument_spec = dict(
        graph_arn=dict(required=False),
        list_invitations=dict(required=False, type=bool),
        list_members=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_members', True, ['graph_arn']),
        ),
        mutually_exclusive=[
            (
                'list_invitations',
                'list_members',
            )
        ],
    )

    client = module.client('detective', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _detective(client, module)

    if module.params['list_invitations']:
        module.exit_json(invitations=aws_response_list_parser(paginate, _it, 'Invitations'))
    elif module.params['list_members']:
        module.exit_json(members=aws_response_list_parser(paginate, _it, 'MemberDetails'))
    else:
        module.exit_json(graph_list=aws_response_list_parser(paginate, _it, 'GraphList'))


if __name__ == '__main__':
    main()
