#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_eks_cluster_info
short_description: Get Information about AWS EKS Clusters.
description:
  - Get Information about AWS EKS Clusters.
version_added: 0.0.2
options:
  name:
    description:
      - name of the eks cluster
    required: false
    type: str
    aliases: ['cluster_name']
  list_fargate_profiles:
    description:
      - do you want to fetch fargate profiles for given eks cluster
    required: false
    type: bool
  list_nodegroups:
    description:
      - do you want to fetch node groups for given eks cluster
    required: false
    type: bool
  list_addons:
    description:
      - do you want to fetch addons for given eks cluster
    required: false
    type: bool
  describe_cluster:
    description:
      - do you want to describe / fetch all attributes of given eks cluster
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
- name: "get list of eks clusters"
  aws_eks_cluster_info:
  register: __all

- name: "get fargate profiles for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_fargate_profiles: true

- name: "get nodegroups for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_nodegroups: true

- name: "get list of addons for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_addons: true

- name: "get details about given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    describe_cluster: true
"""

RETURN = """
clusters:
  description: List of EKS Cluster.
  returned: when no argument is defined and success
  type: list
  sample: ["test-eks-cluster1", "test-eks-cluster2"]
fargate_profile_names:
  description: List of Fargate Profiles for given EKS Cluster.
  returned: when I(fargate_profile_names) and success
  type: list
  sample: ["test-fg"]
node_groups:
  description: List of Node Groups for given EKS Cluster.
  returned: when I(list_nodegroups) and success
  type: list
  sample: ["test-ng"]
addons:
  description: List of Addons for given EKS Cluster.
  returned: when I(list_addons) and success
  type: list
  sample: ["test-addon"]
cluster:
  description: List of Fargate Profiles for given EKS Cluster.
  returned: when I(describe_cluster) and success
  type: dict
  sample: {
      "arn": "arn:aws:eks:us-east-1:xxxxxxxx:cluster/test-eks",
      "certificate_authority": {
        "data": "xxxxxxxxxxxxxxxxxxxx"
      },
      "created_at": "2020-02-22T16:23:22.190000+02:00",
      "endpoint": "https://xxxxxxxxxxxxxx.us-east-1.eks.amazonaws.com",
      "identity": {
        "oidc": {
          "issuer": "https://oidc.eks.us-east-1.amazonaws.com/id/xxxxxxxxxxxx"
        }
      },
      "kubernetes_network_config": {
        "service_ipv4_cidr": "172.20.0.0/16"
      },
      "logging": {
        "cluster_logging": []
      },
      "name": "test-eks",
      "platform_version": "eks.5",
      "resources_vpc_config": {
        "cluster_security_group_id": "sg-xxxxxxxx",
        "endpoint_private_access": true,
        "endpoint_public_access": true,
        "public_access_cidrs": [],
        "security_group_ids": [],
        "subnet_ids": [],
        "vpc_id": "vpc-xxxxx"
      },
      "role_arn": "arn:aws:iam::xxxxxxxx:role/eks-cluster-service-role",
      "status": "ACTIVE",
      "tags": {},
      "version": "1.15"
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _eks(eks, module):
    try:
        if module.params['list_fargate_profiles']:
            paginator = eks.get_paginator('list_fargate_profiles')
            iterator = paginator.paginate(
                clusterName=module.params['name']
            )
        elif module.params['list_nodegroups']:
            paginator = eks.get_paginator('list_nodegroups')
            iterator = paginator.paginate(
                clusterName=module.params['name']
            )
        elif module.params['list_addons']:
            paginator = eks.get_paginator('list_addons')
            iterator = paginator.paginate(
                clusterName=module.params['name']
            )
        elif module.params['describe_cluster']:
            return eks.describe_cluster(
                name=module.params['name']
            )
        else:
            paginator = eks.get_paginator('list_clusters')
            iterator = paginator.paginate()
        return iterator
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws eks details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['cluster_name']),
        list_fargate_profiles=dict(required=False, type=bool),
        list_nodegroups=dict(required=False, type=bool),
        list_addons=dict(required=False, type=bool),
        describe_cluster=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_fargate_profiles', True, ['name']),
            ('list_nodegroups', True, ['name']),
            ('list_addons', True, ['name']),
            ('describe_cluster', True, ['name']),
        ),
        mutually_exclusive=[
            ('list_fargate_profiles', 'list_nodegroups', 'list_addons', 'describe_cluster'),
        ],
    )

    eks = module.client('eks')

    __default_return = []

    _it = _eks(eks, module)
    if _it is not None:
        if module.params['list_fargate_profiles']:
            for response in _it:
                __default_return += response['fargateProfileNames']
                module.exit_json(fargate_profile_names=__default_return)
        elif module.params['list_nodegroups']:
            for response in _it:
                __default_return += response['nodegroups']
                module.exit_json(node_groups=__default_return)
        elif module.params['list_addons']:
            for response in _it:
                __default_return += response['addons']
                module.exit_json(addons=__default_return)
        elif module.params['describe_cluster']:
            module.exit_json(cluster=camel_dict_to_snake_dict(_it['cluster']))
        else:
            for response in _it:
                __default_return += response['clusters']
                module.exit_json(clusters=__default_return)


if __name__ == '__main__':
    main()
