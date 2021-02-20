#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kafka_info
short_description: Get Information about Amazon MSK cluster.
description:
  - Get Information about Amazon MSK cluster.
  - U(https://docs.aws.amazon.com/msk/1.0/apireference/resources.html)
version_added: 0.0.7
options:
  arn:
    description:
      - can be config arn?
      - can be cluster arn?
    required: false
    type: str
    aliases: ['config_arn', 'cluster_arn']
  list_cluster_operations:
    description:
      - do you want to get list of cluster_operations for given cluster I(arn)?
    required: false
    type: bool
  list_clusters:
    description:
      - do you want to get list of clusters?
    required: false
    type: bool
  list_configuration_revisions:
    description:
      - do you want to get list of configuration revisions for given config I(arn)?
    required: false
    type: bool
  list_configurations:
    description:
      - do you want to get list of configurations?
    required: false
    type: bool
  list_nodes:
    description:
      - do you want to get list of nodes for given cluster I(arn)?
    required: false
    type: bool
  list_scram_secrets:
    description:
      - do you want to get list of scram secrets for given cluster I(arn)?
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
- name: "get list of cluster_operations"
  aws_kafka_info:
    list_cluster_operations: true
    arn: 'cluster-arn'

- name: "get list of clusters"
  aws_kafka_info:
    list_clusters: true

- name: "get list of configuration_revisions"
  aws_kafka_info:
    list_configuration_revisions: true
    arn: 'configuration-arn'

- name: "get list of configurations"
  aws_kafka_info:
    list_configurations: true

- name: "get list of nodes"
  aws_kafka_info:
    list_nodes: true
    arn: 'cluster-arn'

- name: "get list of scram_secrets"
  aws_kafka_info:
    list_scram_secrets: true
    arn: 'cluster-arn'
"""

RETURN = """
cluster_operations:
  description: list of cluster_operations.
  returned: when `list_cluster_operations` is defined and success.
  type: list
clusters:
  description: list of clusters.
  returned: when `list_clusters` is defined and success.
  type: list
configuration_revisions:
  description: list of configuration_revisions.
  returned: when `list_configuration_revisions` is defined and success.
  type: list
configurations:
  description: list of configurations.
  returned: when `list_configurations` is defined and success.
  type: list
nodes:
  description: list of nodes.
  returned: when `list_nodes` is defined and success.
  type: list
scram_secrets:
  description: list of scram_secrets.
  returned: when `list_scram_secrets` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kafka(client, module):
    try:
        if module.params['list_cluster_operations']:
            if client.can_paginate('list_cluster_operations'):
                paginator = client.get_paginator('list_cluster_operations')
                return paginator.paginate(
                    ClusterArn=module.params['arn']
                ), True
            else:
                return client.list_cluster_operations(
                    ClusterArn=module.params['arn']
                ), False
        elif module.params['list_clusters']:
            if client.can_paginate('list_clusters'):
                paginator = client.get_paginator('list_clusters')
                return paginator.paginate(), True
            else:
                return client.list_clusters(), False
        elif module.params['list_configuration_revisions']:
            if client.can_paginate('list_configuration_revisions'):
                paginator = client.get_paginator('list_configuration_revisions')
                return paginator.paginate(
                    Arn=module.params['arn']
                ), True
            else:
                return client.list_configuration_revisions(
                    Arn=module.params['arn']
                ), False
        elif module.params['list_configurations']:
            if client.can_paginate('list_configurations'):
                paginator = client.get_paginator('list_configurations')
                return paginator.paginate(), True
            else:
                return client.list_configurations(), False
        elif module.params['list_nodes']:
            if client.can_paginate('list_nodes'):
                paginator = client.get_paginator('list_nodes')
                return paginator.paginate(
                    ClusterArn=module.params['arn']
                ), True
            else:
                return client.list_nodes(
                    ClusterArn=module.params['arn']
                ), False
        elif module.params['list_scram_secrets']:
            if client.can_paginate('list_scram_secrets'):
                paginator = client.get_paginator('list_scram_secrets')
                return paginator.paginate(
                    ClusterArn=module.params['arn']
                ), True
            else:
                return client.list_scram_secrets(
                    ClusterArn=module.params['arn']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon kafka details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['config_arn', 'cluster_arn']),
        list_cluster_operations=dict(required=False, type=bool),
        list_clusters=dict(required=False, type=bool),
        list_configuration_revisions=dict(required=False, type=bool),
        list_configurations=dict(required=False, type=bool),
        list_nodes=dict(required=False, type=bool),
        list_scram_secrets=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_cluster_operations', True, ['arn']),
            ('list_configuration_revisions', True, ['arn']),
            ('list_nodes', True, ['arn']),
            ('list_scram_secrets', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_cluster_operations',
                'list_clusters',
                'list_configuration_revisions',
                'list_configurations',
                'list_nodes',
                'list_scram_secrets',
            )
        ],
    )

    client = module.client('kafka', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kafka(client, module)

    if module.params['list_cluster_operations']:
        module.exit_json(cluster_operations=aws_response_list_parser(paginate, it, 'ClusterOperationInfoList'))
    elif module.params['list_clusters']:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'ClusterInfoList'))
    elif module.params['list_configuration_revisions']:
        module.exit_json(configuration_revisions=aws_response_list_parser(paginate, it, 'Revisions'))
    elif module.params['list_configurations']:
        module.exit_json(configurations=aws_response_list_parser(paginate, it, 'Configurations'))
    elif module.params['list_nodes']:
        module.exit_json(nodes=aws_response_list_parser(paginate, it, 'NodeInfoList'))
    elif module.params['list_scram_secrets']:
        module.exit_json(scram_secrets=aws_response_list_parser(paginate, it, 'SecretArnList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
