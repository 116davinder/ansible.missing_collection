#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediaconnect_info
short_description: Get Information about AWS Elemental MediaConnect.
description:
  - Get Information about AWS Elemental MediaConnect.
  - U(https://docs.aws.amazon.com/mediaconnect/latest/api/resources.html)
version_added: 0.0.7
options:
  list_entitlements:
    description:
      - do you want to get list of entitlements?
    required: false
    type: bool
  list_flows:
    description:
      - do you want to get list of flows?
    required: false
    type: bool
  list_offerings:
    description:
      - do you want to get list of offerings?
    required: false
    type: bool
  list_reservations:
    description:
      - do you want to get list of reservations?
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
- name: "get list of entitlements"
  aws_mediaconnect_info:
    list_entitlements: true

- name: "get list of flows"
  aws_mediaconnect_info:
    list_flows: true

- name: "get list of offerings"
  aws_mediaconnect_info:
    list_offerings: true

- name: "get list of reservations"
  aws_mediaconnect_info:
    list_reservations: true
"""

RETURN = """
entitlements:
  description: list of entitlements.
  returned: when `list_entitlements` is defined and success.
  type: list
flows:
  description: list of flows.
  returned: when `list_flows` is defined and success.
  type: list
offerings:
  description: list of offerings.
  returned: when `list_offerings` is defined and success.
  type: list
reservations:
  description: list of reservations.
  returned: when `list_reservations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mediaconnect(client, module):
    try:
        if module.params['list_entitlements']:
            if client.can_paginate('list_entitlements'):
                paginator = client.get_paginator('list_entitlements')
                return paginator.paginate(), True
            else:
                return client.list_entitlements(), False
        elif module.params['list_flows']:
            if client.can_paginate('list_flows'):
                paginator = client.get_paginator('list_flows')
                return paginator.paginate(), True
            else:
                return client.list_flows(), False
        elif module.params['list_offerings']:
            if client.can_paginate('list_offerings'):
                paginator = client.get_paginator('list_offerings')
                return paginator.paginate(), True
            else:
                return client.list_offerings(), False
        elif module.params['list_reservations']:
            if client.can_paginate('list_reservations'):
                paginator = client.get_paginator('list_reservations')
                return paginator.paginate(), True
            else:
                return client.list_reservations(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Media Connect details')


def main():
    argument_spec = dict(
        list_entitlements=dict(required=False, type=bool),
        list_flows=dict(required=False, type=bool),
        list_offerings=dict(required=False, type=bool),
        list_reservations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_entitlements',
                'list_flows',
                'list_offerings',
                'list_reservations',
            )
        ],
    )

    client = module.client('mediaconnect', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediaconnect(client, module)

    if module.params['list_entitlements']:
        module.exit_json(entitlements=aws_response_list_parser(paginate, it, 'Entitlements'))
    elif module.params['list_flows']:
        module.exit_json(flows=aws_response_list_parser(paginate, it, 'Flows'))
    elif module.params['list_offerings']:
        module.exit_json(offerings=aws_response_list_parser(paginate, it, 'Offerings'))
    elif module.params['list_reservations']:
        module.exit_json(reservations=aws_response_list_parser(paginate, it, 'Reservations'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
