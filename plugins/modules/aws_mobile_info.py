#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mobile_info
short_description: Get Information about AWS Mobile.
description:
  - Get Information about AWS Mobile.
  - U(https://docs.aws.amazon.com/migrationhub/latest/ug/API_Operations.html)
version_added: 0.0.7
options:
  list_bundles:
    description:
      - do you want to get list of bundles?
    required: false
    type: bool
  list_projects:
    description:
      - do you want to get projects?
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
- name: "get list of bundles"
  aws_mobile_info:
    list_bundles: true

- name: "get projects"
  aws_mobile_info:
    list_projects: true
"""

RETURN = """
bundles:
  description: list of bundles.
  returned: when `list_bundles` is defined and success.
  type: list
projects:
  description: get of projects.
  returned: when `list_projects` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mobile(client, module):
    try:
        if module.params['list_bundles']:
            if client.can_paginate('list_bundles'):
                paginator = client.get_paginator('list_bundles')
                return paginator.paginate(), True
            else:
                return client.list_bundles(), False
        elif module.params['list_projects']:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(), True
            else:
                return client.list_projects(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Mobile details')


def main():
    argument_spec = dict(
        list_bundles=dict(required=False, type=bool),
        list_projects=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_bundles',
                'list_projects',
            )
        ],
    )

    client = module.client('mobile', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mobile(client, module)

    if module.params['list_bundles']:
        module.exit_json(bundles=aws_response_list_parser(paginate, it, 'bundleList'))
    elif module.params['list_projects']:
        module.exit_json(projects=aws_response_list_parser(paginate, it, 'projects'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
