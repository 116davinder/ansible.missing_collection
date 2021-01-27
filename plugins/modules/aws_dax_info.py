#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dax_info
short_description: Get Information about AWS Dax.
description:
  - Get Information about AWS Dax.
  - U(https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB_Accelerator_(DAX).html)
version_added: 0.0.5
options:
  cluster_names:
    description:
      -  names of dax clusters.
    required: false
    type: list
    default: []
  parameter_group_names:
    description:
      -  names of dax parameter groups.
    required: false
    type: list
    default: []
  subnet_group_names:
    description:
      -  names of dax subnet groups.
    required: false
    type: list
    default: []
  parameter_group_name:
    description:
      -  name of parameter group name.
    required: false
    type: str
  source_name:
    description:
      -  name of the source event.
    required: false
    type: str
  source_type:
    description:
      -  type of source event.
    required: false
    type: str
    choices: ['CLUSTER', 'PARAMETER_GROUP', 'SUBNET_GROUP']
  describe_clusters:
    description:
      - do you want to describe list of dax clusters of given I(cluster_names)?
    required: false
    type: bool
  describe_default_parameters:
    description:
      - do you want to describe default parameters?
    required: false
    type: bool
  describe_events:
    description:
      - do you want to describe dax events of given I(source_name) and I(source_type)?
    required: false
    type: bool
  describe_parameter_groups:
    description:
      - do you want to describe dax parameter groups of given I(parameter_group_names)?
    required: false
    type: bool
  describe_parameters:
    description:
      - do you want to describe dax parameter group name of given I(parameter_group_name)?
    required: false
    type: bool
  describe_subnet_groups:
    description:
      - do you want to describe dax subnet groups for given I(subnet_group_names)?
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
- name: "Lists all of the dax clusters."
  aws_dax_info:
    describe_clusters: true
    cluster_names: []

- name: "Lists all of default parameters."
  aws_dax_info:
    describe_default_parameters: true

- name: "Lists of the dax events."
  aws_dax_info:
    describe_events: true
    source_name: 'test'
    source_type: 'CLUSTER'

- name: "Lists all of the dax parameter groups."
  aws_dax_info:
    describe_parameter_groups: true
    parameter_group_names: []

- name: "describe dax parameters of a parameter group name"
  aws_dax_info:
    describe_parameters: true
    parameter_group_name: 'test'

- name: "describe dax subnet groups."
  aws_dax_info:
    describe_subnet_groups: true
    subnet_group_names: []
"""

RETURN = """
clusters:
  description: Lists all of the dax clusters.
  returned: when `describe_clusters` and `cluster_names` defined and success
  type: list
  sample: [
    {
        'cluster_name': 'string',
        'description': 'string',
        'cluster_arn': 'string',
        'total_nodes': 123,
        'active_nodes': 1234,
        'node_type': 'string',
        'status': 'string',
        'cluster_discovery_endpoint': {},
        'node_ids_to_remove': [],
        'nodes': [],
        'preferred_maintenance_window': 'string',
        'notification_configuration': {},
        'subnet_group': 'string',
        'security_groups': [],
        'aam_role_Arn': 'string',
        'parameter_group': {},
        'sse_description': {}
    },
  ]
parameters:
  description: Lists all of default parameters.
  returned: when `describe_default_parameters` is defined and success
  type: list
  sample: [
    {
        'parameter_name': 'string',
        'parameter_type': 'DEFAULT',
        'parameter_value': 'string',
        'node_type_specific_values': [],
        'description': 'string',
        'source': 'string',
        'data_type': 'string',
        'allowed_values': 'string',
        'is_modifiable': 'TRUE',
        'change_type': 'IMMEDIATE'
    },
  ]
events:
  description: Lists of the dax events.
  returned: when `describe_events`, `source_type`, and `source_name` are defined and success
  type: list
  sample: [
    {
        'source_name': 'string',
        'source_type': 'CLUSTER',
        'message': 'string',
        'date': datetime(2015, 1, 1)
    },
  ]
parameter_groups:
  description: Lists all of the dax parameter groups.
  returned: when `describe_parameter_groups` and `parameter_group_names` is defined and success
  type: list
  sample: [
    {
        'parameter_group_name': 'string',
        'description': 'string'
    },
  ]
parameter:
  description: describe dax parameters of a parameter group name.
  returned: when `describe_parameters`, and `parameter_group_name` are defined and success
  type: list
  sample: [
    {
        'parameter_name': 'string',
        'parameter_type': 'DEFAULT',
        'parameter_value': 'string',
        'node_type_specific_values': [],
        'description': 'string',
        'source': 'string',
        'data_type': 'string',
        'allowed_values': 'string',
        'is_modifiable': 'TRUE',
        'change_type': 'IMMEDIATE'
    },
  ]
