#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codecommit_info
short_description: Get Information about AWS Code Commit.
description:
  - Get Information about AWS Code Commit.
  - U(https://docs.aws.amazon.com/codecommit/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  name:
    description:
      - name of the code commit repository.
    required: false
    type: str
    aliases: ['repository_name']
  status:
    description:
      - status of the pull request.
    required: false
    type: str
    choices: ['OPEN', 'CLOSED']
    default: 'OPEN'
  sort_by:
    description:
      - sort repository list.
    required: false
    type: str
    choices: ['repositoryName', 'lastModifiedDate']
    default: 'repositoryName'
  sort_order:
    description:
      - sort order repository list.
    required: false
    type: str
    choices: ['ascending', 'descending']
    default: 'ascending'
  list_repositories:
    description:
      - do you want to fetch list of repositories for given I(sort_by) and I(sort_oder)?
    required: false
    type: bool
  list_branches:
    description:
      - do you want to fetch list of branches for given I(name)?
    required: false
    type: bool
  list_pull_requests:
    description:
      - do you want to fetch list pull request ids for given I(name) and I(status)?
    required: false
    type: bool
  describe_repository:
    description:
      - do you want to describe given repository I(name)?
    required: false
    type: bool
  describe_repository_triggers:
    description:
      - do you want to describe triggers for given repository I(name)?
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
- name: "get list of all repositories"
  aws_codecommit_info:
    list_repositories: true
    sort_by: 'repositoryName'
    sort_order: 'ascending'

- name: "get list of all branches of given repository"
  aws_codecommit_info:
    list_branches: true
    name: 'test'

- name: "get list of pull request of given repository"
  aws_codecommit_info:
    list_pull_requests: true
    name: 'test'

- name: "get details of given repository"
  aws_codecommit_info:
    describe_repository: true
    name: 'test'

- name: "get details about triggers of given repository"
  aws_codecommit_info:
    describe_repository_triggers: true
    name: 'test'
"""

RETURN = """
repositories:
  description: list of repositories.
  returned: when `list_repositories`, `sort_by` and `sort_order` are defined and success
  type: list
  sample: [
    {
        "repository_id": "0185f2c7-xxxxxxxxx-b73de15c4600",
        "repository_name": "test"
    },
  ]
branches:
  description: list of branches for given repositories.
  returned: when `list_branches`, and `name` are defined and success
  type: list
  sample: ["master", "devel"]
pull_request_ids:
  description: list of pull request ids for given repositories.
  returned: when `list_pull_requests`, `status`, and `name` are defined and success
  type: list
  sample: ['string',]
repository_metadata:
  description: details about given repository.
  returned: when `describe_repository`, and `name` are defined and success
  type: dict
  sample: {
    "account_id": "xxxxxxxxxxx",
    "arn": "arn:aws:codecommit:us-east-1:xxxxxxxxxxx:test",
    "clone_url_http": "https://git-codecommit.us-east-1.amazonaws.com/v1/repos/test",
    "clone_url_ssh": "ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/test",
    "creation_date": "2021-01-08T15:28:03.798000+02:00",
    "default_branch": "master",
    "last_modified_date": "2021-01-08T15:28:41.349000+02:00",
    "repository_description": "hola",
    "repository_id": "0185f2c7-xxxxxxxxx-b73de15c4600",
    "repository_name": "test"
  }
triggers:
  description: list of triggers attached to given repository.
  returned: when `describe_repository_triggers`, and `name` are defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'destination_arn': 'string',
        'custom_data': 'string',
        'branches': [
            'string',
        ],
        'events': [
            'all',
        ]
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
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
    else:
        for _app in iterator[resource_field]:
            try:
                _return.append(camel_dict_to_snake_dict(_app))
            except AttributeError:
                _return.append(_app)
    return _return


def _codecommit(client, module):
    try:
        if module.params['list_repositories']:
            if client.can_paginate('list_repositories'):
                paginator = client.get_paginator('list_repositories')
                return paginator.paginate(
                    sortBy=module.params['sort_by'],
                    order=module.params['sort_order']
                ), True
            else:
                return client.list_repositories(
                    sortBy=module.params['sort_by'],
                    order=module.params['sort_order']
                ), False
        elif module.params['list_branches']:
            if client.can_paginate('list_branches'):
                paginator = client.get_paginator('list_branches')
                return paginator.paginate(
                    repositoryName=module.params['name'],
                ), True
            else:
                return client.list_branches(
                    repositoryName=module.params['name'],
                ), False
        elif module.params['list_pull_requests']:
            if client.can_paginate('list_pull_requests'):
                paginator = client.get_paginator('list_pull_requests')
                return paginator.paginate(
                    repositoryName=module.params['name'],
                    pullRequestStatus=module.params['status']
                ), True
            else:
                return client.list_pull_requests(
                    repositoryName=module.params['name'],
                    pullRequestStatus=module.params['status']
                ), False
        elif module.params['describe_repository']:
            if client.can_paginate('get_repository'):
                paginator = client.get_paginator('get_repository')
                return paginator.paginate(
                    repositoryName=module.params['name'],
                ), True
            else:
                return client.get_repository(
                    repositoryName=module.params['name'],
                ), False
        elif module.params['describe_repository_triggers']:
            if client.can_paginate('get_repository_triggers'):
                paginator = client.get_paginator('get_repository_triggers')
                return paginator.paginate(
                    repositoryName=module.params['name'],
                ), True
            else:
                return client.get_repository_triggers(
                    repositoryName=module.params['name'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws code commit details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['repository_name']),
        status=dict(required=False, choices=['OPEN', 'CLOSED'], default='OPEN'),
        sort_by=dict(required=False, choices=['repositoryName', 'lastModifiedDate'], default='repositoryName'),
        sort_order=dict(required=False, choices=['ascending', 'descending'], default='ascending'),
        list_repositories=dict(required=False, type=bool),
        list_branches=dict(required=False, type=bool),
        list_pull_requests=dict(required=False, type=bool),
        describe_repository=dict(required=False, type=bool),
        describe_repository_triggers=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_branches', True, ['name']),
            ('list_pull_requests', True, ['name']),
            ('describe_repository', True, ['name']),
            ('describe_repository_triggers', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_repositories',
                'list_branches',
                'list_pull_requests',
                'describe_repository',
                'describe_repository_triggers',
            )
        ],
    )

    client = module.client('codecommit', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codecommit(client, module)

    if module.params['list_repositories']:
        module.exit_json(repositories=aws_response_list_parser(paginate, _it, 'repositories'))
    elif module.params['list_branches']:
        module.exit_json(branches=aws_response_list_parser(paginate, _it, 'branches'))
    elif module.params['list_pull_requests']:
        module.exit_json(pull_request_ids=aws_response_list_parser(paginate, _it, 'pullRequestIds'))
    elif module.params['describe_repository']:
        module.exit_json(repository_metadata=camel_dict_to_snake_dict(_it['repositoryMetadata']))
    elif module.params['describe_repository_triggers']:
        module.exit_json(triggers=aws_response_list_parser(paginate, _it, 'triggers'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
