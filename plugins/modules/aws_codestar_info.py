#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_info
short_description: Get Information about AWS CodeStar.
description:
  - Get Information about AWS CodeStar.
  - U(https://docs.aws.amazon.com/codestar/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  id:
    description:
      - id of codestar project.
    required: false
    type: str
  list_resources:
    description:
      - do you want to get list of resources for given I(id)?
    required: false
    type: bool
  list_team_members:
    description:
      - do you want to get list of team members for given I(id)?
    required: false
    type: bool
  describe_project:
    description:
      - do you want to get details for given I(id)?
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
- name: "get list of codestar projects"
  aws_codestar_info:

- name: "get list of codestar project resources"
  aws_codestar_info:
    list_resources: true
    id: 'test-codestar-project'

- name: "get list of codestar project team members"
  aws_codestar_info:
    list_team_members: true
    id: 'test-codestar-project'

- name: "get details about codestar project"
  aws_codestar_info:
    describe_project: true
    id: 'test-codestar-project'
"""

RETURN = """
projects:
  description: get list of code pipelines.
  returned: when no argument and success
  type: list
  sample: [
    {
        'project_id': 'string',
        'project_arn': 'string'
    },
  ]
resources:
  description: get list of resources for project.
  returned: when `list_resources` and `id` are defined and success
  type: list
  sample: [
    {
        'id': 'string'
    },
  ]
team_members:
  description: get list of team members for project.
  returned: when `list_team_members` and `id` are defined and success
  type: list
  sample: [
    {
        'user_arn': 'string',
        'project_role': 'string',
        'remote_access_allowed': True
    },
  ]
project:
  description: get details about project.
  returned: when `describe_project` and `id` are defined and success
  type: dict
  sample: {
    'name': 'string',
    'id': 'string',
    'arn': 'string',
    'description': 'string',
    'client_request_token': 'string',
    'created_time_stamp': datetime(2015, 1, 1),
    'stack_dd': 'string',
    'project_template_id': 'string',
    'status': {
        'state': 'string',
        'reason': 'string'
    }
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


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
