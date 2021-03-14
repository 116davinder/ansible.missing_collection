#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mediastore_info
short_description: Get Information about AWS Elemental MediaStore.
description:
  - Get Information about AWS Elemental MediaStore.
  - U(https://docs.aws.amazon.com/mediastore/latest/api/resources.html)
version_added: 0.0.7
options:
  name:
    description:
      - container name.
    required: false
    type: str
  list_containers:
    description:
      - do you want to get list of channels?
    required: false
    type: bool
  get_container_policy:
    description:
      - do you want to get container_policy for given I(name)?
    required: false
    type: bool
  get_cors_policy:
    description:
      - do you want to get list of cors_policy for given I(name)?
    required: false
    type: bool
  get_lifecycle_policy:
    description:
      - do you want to get lifecycle_policy for given I(name)?
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
- name: "get list of channels"
  aws_mediastore_info:
    list_containers: true

- name: "get container_policy"
  aws_mediastore_info:
    get_container_policy: true
    name: 'container-name'

- name: "get list of cors_policy"
  aws_mediastore_info:
    get_cors_policy: true
    name: 'container-name'

- name: "get lifecycle_policy"
  aws_mediastore_info:
    get_lifecycle_policy: true
    name: 'container-name'
"""

RETURN = """
channels:
  description: list of channels.
  returned: when `list_containers` is defined and success.
  type: list
container_policy:
  description: get of container_policy.
  returned: when `get_container_policy` is defined and success.
  type: dict
cors_policy:
  description: list of cors_policy.
  returned: when `get_cors_policy` is defined and success.
  type: list
lifecycle_policy:
  description: get of lifecycle_policy.
  returned: when `get_lifecycle_policy` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _mediastore(client, module):
    try:
        if module.params['list_containers']:
            if client.can_paginate('list_containers'):
                paginator = client.get_paginator('list_containers')
                return paginator.paginate(), True
            else:
                return client.list_containers(), False
        elif module.params['get_container_policy']:
            if client.can_paginate('get_container_policy'):
                paginator = client.get_paginator('get_container_policy')
                return paginator.paginate(
                    ContainerName=module.params['name']
                ), True
            else:
                return client.get_container_policy(
                    ContainerName=module.params['name']
                ), False
        elif module.params['get_cors_policy']:
            if client.can_paginate('get_cors_policy'):
                paginator = client.get_paginator('get_cors_policy')
                return paginator.paginate(
                    ContainerName=module.params['name']
                ), True
            else:
                return client.get_cors_policy(
                    ContainerName=module.params['name']
                ), False
        elif module.params['get_lifecycle_policy']:
            if client.can_paginate('get_lifecycle_policy'):
                paginator = client.get_paginator('get_lifecycle_policy')
                return paginator.paginate(
                    ContainerName=module.params['name']
                ), True
            else:
                return client.get_lifecycle_policy(
                    ContainerName=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elemental MediaStore details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['container_name']),
        list_containers=dict(required=False, type=bool),
        get_container_policy=dict(required=False, type=bool),
        get_cors_policy=dict(required=False, type=bool),
        get_lifecycle_policy=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_container_policy', True, ['name']),
            ('get_cors_policy', True, ['name']),
            ('get_lifecycle_policy', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_containers',
                'get_container_policy',
                'get_cors_policy',
                'get_lifecycle_policy',
            )
        ],
    )

    client = module.client('mediastore', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mediastore(client, module)

    if module.params['list_containers']:
        module.exit_json(containers=aws_response_list_parser(paginate, it, 'Containers'))
    elif module.params['get_container_policy']:
        module.exit_json(container_policy=camel_dict_to_snake_dict(it))
    elif module.params['get_cors_policy']:
        module.exit_json(cors_policy=aws_response_list_parser(paginate, it, 'CorsPolicy'))
    elif module.params['get_lifecycle_policy']:
        module.exit_json(lifecycle_policy=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
