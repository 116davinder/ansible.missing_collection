#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_transcribe_info
short_description: Get Information about Amazon Transcribe Service.
description:
  - Get Information about Amazon Transcribe Service.
  - U(https://docs.aws.amazon.com/transcribe/latest/dg/API_Operations_Amazon_Transcribe_Service.html)
version_added: 0.1.0
options:
  name_contains:
    description:
      - name contains to filter results.
    required: false
    type: str
  status:
    description:
      - filter results.
    required: false
    type: str
    choices: ['IN_PROGRESS', 'FAILED', 'COMPLETED', 'QUEUED']
    default: 'COMPLETED'
  list_language_models:
    description:
      - do you want to get list of language_models for given I(name_contains) and I(status)?
    required: false
    type: bool
  list_medical_transcription_jobs:
    description:
      - do you want to get medical_transcription_jobs for given I(name_contains) and I(status)?
    required: false
    type: bool
  list_transcription_jobs:
    description:
      - do you want to get list of transcription_jobs for given I(name_contains) and I(status)?
    type: bool
  list_vocabulary_filters:
    description:
      - do you want to get vocabulary_filters?
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
- name: "get list of language_models"
  aws_transcribe_info:
    list_language_models: true
    status: 'COMPLETED'
    name_contains: 'test-model'

- name: "get medical_transcription_jobs"
  aws_transcribe_info:
    list_medical_transcription_jobs: true
    status: 'COMPLETED'
    name_contains: 'test-jobs'

- name: "get list of transcription_jobs"
  aws_transcribe_info:
    list_transcription_jobs: true
    status: 'COMPLETED'
    name_contains: 'test-jobs'

- name: "get vocabulary_filters details"
  aws_transcribe_info:
    list_vocabulary_filters: true
"""

RETURN = """
language_models:
  description: list of language_models.
  returned: when `list_language_models` is defined and success.
  type: list
medical_transcription_jobs:
  description: list of medical_transcription_jobs.
  returned: when `list_medical_transcription_jobs` is defined and success.
  type: list
transcription_jobs:
  description: list of transcription_jobs.
  returned: when `list_transcription_jobs` is defined and success.
  type: list
vocabulary_filters:
  description: get details of vocabulary_filters.
  returned: when `list_vocabulary_filters` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _transcribe(client, module):
    try:
        if module.params['list_language_models']:
            if client.can_paginate('list_language_models'):
                paginator = client.get_paginator('list_language_models')
                return paginator.paginate(
                    StatusEquals=module.params['status'],
                    NameContains=module.params['name_contains'],
                ), True
            else:
                return client.list_language_models(
                    StatusEquals=module.params['status'],
                    NameContains=module.params['name_contains'],
                ), False
        elif module.params['list_medical_transcription_jobs']:
            if client.can_paginate('list_medical_transcription_jobs'):
                paginator = client.get_paginator('list_medical_transcription_jobs')
                return paginator.paginate(
                    Status=module.params['status'],
                    JobNameContains=module.params['name_contains'],
                ), True
            else:
                return client.list_medical_transcription_jobs(
                    Status=module.params['status'],
                    JobNameContains=module.params['name_contains'],
                ), False
        elif module.params['list_transcription_jobs']:
            if client.can_paginate('list_transcription_jobs'):
                paginator = client.get_paginator('list_transcription_jobs')
                return paginator.paginate(
                    Status=module.params['status'],
                    JobNameContains=module.params['name_contains'],
                ), True
            else:
                return client.list_transcription_jobs(
                    Status=module.params['status'],
                    JobNameContains=module.params['name_contains'],
                ), False
        elif module.params['list_vocabulary_filters']:
            if client.can_paginate('list_vocabulary_filters'):
                paginator = client.get_paginator('list_vocabulary_filters')
                return paginator.paginate(), True
            else:
                return client.list_vocabulary_filters(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Transcribe Service details')


def main():
    argument_spec = dict(
        name_contains=dict(required=False),
        status=dict(
            required=False,
            choices=['IN_PROGRESS', 'FAILED', 'COMPLETED', 'QUEUED'],
            default='COMPLETED'
        ),
        list_language_models=dict(required=False, type=bool),
        list_medical_transcription_jobs=dict(required=False, type=bool),
        list_transcription_jobs=dict(required=False, type=bool),
        list_vocabulary_filters=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_language_models', True, ['name_contains']),
            ('list_medical_transcription_jobs', True, ['name_contains']),
            ('list_transcription_jobs', True, ['name_contains']),
            ('list_vocabulary_filters', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_language_models',
                'list_medical_transcription_jobs',
                'list_transcription_jobs',
                'list_vocabulary_filters',
            )
        ],
    )

    client = module.client('transcribe', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _transcribe(client, module)

    if module.params['list_language_models']:
        module.exit_json(language_models=aws_response_list_parser(paginate, it, 'Models'))
    elif module.params['list_medical_transcription_jobs']:
        module.exit_json(medical_transcription_jobs=aws_response_list_parser(paginate, it, 'MedicalTranscriptionJobSummaries'))
    elif module.params['list_transcription_jobs']:
        module.exit_json(transcription_jobs=aws_response_list_parser(paginate, it, 'TranscriptionJobSummaries'))
    elif module.params['list_vocabulary_filters']:
        module.exit_json(vocabulary_filters=aws_response_list_parser(paginate, it, 'VocabularyFilters'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
