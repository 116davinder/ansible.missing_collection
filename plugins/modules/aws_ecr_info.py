#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ecr_info
short_description: Get Information about Amazon EC2 Container Registry (ECR).
description:
  - Get Information about Amazon EC2 Container Registry (ECR).
  - U(https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of the ecr registry.
    required: false
    type: str
  name:
    description:
      - name of ecr repository.
    required: false
    type: str
  tag_status:
    description:
      - tag status on ecr images.
    required: false
    type: str
    choices: ['TAGGED', 'UNTAGGED', 'ANY']
    default: 'ANY'
  describe_repositories:
    description:
      - do you want to get details of repository for given I(id)?
    required: false
    type: bool
  list_images:
    description:
      - do you want to get list of ecr images for given I(id) and I(name)?
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
- name: "Gets detailed information registry."
  aws_ecr_info:
  register: _reg

- name: "Gets detailed information about the repositories."
  aws_ecr_info:
    describe_repositories: true
    id: '{{ _reg.registry.registry_id }}'

- name: "Gets list of images for given repository and registry."
  aws_ecr_info:
    list_images: true
    id: '{{ _reg.registry.registry_id }}'
    name: 'test-repository-name'
    tag_status: 'ANY'
"""

RETURN = """
registry:
  description: detailed information registry.
  returned: when no arguments are defined and success
  type: dict
repositories:
  description: detailed information about the repositories.
  returned: when `describe_repositories` and `id` are defined and success
  type: list
images:
  description: list of images for given repository and registry.
  returned: when `list_images`, `name` and `id` are defined and success
  type: list
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


def _ecr(client, module):
    try:
        if module.params['describe_repositories']:
            if client.can_paginate('describe_repositories'):
                paginator = client.get_paginator('describe_repositories')
                return paginator.paginate(
                    registryId=module.params['id'],
                ), True
            else:
                return client.describe_repositories(
                    registryId=module.params['id'],
                ), False
        elif module.params['list_images']:
            if client.can_paginate('list_images'):
                paginator = client.get_paginator('list_images')
                return paginator.paginate(
                    registryId=module.params['id'],
                    repositoryName=module.params['name'],
                    filter={
                        'tagStatus': module.params['tag_status']
                    }
                ), True
            else:
                return client.list_images(
                    registryId=module.params['id'],
                    repositoryName=module.params['name'],
                    filter={
                        'tagStatus': module.params['tag_status']
                    }
                ), False
        else:
            return client.describe_registry(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS ECR details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        name=dict(required=False),
        tag_status=dict(required=False, choices=['TAGGED', 'UNTAGGED', 'ANY'], default='ANY'),
        describe_repositories=dict(required=False, type=bool),
        list_images=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_repositories', True, ['id']),
            ('list_images', True, ['id', 'name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('ecr', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ecr(client, module)

    if module.params['describe_repositories']:
        module.exit_json(repositories=aws_response_list_parser(paginate, it, 'repositories'))
    elif module.params['list_images']:
        module.exit_json(images=aws_response_list_parser(paginate, it, 'imageIds'))
    else:
        module.exit_json(registry=camel_dict_to_snake_dict(it))


if __name__ == '__main__':
    main()
