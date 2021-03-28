#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_outposts_info
short_description: Get Information about Amazon outposts.
description:
  - Get Information about Amazon outposts.
  - U(https://docs.aws.amazon.com/outposts/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  list_outposts:
    description:
      - do you want to get list of outposts?
    required: false
    type: bool
  list_sites:
    description:
      - do you want to get sites?
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
- name: "get list of outposts"
  aws_outposts_info:
    list_outposts: true

- name: "get sites"
  aws_outposts_info:
    list_sites: true
"""

RETURN = """
outposts:
  description: list of outposts.
  returned: when `list_outposts` is defined and success.
  type: list
sites:
  description: get of sites.
  returned: when `list_sites` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _outposts(client, module):
    try:
        if module.params['list_outposts']:
            if client.can_paginate('list_outposts'):
                paginator = client.get_paginator('list_outposts')
                return paginator.paginate(), True
            else:
                return client.list_outposts(), False
        elif module.params['list_sites']:
            if client.can_paginate('list_sites'):
                paginator = client.get_paginator('list_sites')
                return paginator.paginate(), True
            else:
                return client.list_sites(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon outposts details')


def main():
    argument_spec = dict(
        list_outposts=dict(required=False, type=bool),
        list_sites=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_outposts',
                'list_sites',
            )
        ],
    )

    client = module.client('outposts', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _outposts(client, module)

    if module.params['list_outposts']:
        module.exit_json(outposts=aws_response_list_parser(paginate, it, 'Outposts'))
    elif module.params['list_sites']:
        module.exit_json(sites=aws_response_list_parser(paginate, it, 'Sites'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
