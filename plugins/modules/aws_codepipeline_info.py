#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codepipeline_info
short_description: Get Information about AWS CodePipeline.
description:
  - Get Information about AWS CodePipeline.
  - U(https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  name:
    description:
      - name of the code pipeline.
    required: false
    type: str
  action_owner_filter:
    description:
      - type of action owner filter.
    required: false
    type: str
    choices: ['AWS', 'ThirdParty', 'Custom']
    default: 'AWS'
  get_pipeline:
    description:
      - do you want to get details about given I(name)?
    required: false
    type: bool
  list_webhooks:
    description:
      - do you want to get list of webhooks for given I(name)?
    required: false
    type: bool
  list_pipeline_executions:
    description:
      - do you want to get list of pipeline executions for given I(name)?
    required: false
    type: bool
  list_action_types:
    description:
      - do you want to get list of action types for given I(action_owner_filter)?
    required: false
    type: bool
  list_action_executions:
    description:
      - do you want to get list of execution actions details about given I(name)?
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
- name: "get list of codepipelines"
  aws_codepipeline_info:

- name: "get details about codepipeline"
  aws_codepipeline_info:
    get_pipeline: true
    name: 'test'

- name: "get list of webhooks"
  aws_codepipeline_info:
    list_webhooks: true

- name: "get list of codepipeline executions"
  aws_codepipeline_info:
    list_pipeline_executions: true
    name: 'test'

- name: "get list of action types"
  aws_codepipeline_info:
    list_action_types: true
    action_owner_filter: 'AWS'

- name: "get list of the action executions for given pipeline"
  aws_codepipeline_info:
    list_action_executions: true
    name: 'test'
"""

RETURN = """
pipelines:
  description: get list of code pipelines.
  returned: when no argument and success
  type: list
  sample: [
    {
        'name': 'string',
        'version': 123,
        'created': datetime(2015, 1, 1),
        'updated': datetime(2016, 6, 6)
    },
  ]
pipeline:
  description: get detail about given pipeline name.
  returned: when `get_pipeline` is defined and success
  type: dict
  sample: {
    'name': 'string',
    'role_arn': 'string',
    'artifact_store': {},
    'artifact_stores': {},
    'stages': [],
    'version': 123
  }
webhooks:
  description: get list of code pipeline webhooks.
  returned: when `name` and `list_webhooks` are defined and success
  type: list
  sample: [
    {
        'definition': {
            'name': 'string',
            'target_pipeline': 'string',
            'target_action': 'string',
            'filters': [
                {
                    'json_path': 'string',
                    'match_equals': 'string'
                },
            ],
            'authentication': 'GITHUB_HMAC',
            'authentication_configuration': {}
        },
        'url': 'string',
        'error_message': 'string',
        'error_code': 'string',
        'last_triggered': datetime(2015, 1, 1),
        'arn': 'string',
        'tags': []
    },
  ]
executions:
  description: get list of code pipeline executions.
  returned: when `name` and `list_pipeline_executions` are defined and success
  type: list
  sample: [
    {
        'pipeline_execution_id': 'string',
        'status': 'Cancelled',
        'start_time': datetime(2016, 6, 6),
        'last_update_time': datetime(2015, 1, 1),
        'source_revisions': [],
        'trigger': {},
        'stop_trigger': {}
    },
  ]
action_types:
  description: get list of code pipeline action types.
  returned: when `action_owner_filter` and `list_action_types` defined and success
  type: list
  sample: [
    {
        'id': {
            'category': 'Source',
            'owner': 'AWS',
            'provider': 'string',
            'version': 'string'
        },
        'settings': {},
        'action_configuration_properties': [],
        'input_artifact_details': {},
        'output_artifact_details': {}
    },
  ]
action_execution_details:
  description: get list of code pipeline action execution details.
  returned: when `name` and `list_action_executions` are defined and success
  type: list
  sample: [
    {
        'pipeline_execution_id': 'string',
        'action_execution_id': 'string',
        'pipeline_version': 123,
        'stage_name': 'string',
        'action_name': 'string',
        'start_time': datetime(2015, 1, 1),
        'last_update_time': datetime(2016, 6, 6),
        'status': 'InProgress',
        'input': {
            'action_type_id': {
                'category': 'Source',
                'owner': 'AWS',
                'provider': 'string',
                'version': 'string'
            },
            'configuration': {
                'string': 'string'
            },
            'resolved_configuration': {
                'string': 'string'
            },
            'role_arn': 'string',
            'region': 'string',
            'input_artifacts': [],
            'namespace': 'string'
        },
        'output': {
            'output_artifacts': [],
            'execution_result': {},
            'output_variables': {
                'string': 'string'
            }
        }
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _codepipeline(client, module):
    try:
        if module.params['get_pipeline']:
            return client.get_pipeline(
                name=module.params['name']
            ), False
        elif module.params['list_webhooks']:
            if client.can_paginate('list_webhooks'):
                paginator = client.get_paginator('list_webhooks')
                return paginator.paginate(), True
            else:
                return client.list_webhooks(), False
        elif module.params['list_pipeline_executions']:
            if client.can_paginate('list_pipeline_executions'):
                paginator = client.get_paginator('list_pipeline_executions')
                return paginator.paginate(
                    pipelineName=module.params['name']
                ), True
            else:
                return client.list_pipeline_executions(
                    pipelineName=module.params['name']
                ), False
        elif module.params['list_action_types']:
            if client.can_paginate('list_action_types'):
                paginator = client.get_paginator('list_action_types')
                return paginator.paginate(
                    actionOwnerFilter=module.params['action_owner_filter']
                ), True
            else:
                return client.list_action_types(
                    actionOwnerFilter=module.params['action_owner_filter']
                ), False
        elif module.params['list_action_executions']:
            if client.can_paginate('list_action_executions'):
                paginator = client.get_paginator('list_action_executions')
                return paginator.paginate(
                    pipelineName=module.params['name']
                ), True
            else:
                return client.list_action_executions(
                    pipelineName=module.params['name']
                ), False
        else:
            if client.can_paginate('list_pipelines'):
                paginator = client.get_paginator('list_pipelines')
                return paginator.paginate(), True
            else:
                return client.list_pipelines(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codepipeline details')


def main():
    argument_spec = dict(
        name=dict(required=False),
        action_owner_filter=dict(required=False, choices=['AWS', 'ThirdParty', 'Custom'], default='AWS'),
        get_pipeline=dict(required=False, type=bool),
        list_webhooks=dict(required=False, type=bool),
        list_pipeline_executions=dict(required=False, type=bool),
        list_action_types=dict(required=False, type=bool),
        list_action_executions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_pipeline', True, ['name']),
            ('list_pipeline_executions', True, ['name']),
            ('list_action_executions', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'get_pipeline',
                'list_webhooks',
                'list_pipeline_executions',
                'list_action_types',
                'list_action_executions',
            )
        ],
    )

    client = module.client('codepipeline', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codepipeline(client, module)

    if module.params['get_pipeline']:
        module.exit_json(pipeline=camel_dict_to_snake_dict(_it['pipeline']))
    elif module.params['list_webhooks']:
        module.exit_json(webhooks=aws_response_list_parser(paginate, _it, 'webhooks'))
    elif module.params['list_pipeline_executions']:
        module.exit_json(executions=aws_response_list_parser(paginate, _it, 'pipelineExecutionSummaries'))
    elif module.params['list_action_types']:
        module.exit_json(action_types=aws_response_list_parser(paginate, _it, 'actionTypes'))
    elif module.params['list_action_executions']:
        module.exit_json(action_execution_details=aws_response_list_parser(paginate, _it, 'actionExecutionDetails'))
    else:
        module.exit_json(pipelines=aws_response_list_parser(paginate, _it, 'pipelines'))


if __name__ == '__main__':
    main()
