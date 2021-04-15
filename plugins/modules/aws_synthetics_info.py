#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_synthetics_info
short_description: Get Information about Amazon Cloudwatch Synthetics.
description:
  - Get Information about Amazon Cloudwatch Synthetics.
  - U(https://docs.aws.amazon.com/AmazonSynthetics/latest/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  describe_canaries:
    description:
      - do you want to get list of canaries?
    required: false
    type: bool
  describe_canaries_last_run:
    description:
      - do you want to get canaries_last_run?
    required: false
    type: bool
  describe_runtime_versions:
    description:
      - do you want to get list of runtime_versions?
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
- name: "get list of canaries"
  aws_synthetics_info:
    describe_canaries: true

- name: "get canaries_last_run"
  aws_synthetics_info:
    describe_canaries_last_run: true

- name: "get list of runtime_versions"
  aws_synthetics_info:
    describe_runtime_versions: true
"""

RETURN = """
canaries:
  description: list of canaries.
  returned: when `describe_canaries` is defined and success.
  type: list
canaries_last_run:
  description: list of canaries_last_run.
  returned: when `describe_canaries_last_run` is defined and success.
  type: list
runtime_versions:
  description: list of runtime_versions.
  returned: when `describe_runtime_versions` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _synthetics(client, module):
    try:
        if module.params['describe_canaries']:
            if client.can_paginate('describe_canaries'):
                paginator = client.get_paginator('describe_canaries')
                return paginator.paginate(), True
            else:
                return client.describe_canaries(), False
        elif module.params['describe_canaries_last_run']:
            if client.can_paginate('describe_canaries_last_run'):
                paginator = client.get_paginator('describe_canaries_last_run')
                return paginator.paginate(), True
            else:
                return client.describe_canaries_last_run(), False
        elif module.params['describe_runtime_versions']:
            if client.can_paginate('describe_runtime_versions'):
                paginator = client.get_paginator('describe_runtime_versions')
                return paginator.paginate(), True
            else:
                return client.describe_runtime_versions(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Cloudwatch Synthetics details')


def main():
    argument_spec = dict(
        describe_canaries=dict(required=False, type=bool),
        describe_canaries_last_run=dict(required=False, type=bool),
        describe_runtime_versions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'describe_canaries',
                'describe_canaries_last_run',
                'describe_runtime_versions',
            )
        ],
    )

    client = module.client('synthetics', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _synthetics(client, module)

    if module.params['describe_canaries']:
        module.exit_json(canaries=aws_response_list_parser(paginate, it, 'Canaries'))
    elif module.params['describe_canaries_last_run']:
        module.exit_json(canaries_last_run=aws_response_list_parser(paginate, it, 'CanariesLastRun'))
    elif module.params['describe_runtime_versions']:
        module.exit_json(runtime_versions=aws_response_list_parser(paginate, it, 'RuntimeVersions'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
