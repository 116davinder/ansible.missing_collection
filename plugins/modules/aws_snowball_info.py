#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_snowball_info
short_description: Get Information about Amazon Snowball.
description:
  - Get Information about Amazon Snowball.
  - U(https://docs.aws.amazon.com/snowball/latest/apiref/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - cluster id.
    required: false
    type: str
    aliases: ['cluster_id']
  list_cluster_jobs:
    description:
      - do you want to get list of cluster_jobs for given I(id)?
    required: false
    type: bool
  list_clusters:
    description:
      - do you want to get list of clusters?
    required: false
    type: bool
  list_compatible_images:
    description:
      - do you want to get list of compatible_images?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get jobs?
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
- name: "get list of cluster_jobs"
  aws_snowball_info:
    list_cluster_jobs: true
    id: 'cluster-id'

- name: "get clusters"
  aws_snowball_info:
    list_clusters: true

- name: "get list of compatible_images"
  aws_snowball_info:
    list_compatible_images: true

- name: "get jobs"
  aws_snowball_info:
    list_jobs: true
"""

RETURN = """
cluster_jobs:
  description: list of cluster_jobs.
  returned: when `list_cluster_jobs` is defined and success.
  type: list
clusters:
  description: get of clusters.
  returned: when `list_clusters` is defined and success.
  type: list
compatible_images:
  description: list of compatible_images.
  returned: when `list_compatible_images` is defined and success.
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _snowball(client, module):
    try:
        if module.params['list_cluster_jobs']:
            if client.can_paginate('list_cluster_jobs'):
                paginator = client.get_paginator('list_cluster_jobs')
                return paginator.paginate(
                    ClusterId=module.params['id']
                ), True
            else:
                return client.list_cluster_jobs(
                    ClusterId=module.params['id']
                ), False
        elif module.params['list_clusters']:
            if client.can_paginate('list_clusters'):
                paginator = client.get_paginator('list_clusters')
                return paginator.paginate(), True
            else:
                return client.list_clusters(), False
        elif module.params['list_compatible_images']:
            if client.can_paginate('list_compatible_images'):
                paginator = client.get_paginator('list_compatible_images')
                return paginator.paginate(), True
            else:
                return client.list_compatible_images(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(), True
            else:
                return client.list_jobs(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Snowball details')


def main():
    argument_spec = dict(
        id=dict(
            required=False,
            aliases=['cluster_id']
        ),
        list_cluster_jobs=dict(required=False, type=bool),
        list_clusters=dict(required=False, type=bool),
        list_compatible_images=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_cluster_jobs', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_cluster_jobs',
                'list_clusters',
                'list_compatible_images',
                'list_jobs',
            )
        ],
    )

    client = module.client('snowball', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _snowball(client, module)

    if module.params['list_cluster_jobs']:
        module.exit_json(cluster_jobs=aws_response_list_parser(paginate, it, 'JobListEntries'))
    elif module.params['list_clusters']:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'ClusterListEntries'))
    elif module.params['list_compatible_images']:
        module.exit_json(compatible_images=aws_response_list_parser(paginate, it, 'CompatibleImages'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'JobListEntries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