subnet_groups:
  description: describe dax subnet groups.
  returned: when `describe_subnet_groups`, and `subnet_group_names` are defined and success
  type: list
  sample: [
    {
        'subnet_group_name': 'string',
        'description': 'string',
        'vpc_id': 'string',
        'subnets': [
            {
                'subnet_identifier': 'string',
                'subnet_availability_zone': 'string'
            },
        ]
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _dax(client, module):
    try:
        if module.params['describe_clusters']:
            if client.can_paginate('describe_clusters'):
                paginator = client.get_paginator('describe_clusters')
                return paginator.paginate(
                    ClusterNames=module.params['cluster_names'],
                ), True
            else:
                return client.describe_clusters(
                    ClusterNames=module.params['cluster_names'],
                ), False
        elif module.params['describe_default_parameters']:
            if client.can_paginate('describe_default_parameters'):
                paginator = client.get_paginator('describe_default_parameters')
                return paginator.paginate(), True
            else:
                return client.describe_default_parameters(), False
        elif module.params['describe_events']:
            if client.can_paginate('describe_events'):
                paginator = client.get_paginator('describe_events')
                return paginator.paginate(
                    SourceName=module.params['source_name'],
                    SourceType=module.params['source_type'],
                ), True
            else:
                return client.describe_events(
                    SourceName=module.params['source_name'],
                    SourceType=module.params['source_type'],
                ), False
        elif module.params['describe_parameter_groups']:
            if client.can_paginate('describe_parameter_groups'):
                paginator = client.get_paginator('describe_parameter_groups')
                return paginator.paginate(
                    ParameterGroupNames=module.params['parameter_group_names'],
                ), True
            else:
                return client.describe_parameter_groups(
                    ParameterGroupNames=module.params['parameter_group_names'],
                ), False
        elif module.params['describe_parameters']:
            return client.describe_parameters(
                ParameterGroupName=module.params['parameter_group_name'],
            ), False
        elif module.params['describe_subnet_groups']:
            if client.can_paginate('describe_subnet_groups'):
                paginator = client.get_paginator('describe_subnet_groups')
                return paginator.paginate(
                    SubnetGroupNames=module.params['subnet_group_names'],
                ), True
            else:
                return client.describe_subnet_groups(
                    SubnetGroupNames=module.params['subnet_group_names'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Dax details')


def main():
    argument_spec = dict(
        cluster_names=dict(required=False, type=list, default=[]),
        parameter_group_names=dict(required=False, type=list, default=[]),
        subnet_group_names=dict(required=False, type=list, default=[]),
        parameter_group_name=dict(required=False),
        source_name=dict(required=False),
        source_type=dict(required=False, choices=['CLUSTER', 'PARAMETER_GROUP', 'SUBNET_GROUP']),
        describe_clusters=dict(required=False, type=bool),
        describe_default_parameters=dict(required=False, type=bool),
        describe_events=dict(required=False, type=bool),
        describe_parameter_groups=dict(required=False, type=bool),
        describe_parameters=dict(required=False, type=bool),
        describe_subnet_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_events', True, ['source_name', 'source_type']),
            ('describe_parameters', True, ['parameter_group_name'])
        ),
        mutually_exclusive=[
            (
                'describe_clusters',
                'describe_default_parameters',
                'describe_events',
                'describe_parameter_groups',
                'describe_parameters',
                'describe_subnet_groups',
            )
        ],
    )

    client = module.client('dax', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _dax(client, module)

    if module.params['describe_clusters']:
        module.exit_json(clusters=aws_response_list_parser(paginate, _it, 'Clusters'))
    elif module.params['describe_default_parameters']:
        module.exit_json(parameters=aws_response_list_parser(paginate, _it, 'Parameters'))
    elif module.params['describe_events']:
        module.exit_json(events=aws_response_list_parser(paginate, _it, 'Events'))
    elif module.params['describe_parameter_groups']:
        module.exit_json(parameter_groups=aws_response_list_parser(paginate, _it, 'ParameterGroups'))
    elif module.params['describe_parameters']:
        module.exit_json(parameter=camel_dict_to_snake_dict(_it['Parameters']))
    elif module.params['describe_subnet_groups']:
        module.exit_json(subnet_groups=aws_response_list_parser(paginate, _it, 'SubnetGroups'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
