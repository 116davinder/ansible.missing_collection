#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ecr_public_info
short_description: Get Information about Amazon Elastic Container Registry Public (ECR Public).
description:
  - Get Information about Amazon Elastic Container Registry Public (ECR Public).
  - U(https://docs.aws.amazon.com/AmazonECRPublic/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of the ecr_public registry.
    required: false
    type: str
  name:
    description:
      - name of ecr_public repository.
    required: false
    type: str
  describe_repositories:
    description:
      - do you want to get details of repository for given I(id)?
    required: false
    type: bool
  describe_images:
    description:
      - do you want to get details of ecr_public images for given I(id) and I(name)?
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
- name: "Gets detailed information registries."
  aws_ecr_public_info:
  register: _reg

- name: "Gets detailed information about the repositories."
  aws_ecr_public_info:
    describe_repositories: true
    id: '{{ _reg.registries[0].registry_id }}'

- name: "Gets list of images for given repository and registry."
  aws_ecr_public_info:
    describe_images: true
    id: '{{ _reg.registries[0].registry_id }}'
    name: 'test-repository-name'
"""

RETURN = """
registries:
  description: detailed information about all registries.
  returned: when no arguments are defined and success
  type: list
repositories:
  description: detailed information about the repositories.
  returned: when `describe_repositories` and `id` are defined and success
  type: list
images:
  description: list of images for given repository and registry.
  returned: when `describe_images`, `name` and `id` are defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _ecr_public(client, module):
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
        elif module.params['describe_images']:
            if client.can_paginate('describe_images'):
                paginator = client.get_paginator('describe_images')
                return paginator.paginate(
                    registryId=module.params['id'],
                    repositoryName=module.params['name'],
                ), True
            else:
                return client.describe_images(
                    registryId=module.params['id'],
                    repositoryName=module.params['name'],
                ), False
        else:
            if client.can_paginate('describe_registries'):
                paginator = client.get_paginator('describe_registries')
                return paginator.paginate(), True
            else:
                return client.describe_registries(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS ecr_public details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        name=dict(required=False),
        describe_repositories=dict(required=False, type=bool),
        describe_images=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_repositories', True, ['id']),
            ('describe_images', True, ['id', 'name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('ecr-public', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ecr_public(client, module)

    if module.params['describe_repositories']:
        module.exit_json(repositories=aws_response_list_parser(paginate, it, 'repositories'))
    elif module.params['describe_images']:
        module.exit_json(images=aws_response_list_parser(paginate, it, 'imageDetails'))
    else:
        module.exit_json(registries=aws_response_list_parser(paginate, it, 'registries'))


if __name__ == '__main__':
    main()
