#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_emr_info
short_description: Get Information about Amazon Elastic MapReduce (EMR).
description:
  - Get Information about Amazon Elastic MapReduce (EMR).
  - U(https://docs.aws.amazon.com/emr/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of emr cluster.
    required: false
    type: str
  cluster_states:
    description:
      - list of cluster states to filter results.
      - can be combination of following 'STARTING', 'BOOTSTRAPPING', 'RUNNING',
        'WAITING', 'TERMINATING', 'TERMINATED', 'TERMINATED_WITH_ERRORS'
    required: false
    type: list
  list_bootstrap_actions:
    description:
      - do you want to get list of bootstrap actions for given I(id)?
    required: false
    type: bool
  list_instance_fleets:
    description:
      - do you want to get list of instance fleets for given I(id)?
    required: false
    type: bool
  list_instance_groups:
    description:
      - do you want to get list of instance groups for given I(id)?
    required: false
    type: bool
  list_steps:
    description:
      - do you want to get list of steps for given I(id)?
    required: false
    type: bool
  list_studios:
    description:
      - do you want to get list of studios for given I(id)?
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
- name: "get list of all emr clusters"
  aws_emr_info:
  register: _reg

- name: "get list of bootstrap actions"
  aws_emr_info:
    list_bootstrap_actions: true
    id: 'test'

- name: "get list of instance fleets"
  aws_emr_info:
    list_instance_fleets: true
    id: 'test'

- name: "get list of instance groups"
  aws_emr_info:
    list_instance_groups: true
    id: 'test'

- name: "get list of steps"
  aws_emr_info:
    list_steps: true
    id: 'test'

- name: "get list of studios"
  aws_emr_info:
    list_studios: true
    id: 'test'
"""

RETURN = """
clusters:
  description: list of all emr clusters.
  returned: when no arguments are defined and success
  type: list
bootstrap_actions:
  description: list of bootstrap actions.
  returned: when `list_bootstrap_actions` is defined and success
  type: list
instance_fleets:
  description: list of instance fleets.
  returned: when `list_instance_fleets` is defined and success
  type: list
instance_groups:
  description: list of instance groups.
  returned: when `list_instance_groups` is defined and success
  type: list
steps:
  description: list of steps.
  returned: when `list_steps` is defined and success
  type: list
studios:
  description: list of studios.
  returned: when `list_studios` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _emr(client, module):
    try:
        if module.params['list_bootstrap_actions']:
            if client.can_paginate('list_bootstrap_actions'):
                paginator = client.get_paginator('list_bootstrap_actions')
                return paginator.paginate(
                    ClusterId=module.params['id']
                ), True
            else:
                return client.list_bootstrap_actions(
                    ClusterId=module.params['id']
                ), False
        elif module.params['list_instance_fleets']:
            if client.can_paginate('list_instance_fleets'):
                paginator = client.get_paginator('list_instance_fleets')
                return paginator.paginate(
                    ClusterId=module.params['id']
                ), True
            else:
                return client.list_instance_fleets(
                    ClusterId=module.params['id']
                ), False
        elif module.params['list_instance_groups']:
            if client.can_paginate('list_instance_groups'):
                paginator = client.get_paginator('list_instance_groups')
                return paginator.paginate(
                    ClusterId=module.params['id']
                ), True
            else:
                return client.list_instance_groups(
                    ClusterId=module.params['id']
                ), False
        elif module.params['list_steps']:
            if client.can_paginate('list_steps'):
                paginator = client.get_paginator('list_steps')
                return paginator.paginate(
                    ClusterId=module.params['id']
                ), True
            else:
                return client.list_steps(
                    ClusterId=module.params['id']
                ), False
        elif module.params['list_studios']:
            if client.can_paginate('list_studios'):
                paginator = client.get_paginator('list_studios')
                return paginator.paginate(), True
            else:
                return client.list_studios(), False
        else:
            if client.can_paginate('list_clusters'):
                paginator = client.get_paginator('list_clusters')
                return paginator.paginate(
                    ClusterStates=module.params['cluster_states']
                ), True
            else:
                return client.list_clusters(
                    ClusterStates=module.params['cluster_states']
                ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS EMR details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        cluster_states=dict(
            required=False,
            type=list,
            default=[]
        ),
        list_bootstrap_actions=dict(required=False, type=bool),
        list_instance_fleets=dict(required=False, type=bool),
        list_instance_groups=dict(required=False, type=bool),
        list_steps=dict(required=False, type=bool),
        list_studios=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_bootstrap_actions', True, ['id']),
            ('list_instance_fleets', True, ['id']),
            ('list_steps', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_bootstrap_actions',
                'list_instance_fleets',
                'list_instance_groups',
                'list_steps',
                'list_studios',
            )
        ],
    )

    client = module.client('emr', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _emr(client, module)

    if module.params['list_bootstrap_actions']:
        module.exit_json(bootstrap_actions=aws_response_list_parser(paginate, it, 'BootstrapActions'))
    elif module.params['list_instance_fleets']:
        module.exit_json(instance_fleets=aws_response_list_parser(paginate, it, 'InstanceFleets'))
    elif module.params['list_instance_groups']:
        module.exit_json(instance_groups=aws_response_list_parser(paginate, it, 'InstanceGroups'))
    elif module.params['list_steps']:
        module.exit_json(steps=aws_response_list_parser(paginate, it, 'Steps'))
    elif module.params['list_studios']:
        module.exit_json(studios=aws_response_list_parser(paginate, it, 'Studios'))
    else:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'Clusters'))


if __name__ == '__main__':
    main()
