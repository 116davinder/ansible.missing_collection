#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_resource_groups_info
short_description: Get Information about AWS Resource Groups.
description:
  - Get Information about AWS Resource Groups.
  - U(https://docs.aws.amazon.com/ARG/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  name:
    description:
      - group name.
    required: false
    type: str
    aliases: ['group_name']
  list_groups:
    description:
      - do you want to get list of groups?
    required: false
    type: bool
  list_group_resources:
    description:
      - do you want to get group_resources for given group I(name)?
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
- name: "get list of groups"
  aws_resource_groups_info:
    list_groups: true

- name: "get list of group_resources"
  aws_resource_groups_info:
    list_group_resources: true
    name: 'group_name'
"""

RETURN = """
groups:
  description: list of groups.
  returned: when `list_groups` is defined and success.
  type: list
group_resources:
  description: get of group_resources.
  returned: when `list_group_resources` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _resource_groups(client, module):
    try:
        if module.params['list_groups']:
            if client.can_paginate('list_groups'):
                paginator = client.get_paginator('list_groups')
                return paginator.paginate(), True
            else:
                return client.list_groups(), False
        elif module.params['list_group_resources']:
            if client.can_paginate('list_group_resources'):
                paginator = client.get_paginator('list_group_resources')
                return paginator.paginate(
                    Group=module.params['name'],
                ), True
            else:
                return client.list_group_resources(
                    Group=module.params['name'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Resource Groups details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['group_name']),
        list_groups=dict(required=False, type=bool),
        list_group_resources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_group_resources', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_groups',
                'list_group_resources',
            )
        ],
    )

    client = module.client('resource-groups', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _resource_groups(client, module)

    if module.params['list_groups']:
        module.exit_json(groups=aws_response_list_parser(paginate, it, 'GroupIdentifiers'))
    elif module.params['list_group_resources']:
        module.exit_json(group_resources=aws_response_list_parser(paginate, it, 'Resources'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
