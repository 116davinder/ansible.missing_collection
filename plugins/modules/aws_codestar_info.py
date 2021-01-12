#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_info
short_description: Get Information about AWS CodePipeline.
description:
  - Get Information about AWS CodePipeline.
  - U(https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  name:
    description:
      - name of the code pipeline.
    required: false
    type: str
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


def _codestar(client, module):
    try:
        if module.params['list_resources']:
            if client.can_paginate('list_resources'):
                paginator = client.get_paginator('list_resources')
                return paginator.paginate(
                    projectId=module.params['id']
                ), True
            else:
                return client.list_resources(
                    projectId=module.params['id']
                ), False
        elif module.params['list_team_members']:
            if client.can_paginate('list_team_members'):
                paginator = client.get_paginator('list_team_members')
                return paginator.paginate(
                    projectId=module.params['id']
                ), True
            else:
                return client.list_team_members(
                    projectId=module.params['id']
                ), False
        elif module.params['list_user_profiles']:
            if client.can_paginate('list_user_profiles'):
                paginator = client.get_paginator('list_user_profiles')
                return paginator.paginate(), True
            else:
                return client.list_user_profiles(), False
        elif module.params['describe_project']:
            return client.describe_project(
                id=module.params['id']
            ), False
        else:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(), True
            else:
                return client.list_projects(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codestar details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        list_resources=dict(required=False, type=bool),
        list_team_members=dict(required=False, type=bool),
        describe_project=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_resources', True, ['id']),
            ('list_team_members', True, ['id']),
            ('describe_project', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_resources',
                'list_team_members',
                'describe_project',
            )
        ],
    )

    client = module.client('codestar', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codestar(client, module)

    if module.params['list_resources']:
        module.exit_json(resources=aws_response_list_parser(paginate, _it, 'resources'))
    elif module.params['list_team_members']:
        module.exit_json(team_members=aws_response_list_parser(paginate, _it, 'teamMembers'))
    elif module.params['describe_project']:
        module.exit_json(project=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(projects=aws_response_list_parser(paginate, _it, 'projects'))


if __name__ == '__main__':
    main()
