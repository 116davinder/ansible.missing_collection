#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_lookoutvision_info
short_description: Get Information about Amazon Lookout for Vision.
description:
  - Get Information about Amazon Lookout for Vision.
  - U(https://docs.aws.amazon.com/lookout-for-vision/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  name:
    description:
      - name of project.
    required: false
    type: str
    aliases: ['project_name']
  list_dataset_entries:
    description:
      - do you want to get list of dataset_entries for given project I(name) and I(dataset_type)?
    required: false
    type: bool
  list_models:
    description:
      - do you want to get list of models for given project I(name)?
    required: false
    type: bool
  list_projects:
    description:
      - do you want to get list of projects?
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
- name: "get list of dataset_entries"
  aws_lookoutvision_info:
    list_dataset_entries: true
    name: 'test-project-name'
    dataset_type: 'train'

- name: "get list of models"
  aws_lookoutvision_info:
    list_models: true
    name: 'test-project-name'

- name: "get list of projects"
  aws_lookoutvision_info:
    list_projects: true
"""

RETURN = """
dataset_entries:
  description: list of dataset_entries.
  returned: when `list_dataset_entries` is defined and success.
  type: list
models:
  description: list of models.
  returned: when `list_models` is defined and success.
  type: list
projects:
  description: list of projects.
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


def _lookoutvision(client, module):
    try:
        if module.params['list_dataset_entries']:
            if client.can_paginate('list_dataset_entries'):
                paginator = client.get_paginator('list_dataset_entries')
                return paginator.paginate(
                    ProjectName=module.params['name'],
                    DatasetType=module.params['dataset_type']
                ), True
            else:
                return client.list_dataset_entries(
                    ProjectName=module.params['name'],
                    DatasetType=module.params['dataset_type']
                ), False
        elif module.params['list_models']:
            if client.can_paginate('list_models'):
                paginator = client.get_paginator('list_models')
                return paginator.paginate(
                    ProjectName=module.params['name'],
                ), True
            else:
                return client.list_models(
                    ProjectName=module.params['name'],
                ), False
        elif module.params['list_projects']:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(), True
            else:
                return client.list_projects(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Lookout for Vision details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['project_name']),
        dataset_type=dict(required=False),
        list_dataset_entries=dict(required=False, type=bool),
        list_models=dict(required=False, type=bool),
        list_projects=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_dataset_entries', True, ['name', 'dataset_type']),
            ('list_models', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_dataset_entries',
                'list_models',
                'list_projects',
            )
        ],
    )

    client = module.client('lookoutvision', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _lookoutvision(client, module)

    if module.params['list_dataset_entries']:
        module.exit_json(dataset_entries=aws_response_list_parser(paginate, it, 'DatasetEntries'))
    elif module.params['list_models']:
        module.exit_json(models=aws_response_list_parser(paginate, it, 'Models'))
    elif module.params['list_projects']:
        module.exit_json(projects=aws_response_list_parser(paginate, it, 'Projects'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
