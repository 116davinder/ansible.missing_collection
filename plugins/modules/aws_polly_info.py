#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_polly_info
short_description: Get Information about Amazon Polly.
description:
  - Get Information about Amazon Polly.
  - U(https://docs.aws.amazon.com/polly/latest/dg/API_Operations.html)
version_added: 0.0.8
options:
  status:
    description:
      - status of speech synthesis tasks.
    required: false
    type: str
    choices: ['scheduled', 'inProgress', 'completed', 'failed']
    default: 'inProgress'
  list_lexicons:
    description:
      - do you want to get list of lexicons?
    required: false
    type: bool
  list_speech_synthesis_tasks:
    description:
      - do you want to get speech_synthesis_tasks for given I(status)?
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
- name: "get list of lexicons"
  aws_polly_info:
    list_lexicons: true

- name: "get speech_synthesis_tasks"
  aws_polly_info:
    list_speech_synthesis_tasks: true
    status: 'inProgress'
"""

RETURN = """
lexicons:
  description: list of lexicons.
  returned: when `list_lexicons` is defined and success.
  type: list
speech_synthesis_tasks:
  description: get of speech_synthesis_tasks.
  returned: when `list_speech_synthesis_tasks` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _polly(client, module):
    try:
        if module.params['list_lexicons']:
            if client.can_paginate('list_lexicons'):
                paginator = client.get_paginator('list_lexicons')
                return paginator.paginate(), True
            else:
                return client.list_lexicons(), False
        elif module.params['list_speech_synthesis_tasks']:
            if client.can_paginate('list_speech_synthesis_tasks'):
                paginator = client.get_paginator('list_speech_synthesis_tasks')
                return paginator.paginate(
                    Status=module.params['status']
                ), True
            else:
                return client.list_speech_synthesis_tasks(
                    Status=module.params['status']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Polly details')


def main():
    argument_spec = dict(
        status=dict(
            required=False,
            choices=['scheduled', 'inProgress', 'completed', 'failed'],
            default='inProgress'
        ),
        list_lexicons=dict(required=False, type=bool),
        list_speech_synthesis_tasks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_lexicons',
                'list_speech_synthesis_tasks',
            )
        ],
    )

    client = module.client('polly', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _polly(client, module)

    if module.params['list_lexicons']:
        module.exit_json(lexicons=aws_response_list_parser(paginate, it, 'Lexicons'))
    elif module.params['list_speech_synthesis_tasks']:
        module.exit_json(speech_synthesis_tasks=aws_response_list_parser(paginate, it, 'SynthesisTasks'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
