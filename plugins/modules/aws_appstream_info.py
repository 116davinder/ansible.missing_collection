#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_appstream_info
short_description: Get details about Amazon AppStream 2.0.
description:
  - Get Information about Amazon AppStream 2.0 API.
  - U(https://docs.aws.amazon.com/appstream2/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  names:
    description:
      - can be names of the fleets to describe?
      - can be names of the stacks to describe?
      - can be aws app stream directory names to describe?
      - can be names of the image builders to describe?
      - can be names of the public or private images to describe?
    required: false
    type: list
    default: []
  describe_fleets:
    description:
      - do you want to describe all appstreams fleet or given I(names) of fleets?
    required: false
    type: bool
  describe_directory_configs:
    description:
      - do you want to describe all appstreams directory configs or given I(names) of directory configs?
    required: false
    type: bool
  describe_image_builders:
    description:
      - do you want to describe all appstreams image builders or given I(names) of builders?
    required: false
    type: bool
  image_type:
    description:
      - what type of image will be decribed?
    required: false
    type: str
    choices: ['PUBLIC', 'PRIVATE', 'SHARED']
    default: 'PUBLIC'
  describe_images:
    description:
      - do you want to describe all appstreams images or given I(names) of images?
    required: false
    type: bool
  authentication_type:
    description:
      - what type of authentication for I(describe_user)?
    required: false
    type: str
    choices: ['API', 'SAML', 'USERPOOL']
    default: 'USERPOOL'
  describe_users:
    description:
      - do you want to describe appstreams user or given I(authentication_type)?
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
- name: "describe all fleets of aws app streams"
  aws_appstream_info:
    describe_fleets: true

- name: "describe all directory configs of aws app streams"
  aws_appstream_info:
    describe_directory_configs: true

- name: "describe all image builder of aws app streams"
  aws_appstream_info:
    describe_image_builders: true

- name: "describe all images of aws app streams"
  aws_appstream_info:
    describe_images: true
    image_type: 'PRIVATE'

- name: "describe all users of aws app streams"
  aws_appstream_info:
    describe_users: true
    authentication_type: 'USERPOOL'
"""

RETURN = """
fleets:
  description: Retrieves a list that describes one or more specified fleets, if the fleet names are provided.
  returned: when `names` and `describe_fleets` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'name': 'string',
          'display_name': 'string',
          'description': 'string',
          'image_name': 'string',
          'image_arn': 'string',
          'instance_type': 'string',
          'fleet_type': 'ALWAYS_ON',
          'compute_capacity_status': {},
          'max_user_duration_in_seconds': 123,
          'disconnect_timeout_in_seconds': 123,
          'state': 'STARTING',
          'vpc_config': {},
          'created_time': datetime(2015, 1, 1),
          'fleet_errors': [],
          'enable_default_internet_access': True,
          'domain_join_info': {},
          'idle_disconnect_timeout_in_seconds': 123,
          'iam_role_arn': 'string',
          'stream_view': 'APP'
      },
  ]
stacks:
  description: Retrieves a list that describes one or more specified stacks, if the stack names are provided.
  returned: when `names` and `describe_stacks` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'name': 'string',
          'description': 'string',
          'display_name': 'string',
          'created_time': datetime(2015, 1, 1),
          'storage_connectors': [],
          'redirect_url': 'string',
          'feedback_url': 'string',
          'stack_errors': [],
          'user_settings': [],
          'application_settings': {},
          'access_endpoints': [],
          'embed_host_domains': []
      },
  ]
directory_configs:
  description: Retrieves a list that describes one or more specified Directory Config objects for AppStream 2.0, if the names for these objects are provided.
  returned: when `names` and `describe_directory_configs` are defined and success
  type: list
  sample: [
      {
          'directory_name': 'string',
          'organizational_unit_distinguished_names': [],
          'service_account_credentials': {},
          'created_time': datetime(2015, 1, 1)
      },
  ]
image_builders:
  description: Retrieves a list that describes one or more specified image builders, if the image builder names are provided.
  returned: when `names` and `describe_image_builders` are defined and success
  type: list
  sample: [
      {
          'name': 'string',
          'arn': 'string',
          'image_arn': 'string',
          'description': 'string',
          'display_name': 'string',
          'vpc_config': {},
          'instance_type': 'string',
          'platform': 'WINDOWS',
          'iam_role_arn': 'string',
          'state': 'PENDING',
          'state_change_reason': {},
          'created_time': datetime(2015, 1, 1),
          'enable_default_internet_access': True,
          'domain_join_info': {},
          'network_access_configuration': {},
          'image_builder_errors': [],
          'appstream_agent_version': 'string',
          'access_endpoints': []
      },
  ]
