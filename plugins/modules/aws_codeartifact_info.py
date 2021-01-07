#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codeartifact_info
short_description: Get Information about AWS Code Artifact.
description:
  - Get Information about AWS Code Artifact.
  - U(https://docs.aws.amazon.com/codeartifact/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  prefix:
    description:
      - can be used as repositoryPrefix?
      - can be used as packagePrefix?
    required: false
    type: str
  domain:
    description:
      - name of the codeartifact domain.
    required: false
    type: str
  repository:
    description:
      - name of the codeartifact repository.
    required: false
    type: str
  package:
    description:
      - name of the codeartifact package.
    required: false
    type: str
  format:
    description:
      - type of codeartifact package.
    required: false
    type: str
    choices: ['npm', 'pypi', 'maven', 'nuget']
  list_repositories:
    description:
      - do you want to get list of repository for given I(prefix)?
    required: false
    type: bool
  list_repositories_in_domain:
    description:
      - do you want to get list of repository in specific domain for given I(prefix) and I(domain)?
    required: false
    type: bool
  list_packages:
    description:
      - do you want to get list of repository packages for given I(prefix), I(domain), I(format) and I(repository)?
    required: false
    type: bool
  describe_domain:
    description:
      - do you want to get details about given I(domain)?
    required: false
    type: bool
  describe_repository:
    description:
      - do you want to get details about given I(repository) in given I(domain)?
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
- name: "get list of all domains"
  aws_codeartifact_info:

- name: "get list of repositories"
  aws_codeartifact_info:
    list_repositories: true
    prefix: 'test'      # works as repositoryPrefix

- name: "get list of repositories in a domain"
  aws_codeartifact_info:
    list_repositories_in_domain: true
    prefix: 'test'      # works as repositoryPrefix
    domain: 'test'

- name: "get list of packages in a repository"
  aws_codeartifact_info:
    list_packages: true
    prefix: 'test'    # works as packagePrefix
    domain: 'test'
    repository: 'test-hola'
    format: 'pypi'

- name: "get details about domain"
  aws_codeartifact_info:
    describe_domain: true
    domain: 'test'

- name: "get details about repository"
  aws_codeartifact_info:
    describe_repository: true
    domain: 'test'
    repository: 'test-hola'
"""

RETURN = """
domains:
  description: List of codeartifact domains.
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'owner': 'string',
        'arn': 'string',
        'status': 'Active',
        'created_time': datetime(2015, 1, 1),
        'encryption_key': 'string'
    },
  ]
repositories:
  description: list of all repositories or Domain specific repositories
  returned: when (`list_repositories` and `prefix`) or (`list_repositories_in_domain`, `prefix` and `domain`) are defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'administrator_account': 'string',
        'domain_name': 'string',
        'domain_owner': 'string',
        'arn': 'string',
        'description': 'string'
    },
  ]
packages:
  description: list of all packages from specific repositories
  returned: when `list_packages`, `prefix`, `repository`, `format` and `domain` are defined and success
  type: list
  sample: [
    {
        'format': 'npm',
        'namespace': 'string',
        'package': 'string'
    },
  ]
domain:
  description: details about specific domain
  returned: when `describe_domain`, and `domain` are defined and success
  type: dict
  sample: {
    'name': 'string',
    'owner': 'string',
    'arn': 'string',
    'status': 'Active',
    'created_time': datetime(2015, 1, 1),
    'encryption_key': 'string',
    'repository_count': 123,
    'asset_size_bytes': 123,
    's3_bucket_arn': 'string'
  }
repository:
  description: details about specific repository in a domain.
  returned: when `describe_repository`, `repository` and `domain` are defined and success
  type: dict
  sample: {
    'name': 'string',
    'administrator_account': 'string',
    'domain_name': 'string',
    'domain_owner': 'string',
    'arn': 'string',
    'description': 'string',
    'upstreams': [
        {
            'repository_name': 'string'
        },
    ],
    'external_connections': [
        {
            'external_connection_name': 'string',
            'package_format': 'npm',
            'status': 'Available'
        },
    ]
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


def _cloudtrail(client, module):
    try:
        if module.params['list_repositories']:
            if client.can_paginate('list_repositories'):
                paginator = client.get_paginator('list_repositories')
                return paginator.paginate(
                    repositoryPrefix=module.params['prefix']
                ), True
            else:
                return client.list_repositories(
                    repositoryPrefix=module.params['prefix']
                ), False
        elif module.params['list_repositories_in_domain']:
            if client.can_paginate('list_repositories_in_domain'):
                paginator = client.get_paginator('list_repositories_in_domain')
                return paginator.paginate(
                    domain=module.params['domain'],
                    repositoryPrefix=module.params['prefix']
                ), True
            else:
                return client.list_repositories_in_domain(
                    domain=module.params['domain'],
                    repositoryPrefix=module.params['prefix']
                ), False
        elif module.params['list_packages']:
            if client.can_paginate('list_packages'):
                paginator = client.get_paginator('list_packages')
                return paginator.paginate(
                    domain=module.params['domain'],
                    format=module.params['format'],
                    repository=module.params['repository'],
                    packagePrefix=module.params['prefix'],
                ), True
            else:
                return client.list_packages(
                    domain=module.params['domain'],
                    format=module.params['format'],
                    repository=module.params['repository'],
                    packagePrefix=module.params['prefix'],
                ), False
        elif module.params['describe_domain']:
            return client.describe_domain(
                domain=module.params['domain'],
            ), False
        elif module.params['describe_repository']:
            return client.describe_repository(
                domain=module.params['domain'],
                repository=module.params['repository'],
            ), False
        else:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(), True
            else:
                return client.list_domains(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudtrail details')


def main():
    argument_spec = dict(
        prefix=dict(required=False),
        domain=dict(required=False),
        repository=dict(required=False),
        package=dict(required=False),
        format=dict(required=False, choices=['npm', 'pypi', 'maven', 'nuget']),
        list_repositories=dict(required=False, type=bool),
        list_repositories_in_domain=dict(required=False, type=bool),
        list_packages=dict(required=False, type=bool),
        describe_domain=dict(required=False, type=bool),
        describe_repository=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_repositories', True, ['prefix']),
            ('list_repositories_in_domain', True, ['prefix', 'domain']),
            ('list_packages', True, ['prefix', 'domain', 'repository', 'format']),
            ('describe_domain', True, ['domain']),
            ('describe_repository', True, ['domain', 'repository']),
        ),
        mutually_exclusive=[
            (
                'list_repositories',
                'list_repositories_in_domain',
                'list_packages',
                'describe_domain',
                'describe_repository',
            )
        ],
    )

    client = module.client('codeartifact', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudtrail(client, module)

    if module.params['list_repositories'] or module.params['list_repositories_in_domain']:
        module.exit_json(repositories=aws_response_list_parser(paginate, _it, 'repositories'))
    elif module.params['list_packages']:
        module.exit_json(packages=aws_response_list_parser(paginate, _it, 'packages'))
    elif module.params['describe_domain']:
        module.exit_json(domain=camel_dict_to_snake_dict(_it['domain']))
    elif module.params['describe_repository']:
        module.exit_json(repository=camel_dict_to_snake_dict(_it['repository']))
    else:
        module.exit_json(domains=aws_response_list_parser(paginate, _it, 'domains'))


if __name__ == '__main__':
    main()
