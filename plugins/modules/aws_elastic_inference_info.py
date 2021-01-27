#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_elastic_inference_info
short_description: Get Information about Amazon Elastic Inference (Elastic Inference).
description:
  - Get Information about Amazon Elastic Inference (Elastic Inference).
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elastic-inference.html)
version_added: 0.0.6
options:
  ids:
    description:
      - ids of the accelerators.
    required: false
    type: list
  location_type:
    description:
      - accelerator location type.
    required: false
    type: str
    choices: ['region', 'availability-zone', 'availability-zone-id']
    default: 'region'
  describe_accelerators:
    description:
      - do you want to get details of accelerators for given I(ids)?
    required: false
    type: bool
  describe_accelerator_types:
    description:
      - do you want to get details of accelerators types?
    required: false
    type: bool
  describe_accelerator_offerings:
    description:
      - do you want to get details of accelerators offerings for given I(location_type)?
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
- name: "get details of accelerators"
  aws_elastic_inference_info:
    describe_accelerators: true
    ids: []

- name: "get details of accelerators types"
  aws_elastic_inference_info:
    describe_accelerator_types: true

- name: "get details of accelerators offerings"
  aws_elastic_inference_info:
    describe_accelerator_offerings: true
    location_type: 'region'
"""

RETURN = """
accelerators:
  description: details of accelerators.
  returned: when `describe_accelerators` and `ids` are defined and success
  type: list
accelerator_types:
  description: details of accelerators types.
  returned: when `describe_accelerator_types` is defined and success
  type: list
accelerator_offerings:
  description: details of accelerators offerings.
  returned: when `describe_accelerator_offerings` and `location_type` are defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _elastic_inference(client, module):
    try:
        if module.params['describe_accelerators']:
            if client.can_paginate('describe_accelerators'):
                paginator = client.get_paginator('describe_accelerators')
                return paginator.paginate(
                    acceleratorIds=module.params['ids'],
                ), True
            else:
                return client.describe_accelerators(
                    acceleratorIds=module.params['ids'],
                ), False
        elif module.params['describe_accelerator_types']:
            return client.describe_accelerator_types(), False
        elif module.params['describe_accelerator_offerings']:
            if client.can_paginate('describe_accelerator_offerings'):
                paginator = client.get_paginator('describe_accelerator_offerings')
                return paginator.paginate(
                    locationType=module.params['location_type'],
                ), True
            else:
                return client.describe_accelerator_offerings(
                    locationType=module.params['location_type'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elastic Inference details')


def main():
    argument_spec = dict(
        ids=dict(required=False, type=list),
        location_type=dict(
            required=False,
            choices=['region', 'availability-zone', 'availability-zone-id'],
            default='region'
        ),
        describe_accelerators=dict(required=False, type=bool),
        describe_accelerator_types=dict(required=False, type=bool),
        describe_accelerator_offerings=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_accelerators', True, ['ids']),
        ),
        mutually_exclusive=[
            (
                'describe_accelerators',
                'describe_accelerator_types',
                'describe_accelerator_offerings',
            )
        ],
    )

    client = module.client('elastic-inference', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _elastic_inference(client, module)

    if module.params['describe_accelerators']:
        module.exit_json(accelerators=aws_response_list_parser(paginate, it, 'acceleratorSet'))
    elif module.params['describe_accelerator_types']:
        module.exit_json(accelerator_types=aws_response_list_parser(paginate, it, 'acceleratorTypes'))
    elif module.params['describe_accelerator_offerings']:
        module.exit_json(accelerator_offerings=aws_response_list_parser(paginate, it, 'acceleratorTypeOfferings'))
    else:
        module.fail_json_aws("unknown options are passed")


if __name__ == '__main__':
    main()