images:
  description: Retrieves a list that describes one or more specified images, if the image names are provided.
  returned: when `names` and `describe_images` and `image_type` are defined and success
  type: list
  sample: [
      {
          'name': 'string',
          'arn': 'string',
          'base_image_arn': 'string',
          'display_name': 'string',
          'state': 'PENDING',
          'visibility': 'PUBLIC',
          'image_builder_supported': True|False,
          'image_builder_name': 'string',
          'platform': 'WINDOWS',
          'description': 'string',
          'state_change_reason': {},
          'applications': [],
          'created_time': datetime(2016, 10, 11),
          'public_base_image_released_date': datetime(2015, 1, 1),
          'appstream_agent_version': 'string',
          'image_permissions': {}
      },
  ]
users:
  description: Retrieves a list that describes one or more specified users in the user pool.
  returned: when `describe_users` and  `authentication_type` are defined and success
  type: list
  sample: [
    {
        'arn': 'string',
        'user_name': 'string',
        'enabled': True,
        'status': 'string',
        'first_name': 'string',
        'last_name': 'string',
        'created_time': datetime(2015, 1, 1),
        'authentication_type': 'USERPOOL'
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _appstream(client, module):
    try:
        if module.params['describe_fleets']:
            if client.can_paginate('describe_fleets'):
                paginator = client.get_paginator('describe_fleets')
                return paginator.paginate(
                    Names=module.params['names']
                ), True
            else:
                return client.describe_fleets(
                    Names=module.params['names']
                ), False
        elif module.params['describe_stacks']:
            if client.can_paginate('describe_stacks'):
                paginator = client.get_paginator('describe_stacks')
                return paginator.paginate(
                    Names=module.params['names']
                ), True
            else:
                return client.describe_stacks(
                    Names=module.params['names']
                ), False
        elif module.params['describe_directory_configs']:
            if client.can_paginate('describe_directory_configs'):
                paginator = client.get_paginator('describe_directory_configs')
                return paginator.paginate(
                    DirectoryNames=module.params['names']
                ), True
            else:
                return client.describe_directory_configs(
                    DirectoryNames=module.params['names']
                ), False
        elif module.params['describe_image_builders']:
            if client.can_paginate('describe_image_builders'):
                paginator = client.get_paginator('describe_image_builders')
                return paginator.paginate(
                    Names=module.params['names']
                ), True
            else:
                return client.describe_image_builders(
                    Names=module.params['names']
                ), False
        elif module.params['describe_images']:
            if client.can_paginate('describe_images'):
                paginator = client.get_paginator('describe_images')
                return paginator.paginate(
                    Names=module.params['names'],
                    Type=module.params['image_type']
                ), True
            else:
                return client.describe_images(
                    Names=module.params['names'],
                    Type=module.params['image_type']
                ), False
        elif module.params['describe_users']:
            if client.can_paginate('describe_users'):
                paginator = client.get_paginator('describe_users')
                return paginator.paginate(
                    AuthenticationType=module.params['authentication_type']
                ), True
            else:
                return client.describe_users(
                    AuthenticationType=module.params['authentication_type']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws appstream details')


def main():
    argument_spec = dict(
        names=dict(required=False, type=list, default=[]),
        describe_fleets=dict(required=False, type=bool),
        describe_stacks=dict(required=False, type=bool),
        describe_directory_configs=dict(required=False, type=bool),
        describe_image_builders=dict(required=False, type=bool),
        image_type=dict(required=False, choices=['PUBLIC', 'PRIVATE', 'SHARED'], default='PUBLIC'),
        describe_images=dict(required=False, type=bool),
        authentication_type=dict(required=False, choices=['API', 'SAML', 'USERPOOL'], default='USERPOOL'),
        describe_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_fleets', True, ['names']),
            ('describe_stacks', True, ['names']),
            ('describe_directory_configs', True, ['names']),
            ('describe_image_builders', True, ['names']),
            ('describe_images', True, ['names']),
            ('describe_users', True, ['authentication_type']),
        ],
        mutually_exclusive=[
            (
                'describe_fleets',
                'describe_stacks',
                'describe_directory_configs',
                'describe_image_builders',
                'describe_images',
                'describe_users',
            ),
        ],
    )

    client = module.client('appstream', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _appstream(client, module)

    if module.params['describe_fleets']:
        module.exit_json(fleets=aws_response_list_parser(paginate, _it, 'Fleets'))
    elif module.params['describe_stacks']:
        module.exit_json(stacks=aws_response_list_parser(paginate, _it, 'Stacks'))
    elif module.params['describe_directory_configs']:
        module.exit_json(directory_configs=aws_response_list_parser(paginate, _it, 'DirectoryConfigs'))
    elif module.params['describe_image_builders']:
        module.exit_json(image_builders=aws_response_list_parser(paginate, _it, 'ImageBuilders'))
    elif module.params['describe_images']:
        module.exit_json(images=aws_response_list_parser(paginate, _it, 'Images'))
    elif module.params['describe_users']:
        module.exit_json(users=aws_response_list_parser(paginate, _it, 'Users'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
