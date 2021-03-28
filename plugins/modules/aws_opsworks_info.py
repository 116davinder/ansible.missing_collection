#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_opsworks_info
short_description: Get Information about Amazon OpsWorks.
description:
  - Get Information about Amazon OpsWorks.
  - U(https://docs.aws.amazon.com/opsworks/latest/apiref/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of opsworks stack.
    required: false
    type: str
    aliases: ['stack_id']
  describe_apps:
    description:
      - do you want to get list of apps for given I(id)?
    required: false
    type: bool
  describe_deployments:
    description:
      - do you want to get deployments for given I(id)?
    required: false
    type: bool
  describe_ecs_clusters:
    description:
      - do you want to get list of ecs_clusters for given I(id)?
    required: false
    type: bool
  describe_elastic_ips:
    description:
      - do you want to get elastic_ips for given I(id)?
    required: false
    type: bool
  describe_elastic_load_balancers:
    description:
      - do you want to get elastic_load_balancers for given I(id)?
    required: false
    type: bool
  describe_instances:
    description:
      - do you want to get instances for given I(id)?
    required: false
    type: bool
  describe_layers:
    description:
      - do you want to get layers for given I(id)?
    required: false
    type: bool
  describe_raid_arrays:
    description:
      - do you want to get raid_arrays for given I(id)?
    required: false
    type: bool
  describe_rds_db_instances:
    description:
      - do you want to get rds_db_instances for given I(id)?
    required: false
    type: bool
  describe_stacks:
    description:
      - do you want to get stacks?
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
- name: "get list of apps"
  aws_opsworks_info:
    describe_apps: true
    id: 'stack_id'

- name: "get deployments"
  aws_opsworks_info:
    describe_deployments: true
    id: 'stack_id'

- name: "get list of ecs_clusters"
  aws_opsworks_info:
    describe_ecs_clusters: true
    id: 'stack_id'

- name: "get elastic_ips"
  aws_opsworks_info:
    describe_elastic_ips: true
    id: 'stack_id'

- name: "get elastic_load_balancers"
  aws_opsworks_info:
    describe_elastic_load_balancers: true

- name: "get instances"
  aws_opsworks_info:
    describe_instances: true
    id: 'stack_id'

- name: "get layers"
  aws_opsworks_info:
    describe_layers: true
    id: 'stack_id'

- name: "get raid_arrays"
  aws_opsworks_info:
    describe_raid_arrays: true
    id: 'stack_id'

- name: "get rds_db_instances"
  aws_opsworks_info:
    describe_rds_db_instances: true
    id: 'stack_id'

- name: "get stacks"
  aws_opsworks_info:
    describe_stacks: true
"""

RETURN = """
apps:
  description: list of apps.
  returned: when `describe_apps` is defined and success.
  type: list
deployments:
  description: get of deployments.
  returned: when `describe_deployments` is defined and success.
  type: list
ecs_clusters:
  description: list of ecs_clusters.
  returned: when `describe_ecs_clusters` is defined and success.
  type: list
elastic_ips:
  description: list of elastic_ips.
  returned: when `describe_elastic_ips` is defined and success.
  type: list
elastic_load_balancers:
  description: list of elastic_load_balancers.
  returned: when `describe_elastic_load_balancers` is defined and success.
  type: list
instances:
  description: list of instances.
  returned: when `describe_instances` is defined and success.
  type: list
layers:
  description: list of layers.
  returned: when `describe_layers` is defined and success.
  type: list
raid_arrays:
  description: list of raid_arrays.
  returned: when `describe_raid_arrays` is defined and success.
  type: list
rds_db_instances:
  description: list of rds_db_instances.
  returned: when `describe_rds_db_instances` is defined and success.
  type: list
stacks:
  description: list of stacks.
  returned: when `describe_stacks` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _opsworks(client, module):
    try:
        if module.params['describe_apps']:
            if client.can_paginate('describe_apps'):
                paginator = client.get_paginator('describe_apps')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_apps(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_deployments']:
            if client.can_paginate('describe_deployments'):
                paginator = client.get_paginator('describe_deployments')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_deployments(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_ecs_clusters']:
            if client.can_paginate('describe_ecs_clusters'):
                paginator = client.get_paginator('describe_ecs_clusters')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_ecs_clusters(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_elastic_ips']:
            if client.can_paginate('describe_elastic_ips'):
                paginator = client.get_paginator('describe_elastic_ips')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_elastic_ips(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_elastic_load_balancers']:
            if client.can_paginate('describe_elastic_load_balancers'):
                paginator = client.get_paginator('describe_elastic_load_balancers')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_elastic_load_balancers(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_instances']:
            if client.can_paginate('describe_instances'):
                paginator = client.get_paginator('describe_instances')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_instances(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_layers']:
            if client.can_paginate('describe_layers'):
                paginator = client.get_paginator('describe_layers')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_layers(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_raid_arrays']:
            if client.can_paginate('describe_raid_arrays'):
                paginator = client.get_paginator('describe_raid_arrays')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_raid_arrays(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_rds_db_instances']:
            if client.can_paginate('describe_rds_db_instances'):
                paginator = client.get_paginator('describe_rds_db_instances')
                return paginator.paginate(
                    StackId=module.params['id']
                ), True
            else:
                return client.describe_rds_db_instances(
                    StackId=module.params['id']
                ), False
        elif module.params['describe_stacks']:
            if client.can_paginate('describe_stacks'):
                paginator = client.get_paginator('describe_stacks')
                return paginator.paginate(), True
            else:
                return client.describe_stacks(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon OpsWorks details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['stack_id']),
        describe_apps=dict(required=False, type=bool),
        describe_deployments=dict(required=False, type=bool),
        describe_ecs_clusters=dict(required=False, type=bool),
        describe_elastic_ips=dict(required=False, type=bool),
        describe_elastic_load_balancers=dict(required=False, type=bool),
        describe_instances=dict(required=False, type=bool),
        describe_layers=dict(required=False, type=bool),
        describe_raid_arrays=dict(required=False, type=bool),
        describe_rds_db_instances=dict(required=False, type=bool),
        describe_stacks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_apps', True, ['id']),
            ('describe_deployments', True, ['id']),
            ('describe_ecs_clusters', True, ['id']),
            ('describe_elastic_ips', True, ['id']),
            ('describe_elastic_load_balancers', True, ['id']),
            ('describe_instances', True, ['id']),
            ('describe_layers', True, ['id']),
            ('describe_raid_arrays', True, ['id']),
            ('describe_rds_db_instances', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_apps',
                'describe_deployments',
                'describe_ecs_clusters',
                'describe_elastic_ips',
                'describe_elastic_load_balancers',
                'describe_instances',
                'describe_layers',
                'describe_raid_arrays',
                'describe_rds_db_instances',
                'describe_stacks',
            )
        ],
    )

    client = module.client('opsworks', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _opsworks(client, module)

    if module.params['describe_apps']:
        module.exit_json(apps=aws_response_list_parser(paginate, it, 'Apps'))
    elif module.params['describe_deployments']:
        module.exit_json(deployments=aws_response_list_parser(paginate, it, 'Deployments'))
    elif module.params['describe_ecs_clusters']:
        module.exit_json(ecs_clusters=aws_response_list_parser(paginate, it, 'EcsClusters'))
    elif module.params['describe_elastic_ips']:
        module.exit_json(elastic_ips=aws_response_list_parser(paginate, it, 'ElasticIps'))
    elif module.params['describe_elastic_load_balancers']:
        module.exit_json(elastic_load_balancers=aws_response_list_parser(paginate, it, 'ElasticLoadBalancers'))
    elif module.params['describe_instances']:
        module.exit_json(instances=aws_response_list_parser(paginate, it, 'Instances'))
    elif module.params['describe_layers']:
        module.exit_json(layers=aws_response_list_parser(paginate, it, 'Layers'))
    elif module.params['describe_raid_arrays']:
        module.exit_json(raid_arrays=aws_response_list_parser(paginate, it, 'RaidArrays'))
    elif module.params['describe_rds_db_instances']:
        module.exit_json(rds_db_instances=aws_response_list_parser(paginate, it, 'RdsDbInstances'))
    elif module.params['describe_stacks']:
        module.exit_json(stacks=aws_response_list_parser(paginate, it, 'Stacks'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
