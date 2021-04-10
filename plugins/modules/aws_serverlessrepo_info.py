#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_serverlessrepo_info
short_description: Get Information about AWS Serverless Application Repository.
description:
  - Get Information about AWS Serverless Application Repository.
  - U(https://docs.aws.amazon.com/serverlessrepo/latest/devguide/resources.html)
version_added: 0.0.9
options:
  id:
    description:
      - application id.
    required: false
    type: str
    aliases: ['application_id']
  list_application_dependencies:
    description:
      - do you want to get list of application_dependencies for given I(id)?
    required: false
    type: bool
  list_application_versions:
    description:
      - do you want to get application_versions for given I(id)?
    required: false
    type: bool
  list_applications:
    description:
      - do you want to get list of applications?
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
- name: "get list of application_dependencies"
  aws_serverlessrepo_info:
    list_application_dependencies: true
    id: 'application_id'

- name: "get application_versions"
  aws_serverlessrepo_info:
    list_application_versions: true
    id: 'application_id'

- name: "get list of applications"
  aws_serverlessrepo_info:
    list_applications: true
"""

RETURN = """
application_dependencies:
  description: list of application_dependencies.
  returned: when `list_application_dependencies` is defined and success.
  type: list
application_versions:
  description: get of application_versions.
  returned: when `list_application_versions` is defined and success.
  type: list
applications:
  description: list of applications.
  returned: when `list_applications` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _serverlessrepo(client, module):
    try:
        if module.params['list_application_dependencies']:
            if client.can_paginate('list_application_dependencies'):
                paginator = client.get_paginator('list_application_dependencies')
                return paginator.paginate(
                    ApplicationId=module.params['id']
                ), True
            else:
                return client.list_application_dependencies(
                    ApplicationId=module.params['id']
                ), False
        elif module.params['list_application_versions']:
            if client.can_paginate('list_application_versions'):
                paginator = client.get_paginator('list_application_versions')
                return paginator.paginate(
                    ApplicationId=module.params['id']
                ), True
            else:
                return client.list_application_versions(
                    ApplicationId=module.params['id']
                ), False
        elif module.params['list_applications']:
            if client.can_paginate('list_applications'):
                paginator = client.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return client.list_applications(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Serverless Application Repository details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['application_id']),
        list_application_dependencies=dict(required=False, type=bool),
        list_application_versions=dict(required=False, type=bool),
        list_applications=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_application_dependencies', True, ['id']),
            ('list_application_versions', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_application_dependencies',
                'list_application_versions',
                'list_applications',
            )
        ],
    )

    client = module.client('serverlessrepo', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _serverlessrepo(client, module)

    if module.params['list_application_dependencies']:
        module.exit_json(application_dependencies=aws_response_list_parser(paginate, it, 'Dependencies'))
    elif module.params['list_application_versions']:
        module.exit_json(application_versions=aws_response_list_parser(paginate, it, 'Versions'))
    elif module.params['list_applications']:
        module.exit_json(applications=aws_response_list_parser(paginate, it, 'Applications'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
