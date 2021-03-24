#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_neptune_info
short_description: Get Information about Amazon Neptune.
description:
  - Get Information about Amazon Neptune.
  - U(https://docs.aws.amazon.com/neptune/latest/apiref/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of db cluster.
    required: false
    type: str
    aliases: ['db_cluster_identifier']
  name:
    description:
      - name of db cluster parameter group.
    required: false
    type: str
    aliases: ['db_cluster_parameter_group_name']
  describe_db_cluster_endpoints:
    description:
      - do you want to get list of db_cluster_endpoints for given I(id)?
    required: false
    type: bool
  describe_db_cluster_parameter_groups:
    description:
      - do you want to get db_cluster_parameter_groups?
    required: false
    type: bool
  describe_db_cluster_parameters:
    description:
      - do you want to get list of db_cluster_parameters for given I(name)?
    required: false
    type: bool
  describe_db_cluster_snapshots:
    description:
      - do you want to get db_cluster_snapshots for given I(id)?
    required: false
    type: bool
  describe_db_clusters:
    description:
      - do you want to get db_clusters?
    required: false
    type: bool
  describe_db_instances:
    description:
      - do you want to get db_instances for given I(id)?
    required: false
    type: bool
  describe_db_parameter_groups:
    description:
      - do you want to get db_parameter_groups?
    required: false
    type: bool
  describe_db_subnet_groups:
    description:
      - do you want to get db_subnet_groups?
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
- name: "get list of db_cluster_endpoints"
  aws_neptune_info:
    describe_db_cluster_endpoints: true
    id: 'db_cluster_identifier'

- name: "get db_cluster_parameter_groups"
  aws_neptune_info:
    describe_db_cluster_parameter_groups: true

- name: "get list of db_cluster_parameters"
  aws_neptune_info:
    describe_db_cluster_parameters: true
    name: 'db_cluster_parameter_group_name'

- name: "get db_cluster_snapshots"
  aws_neptune_info:
    describe_db_cluster_snapshots: true
    id: 'db_cluster_identifier'

- name: "get db_clusters"
  aws_neptune_info:
    describe_db_clusters: true

- name: "get db_instances"
  aws_neptune_info:
    describe_db_instances: true
    id: 'db_cluster_identifier'

- name: "get db_parameter_groups"
  aws_neptune_info:
    describe_db_parameter_groups: true

- name: "get db_subnet_groups"
  aws_neptune_info:
    describe_db_subnet_groups: true
"""

RETURN = """
db_cluster_endpoints:
  description: list of db_cluster_endpoints.
  returned: when `describe_db_cluster_endpoints` is defined and success.
  type: list
db_cluster_parameter_groups:
  description: get of db_cluster_parameter_groups.
  returned: when `describe_db_cluster_parameter_groups` is defined and success.
  type: list
db_cluster_parameters:
  description: list of db_cluster_parameters.
  returned: when `describe_db_cluster_parameters` is defined and success.
  type: list
db_cluster_snapshots:
  description: list of db_cluster_snapshots.
  returned: when `describe_db_cluster_snapshots` is defined and success.
  type: list
db_clusters:
  description: list of db_clusters.
  returned: when `describe_db_clusters` is defined and success.
  type: list
db_instances:
  description: list of db_instances.
  returned: when `describe_db_instances` is defined and success.
  type: list
db_parameter_groups:
  description: list of db_parameter_groups.
  returned: when `describe_db_parameter_groups` is defined and success.
  type: list
db_subnet_groups:
  description: list of db_subnet_groups.
  returned: when `describe_db_subnet_groups` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _neptune(client, module):
    try:
        if module.params['describe_db_cluster_endpoints']:
            if client.can_paginate('describe_db_cluster_endpoints'):
                paginator = client.get_paginator('describe_db_cluster_endpoints')
                return paginator.paginate(
                    DBClusterIdentifier=module.params['id']
                ), True
            else:
                return client.describe_db_cluster_endpoints(
                    DBClusterIdentifier=module.params['id']
                ), False
        elif module.params['describe_db_cluster_parameter_groups']:
            if client.can_paginate('describe_db_cluster_parameter_groups'):
                paginator = client.get_paginator('describe_db_cluster_parameter_groups')
                return paginator.paginate(), True
            else:
                return client.describe_db_cluster_parameter_groups(), False
        elif module.params['describe_db_cluster_parameters']:
            if client.can_paginate('describe_db_cluster_parameters'):
                paginator = client.get_paginator('describe_db_cluster_parameters')
                return paginator.paginate(
                    DBClusterParameterGroupName=module.params['name']
                ), True
            else:
                return client.describe_db_cluster_parameters(
                    DBClusterParameterGroupName=module.params['name']
                ), False
        elif module.params['describe_db_cluster_snapshots']:
            if client.can_paginate('describe_db_cluster_snapshots'):
                paginator = client.get_paginator('describe_db_cluster_snapshots')
                return paginator.paginate(
                    DBClusterIdentifier=module.params['id']
                ), True
            else:
                return client.describe_db_cluster_snapshots(
                    DBClusterIdentifier=module.params['id']
                ), False
        elif module.params['describe_db_clusters']:
            if client.can_paginate('describe_db_clusters'):
                paginator = client.get_paginator('describe_db_clusters')
                return paginator.paginate(), True
            else:
                return client.describe_db_clusters(), False
        elif module.params['describe_db_instances']:
            if client.can_paginate('describe_db_instances'):
                paginator = client.get_paginator('describe_db_instances')
                return paginator.paginate(
                    Filters=[
                        {
                            'Name': 'db-cluster-id',
                            'Values': [module.params['id']]
                        },
                    ]
                ), True
            else:
                return client.describe_db_instances(
                    Filters=[
                        {
                            'Name': 'db-cluster-id',
                            'Values': [module.params['id']]
                        },
                    ]
                ), False
        elif module.params['describe_db_parameter_groups']:
            if client.can_paginate('describe_db_parameter_groups'):
                paginator = client.get_paginator('describe_db_parameter_groups')
                return paginator.paginate(), True
            else:
                return client.describe_db_parameter_groups(), False
        elif module.params['describe_db_subnet_groups']:
            if client.can_paginate('describe_db_subnet_groups'):
                paginator = client.get_paginator('describe_db_subnet_groups')
                return paginator.paginate(), True
            else:
                return client.describe_db_subnet_groups(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Neptune details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['db_cluster_identifier']),
        name=dict(required=False, aliases=['db_cluster_parameter_group_name']),
        describe_db_cluster_endpoints=dict(required=False, type=bool),
        describe_db_cluster_parameter_groups=dict(required=False, type=bool),
        describe_db_cluster_parameters=dict(required=False, type=bool),
        describe_db_cluster_snapshots=dict(required=False, type=bool),
        describe_db_clusters=dict(required=False, type=bool),
        describe_db_instances=dict(required=False, type=bool),
        describe_db_parameter_groups=dict(required=False, type=bool),
        describe_db_subnet_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_db_cluster_endpoints', True, ['id']),
            ('describe_db_cluster_parameters', True, ['name']),
            ('describe_db_cluster_snapshots', True, ['id']),
            ('describe_db_instances', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_db_cluster_endpoints',
                'describe_db_cluster_parameter_groups',
                'describe_db_cluster_parameters',
                'describe_db_cluster_snapshots',
                'describe_db_clusters',
                'describe_db_instances',
                'describe_db_parameter_groups',
                'describe_db_subnet_groups',
            )
        ],
    )

    client = module.client('neptune', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _neptune(client, module)

    if module.params['describe_db_cluster_endpoints']:
        module.exit_json(db_cluster_endpoints=aws_response_list_parser(paginate, it, 'DBClusterEndpoints'))
    elif module.params['describe_db_cluster_parameter_groups']:
        module.exit_json(db_cluster_parameter_groups=aws_response_list_parser(paginate, it, 'DBClusterParameterGroups'))
    elif module.params['describe_db_cluster_parameters']:
        module.exit_json(db_cluster_parameters=aws_response_list_parser(paginate, it, 'Parameters'))
    elif module.params['describe_db_cluster_snapshots']:
        module.exit_json(db_cluster_snapshots=aws_response_list_parser(paginate, it, 'DBClusterSnapshots'))
    elif module.params['describe_db_clusters']:
        module.exit_json(db_clusters=aws_response_list_parser(paginate, it, 'DBClusters'))
    elif module.params['describe_db_instances']:
        module.exit_json(db_instances=aws_response_list_parser(paginate, it, 'DBInstances'))
    elif module.params['describe_db_parameter_groups']:
        module.exit_json(db_parameter_groups=aws_response_list_parser(paginate, it, 'DBParameterGroups'))
    elif module.params['describe_db_subnet_groups']:
        module.exit_json(db_subnet_groups=aws_response_list_parser(paginate, it, 'DBSubnetGroups'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
