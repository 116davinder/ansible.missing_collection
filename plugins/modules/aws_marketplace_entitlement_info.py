#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_marketplace_entitlement_info
short_description: Get Information about AWS Marketplace Entitlement Service.
description:
  - Get Information about AWS Marketplace Entitlement Service.
  - U(https://docs.aws.amazon.com/marketplaceentitlement/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  product_code:
    description:
      - code of product.
    required: false
    type: str
  get_entitlements:
    description:
      - do you want to get list of change_sets for given I(product_code)?
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
  aws_marketplace_entitlement_info:
    get_entitlements: true
    product_code: 'test-product-code'
"""

RETURN = """
entitlements:
  description: list of entitlements.
  returned: when `get_entitlements` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _marketplace_entitlement(client, module):
    try:
        if module.params['get_entitlements']:
            if client.can_paginate('get_entitlements'):
                paginator = client.get_paginator('get_entitlements')
                return paginator.paginate(
                    ProductCode=module.params['product_code']
                ), True
            else:
                return client.get_entitlements(
                    ProductCode=module.params['product_code']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Marketplace Entitlement Service details')


def main():
    argument_spec = dict(
        product_code=dict(required=False),
        get_entitlements=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_entitlements', True, ['product_code']),
        ),
        mutually_exclusive=[
            (
                'get_entitlements',
            )
        ],
    )

    client = module.client('marketplace-catalog', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _marketplace_entitlement(client, module)

    if module.params['get_entitlements']:
        module.exit_json(entitlements=aws_response_list_parser(paginate, it, 'Entitlements'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
