#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_translate_info
short_description: Get Information about Amazon Translate.
description:
  - Get Information about Amazon Translate.
  - U(https://docs.aws.amazon.com/translate/latest/dg/API_Operations.html)
version_added: 0.1.0
options:
  list_parallel_data:
    description:
      - do you want to get list of parallel_data?
    required: false
    type: bool
  list_terminologies:
    description:
      - do you want to get terminologies?
    required: false
    type: bool
  list_text_translation_jobs:
    description:
      - do you want to get list of text_translation_jobs?
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
- name: "get list of parallel_data"
  aws_translate_info:
    list_parallel_data: true

- name: "get terminologies"
  aws_translate_info:
    list_terminologies: true

- name: "get list of text_translation_jobs"
  aws_translate_info:
    list_text_translation_jobs: true
"""

RETURN = """
parallel_data:
  description: list of parallel_data.
  returned: when `list_parallel_data` is defined and success.
  type: list
terminologies:
  description: list of terminologies.
  returned: when `list_terminologies` is defined and success.
  type: list
text_translation_jobs:
  description: list of text_translation_jobs.
  returned: when `list_text_translation_jobs` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _translate(client, module):
    try:
        if module.params['list_parallel_data']:
            if client.can_paginate('list_parallel_data'):
                paginator = client.get_paginator('list_parallel_data')
                return paginator.paginate(), True
            else:
                return client.list_parallel_data(), False
        elif module.params['list_terminologies']:
            if client.can_paginate('list_terminologies'):
                paginator = client.get_paginator('list_terminologies')
                return paginator.paginate(), True
            else:
                return client.list_terminologies(), False
        elif module.params['list_text_translation_jobs']:
            if client.can_paginate('list_text_translation_jobs'):
                paginator = client.get_paginator('list_text_translation_jobs')
                return paginator.paginate(), True
            else:
                return client.list_text_translation_jobs(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Translate details')


def main():
    argument_spec = dict(
        list_parallel_data=dict(required=False, type=bool),
        list_terminologies=dict(required=False, type=bool),
        list_text_translation_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_parallel_data',
                'list_terminologies',
                'list_text_translation_jobs',
            )
        ],
    )

    client = module.client('translate', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _translate(client, module)

    if module.params['list_parallel_data']:
        module.exit_json(parallel_data=aws_response_list_parser(paginate, it, 'ParallelDataPropertiesList'))
    elif module.params['list_terminologies']:
        module.exit_json(terminologies=aws_response_list_parser(paginate, it, 'TerminologyPropertiesList'))
    elif module.params['list_text_translation_jobs']:
        module.exit_json(text_translation_jobs=aws_response_list_parser(paginate, it, 'TextTranslationJobPropertiesList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
