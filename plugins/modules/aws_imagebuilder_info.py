#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_imagebuilder_info
short_description: Get Information about EC2 Image Builder (imagebuilder).
description:
  - Get Information about EC2 Image Builder (imagebuilder).
  - U(https://docs.aws.amazon.com/imagebuilder/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  arn:
    description:
      - can be arn of image?
      - can be arn of image pipeline?
    required: false
    type: str
    aliases: ['image_version_arn', 'image_pipeline_arn']
  owner:
    description:
      - who is owner of resource?
    required: false
    type: str
    choices: ['Self', 'Shared', 'Amazon']
    default: 'Self'
  list_components:
    description:
      - do you want to get list of components for given I(owner)?
    required: false
    type: bool
  list_container_recipes:
    description:
      - do you want to get list of container recipes for given I(owner)?
    required: false
    type: bool
  list_distribution_configurations:
    description:
      - do you want to get list of distribution configurations?
    required: false
    type: bool
  list_image_build_versions:
    description:
      - do you want to get list of image build versions for given I(arn)?
    required: false
    type: bool
  list_image_pipeline_images:
    description:
      - do you want to get list of image pipeline images for given I(arn)?
    required: false
    type: bool
  list_image_pipelines:
    description:
      - do you want to get list of image pipelines?
    required: false
    type: bool
  list_image_recipes:
    description:
      - do you want to get list of image recipes for given I(owner)?
    required: false
    type: bool
  list_images:
    description:
      - do you want to get list of images for given I(owner)?
    required: false
    type: bool
  list_infrastructure_configurations:
    description:
      - do you want to get list of infrastructure configurations?
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
- name: "get list of components"
  aws_imagebuilder_info:
    list_components: true
    owner: 'Self'

- name: "get list of container_recipes"
  aws_imagebuilder_info:
    list_container_recipes: true
    owner: 'Self'

- name: "get list of distribution_configurations"
  aws_imagebuilder_info:
    list_distribution_configurations: true

- name: "get list of image_build_versions"
  aws_imagebuilder_info:
    list_image_build_versions: true
    arn: 'test-image-arn'

- name: "get list of image_pipeline_images"
  aws_imagebuilder_info:
    list_image_pipeline_images: true
    arn: 'test-image-pipeline-arn'

- name: "get list of image_pipelines"
  aws_imagebuilder_info:
    list_image_pipelines: true

- name: "get list of image_recipes"
  aws_imagebuilder_info:
    list_image_recipes: true
    owner: 'Self'

- name: "get list of images"
  aws_imagebuilder_info:
    list_images: true
    owner: 'Self'

- name: "get list of infrastructure_configurations"
  aws_imagebuilder_info:
    list_infrastructure_configurations: true
"""

RETURN = """
components:
  description: list of components.
  returned: when `list_components` is defined and success.
  type: list
container_recipes:
  description: list of container_recipes.
  returned: when `list_container_recipes` is defined and success.
  type: list
distribution_configurations:
  description: list of distribution_configurations.
  returned: when `list_distribution_configurations` is defined and success.
  type: list
image_build_versions:
  description: list of image_build_versions.
  returned: when `list_image_build_versions` is defined and success.
  type: list
image_pipeline_images:
  description: list of image_pipeline_images.
  returned: when `list_image_pipeline_images` is defined and success.
  type: list
image_pipelines:
  description: list of image_pipelines.
  returned: when `list_image_pipelines` is defined and success.
  type: list
image_recipes:
  description: list of image_recipes.
  returned: when `list_image_recipes` is defined and success.
  type: list
images:
  description: list of images.
  returned: when `list_images` is defined and success.
  type: list
infrastructure_configurations:
  description: list of infrastructure_configurations.
  returned: when `list_infrastructure_configurations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _imagebuilder(client, module):
    try:
        if module.params['list_components']:
            if client.can_paginate('list_components'):
                paginator = client.get_paginator('list_components')
                return paginator.paginate(
                    owner=module.params['owner']
                ), True
            else:
                return client.list_components(
                    owner=module.params['owner']
                ), False
        elif module.params['list_container_recipes']:
            if client.can_paginate('list_container_recipes'):
                paginator = client.get_paginator('list_container_recipes')
                return paginator.paginate(
                    owner=module.params['owner']
                ), True
            else:
                return client.list_container_recipes(
                    owner=module.params['owner']
                ), False
        elif module.params['list_distribution_configurations']:
            if client.can_paginate('list_distribution_configurations'):
                paginator = client.get_paginator('list_distribution_configurations')
                return paginator.paginate(), True
            else:
                return client.list_distribution_configurations(), False
        elif module.params['list_image_build_versions']:
            if client.can_paginate('list_image_build_versions'):
                paginator = client.get_paginator('list_image_build_versions')
                return paginator.paginate(
                    imageVersionArn=module.params['arn']
                ), True
            else:
                return client.list_image_build_versions(
                    imageVersionArn=module.params['arn']
                ), False
        elif module.params['list_image_pipeline_images']:
            if client.can_paginate('list_image_pipeline_images'):
                paginator = client.get_paginator('list_image_pipeline_images')
                return paginator.paginate(
                    imagePipelineArn=module.params['arn']
                ), True
            else:
                return client.list_image_pipeline_images(
                    imagePipelineArn=module.params['arn']
                ), False
        elif module.params['list_image_pipelines']:
            if client.can_paginate('list_image_pipelines'):
                paginator = client.get_paginator('list_image_pipelines')
                return paginator.paginate(), True
            else:
                return client.list_image_pipelines(), False
        elif module.params['list_image_recipes']:
            if client.can_paginate('list_image_recipes'):
                paginator = client.get_paginator('list_image_recipes')
                return paginator.paginate(
                    owner=module.params['owner']
                ), True
            else:
                return client.list_image_recipes(
                    owner=module.params['owner']
                ), False
        elif module.params['list_images']:
            if client.can_paginate('list_images'):
                paginator = client.get_paginator('list_images')
                return paginator.paginate(
                    owner=module.params['owner']
                ), True
            else:
                return client.list_images(
                    owner=module.params['owner']
                ), False
        elif module.params['list_infrastructure_configurations']:
            if client.can_paginate('list_infrastructure_configurations'):
                paginator = client.get_paginator('list_infrastructure_configurations')
                return paginator.paginate(), True
            else:
                return client.list_infrastructure_configurations(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon EC2 Image Builder details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['image_version_arn', 'image_pipeline_arn']),
        owner=dict(required=False, choices=['Self', 'Shared', 'Amazon'], default='Self'),
        list_components=dict(required=False, type=bool),
        list_container_recipes=dict(required=False, type=bool),
        list_distribution_configurations=dict(required=False, type=bool),
        list_image_build_versions=dict(required=False, type=bool),
        list_image_pipeline_images=dict(required=False, type=bool),
        list_image_pipelines=dict(required=False, type=bool),
        list_image_recipes=dict(required=False, type=bool),
        list_images=dict(required=False, type=bool),
        list_infrastructure_configurations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_image_build_versions', True, ['arn']),
            ('list_image_pipeline_images', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_components',
                'list_container_recipes',
                'list_distribution_configurations',
                'list_image_build_versions',
                'list_image_pipeline_images',
                'list_image_pipelines',
                'list_image_recipes',
                'list_images',
                'list_infrastructure_configurations',
            )
        ],
    )

    client = module.client('imagebuilder', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _imagebuilder(client, module)

    if module.params['list_components']:
        module.exit_json(components=aws_response_list_parser(paginate, it, 'componentVersionList'))
    elif module.params['list_container_recipes']:
        module.exit_json(container_recipes=aws_response_list_parser(paginate, it, 'containerRecipeSummaryList'))
    elif module.params['list_distribution_configurations']:
        module.exit_json(distribution_configurations=aws_response_list_parser(paginate, it, 'distributionConfigurationSummaryList'))
    elif module.params['list_image_build_versions']:
        module.exit_json(image_build_versions=aws_response_list_parser(paginate, it, 'imageSummaryList'))
    elif module.params['list_image_pipeline_images']:
        module.exit_json(image_pipeline_images=aws_response_list_parser(paginate, it, 'imageSummaryList'))
    elif module.params['list_image_pipelines']:
        module.exit_json(image_pipelines=aws_response_list_parser(paginate, it, 'imagePipelineList'))
    elif module.params['list_image_recipes']:
        module.exit_json(image_recipes=aws_response_list_parser(paginate, it, 'imageRecipeSummaryList'))
    elif module.params['list_images']:
        module.exit_json(images=aws_response_list_parser(paginate, it, 'imageVersionList'))
    elif module.params['list_infrastructure_configurations']:
        module.exit_json(infrastructure_configurations=aws_response_list_parser(paginate, it, 'infrastructureConfigurationSummaryList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
