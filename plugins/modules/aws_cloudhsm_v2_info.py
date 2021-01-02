#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudhsm_v2_info
short_description: Get details about Amazon CloudHSM V2.
description:
  - Get Information about Amazon CloudHSM V2.
  - U(https://docs.aws.amazon.com/cloudhsm/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  cluster_ids:
    description:
      - list of cloudhsm cluster ids.
    required: false
    type: list
  describe_clusters:
    description:
      - do you want to describe cloudhsm clusters given I(cluster_ids)?
    required: false
    type: bool
  describe_backups:
    description:
      - do you want to describe cloudhsm cluster backups given I(cluster_ids)?
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
- name: "describe all hsm clusters"
  aws_cloudhsm_v2_info:
    describe_clusters: true
    cluster_ids: ['test']

- name: "describe backups for all hsm clusters"
  aws_cloudhsm_v2_info:
    describe_backups: true
    cluster_ids: ['test']
"""

RETURN = """
clusters:
  description: List of CloudHSM Clusters.
  returned: when `describe_clusters` and `cluster_ids` are defined and success
  type: list
  sample: [
    {
        'backup_policy': 'DEFAULT',
        'backup_retention_policy': {},
        'cluster_id': 'string',
        'create_timestamp': datetime(2015, 1, 1),
        'hsms': [],
        'hsm_type': 'string',
        'pre_co_password': 'string',
        'security_group': 'string',
        'source_backup_id': 'string',
        'state': 'CREATE_IN_PROGRESS',
        'state_message': 'string',
        'subnet_mapping': {},
        'vpc_id': 'string',
        'certificates': {},
        'tag_list': []
    },
  ]
backups:
  description: List of Backups of Given CloudHSM Cluster Ids.
  returned: when `describe_backups` and `cluster_ids` are defined and success
  type: list
  sample: [
    {
        'backup_id': 'string',
        'backup_state': 'CREATE_IN_PROGRESS',
        'cluster_id': 'string',
        'create_timestamp': datetime(2019, 9, 9),
        'copy_timestamp': datetime(2015, 1, 1),
        'never_expires': True,
        'source_region': 'string',
        'source_backup': 'string',
        'source_cluster': 'string',
        'delete_timestamp': datetime(2018, 8, 8),
        'tag_list': []
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


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _cloudhsm(client, module):
    try:
        if module.params['describe_clusters']:
            if client.can_paginate('describe_clusters'):
                paginator = client.get_paginator('describe_clusters')
                return paginator.paginate(
                    Filters={
                        'clusterIds': module.params['cluster_ids']
                    }
                ), True
            else:
                return client.describe_clusters(
                    Filters={
                        'clusterIds': module.params['cluster_ids']
                    }
                ), False
        elif module.params['describe_backups']:
            if client.can_paginate('describe_backups'):
                paginator = client.get_paginator('describe_backups')
                return paginator.paginate(
                    Filters={
                        'clusterIds': module.params['cluster_ids']
                    },
                    SortAscending=True
                ), True
            else:
                return client.describe_backups(
                    Filters={
                        'clusterIds': module.params['cluster_ids']
                    },
                    SortAscending=True
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudhsm v2 details')


def main():
    argument_spec = dict(
        cluster_ids=dict(required=False, type=list),
        describe_clusters=dict(required=False, type=bool),
        describe_backups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_clusters', True, ['cluster_ids']),
            ('describe_backups', True, ['cluster_ids']),
        ],
        mutually_exclusive=[],
    )

    client = module.client('cloudhsmv2', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudhsm(client, module)

    if module.params['describe_clusters']:
        module.exit_json(clusters=aws_response_list_parser(paginate, _it, 'Clusters'))
    elif module.params['describe_backups']:
        module.exit_json(backups=aws_response_list_parser(paginate, _it, 'Backups'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
