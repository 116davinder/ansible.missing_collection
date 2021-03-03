#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_lightsail_info
short_description: Get Information about Amazon Lightsail.
description:
  - Get Information about Amazon Lightsail.
  - U(https://docs.aws.amazon.com/lightsail/2016-11-28/api-reference/API_Operations.html)
version_added: 0.0.7
options:
  arn:
    description:
      - can be arn of resource name ?
      - can be arn of service name?
    required: false
    type: str
    aliases: ['resource_name', 'service_name']
  get_active_names:
    description:
      - do you want to get list of active_names?
    required: false
    type: bool
  list_alarms:
    description:
      - do you want to get list of alarms?
    required: false
    type: bool
  get_auto_snapshots:
    description:
      - do you want to get list of key policies for given key resource I(name)?
    required: false
    type: bool
  get_blueprints:
    description:
      - do you want to get list of blueprints?
    required: false
    type: bool
  get_bundles:
    description:
      - do you want to get list of bundles?
    required: false
    type: bool
  get_cloud_formation_stack_records:
    description:
      - do you want to get list of cloud_formation_stack_records?
    required: false
    type: bool
  get_contact_methods:
    description:
      - do you want to get list of contact_methods?
    required: false
    type: bool
  get_container_images:
    description:
      - do you want to get list of container_images for given service I(name)?
    required: false
    type: bool
  get_container_service_deployments:
    description:
      - do you want to get list of container_service_deployments for given service I(name)?
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
- name: "get list of active_names"
  aws_lightsail_info:
    get_active_names: true

- name: "get list of alarms"
  aws_lightsail_info:
    list_alarms: true

- name: "get list of auto_snapshots"
  aws_lightsail_info:
    get_auto_snapshots: true
    name: 'test-resource-name'

- name: "get list of blueprints"
  aws_lightsail_info:
    get_blueprints: true

- name: "get list of bundles"
  aws_lightsail_info:
    get_bundles: true

- name: "get list of certificates"
  aws_lightsail_info:
    get_certificates: true

- name: "get list of cloud_formation_stack_records"
  aws_lightsail_info:
    get_cloud_formation_stack_records: true

- name: "get list of contact_methods"
  aws_lightsail_info:
    get_contact_methods: true

- name: "get list of container_images"
  aws_lightsail_info:
    get_container_images: true
    name: 'test-service-name'

- name: "get list of container_service_deployments"
  aws_lightsail_info:
    get_container_service_deployments: true
    name: 'test-service-name'
"""

RETURN = """
active_names:
  description: list of active_names.
  returned: when `get_active_names` is defined and success.
  type: list
alarms:
  description: list of alarms.
  returned: when `list_alarms` is defined and success.
  type: list
auto_snapshots:
  description: list of auto_snapshots.
  returned: when `get_auto_snapshots` is defined and success.
  type: list
blueprints:
  description: list of blueprints.
  returned: when `get_blueprints` is defined and success.
  type: list
bundles:
  description: list of bundles.
  returned: when `get_bundles` is defined and success.
  type: list
certificates:
  description: list of certificates.
  returned: when `get_certificates` is defined and success.
  type: list
cloud_formation_stack_records:
  description: list of cloud_formation_stack_records.
  returned: when `get_cloud_formation_stack_records` is defined and success.
  type: list
contact_methods:
  description: list of contact_methods.
  returned: when `get_contact_methods` is defined and success.
  type: list
container_images:
  description: list of container_images.
  returned: when `get_container_images` is defined and success.
  type: list
container_service_deployments:
  description: list of container_service_deployments.
  returned: when `get_container_service_deployments` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _lightsail(client, module):
    try:
        if module.params['get_active_names']:
            if client.can_paginate('get_active_names'):
                paginator = client.get_paginator('get_active_names')
                return paginator.paginate(), True
            else:
                return client.get_active_names(), False
        elif module.params['get_alarms']:
            if client.can_paginate('get_alarms'):
                paginator = client.get_paginator('get_alarms')
                return paginator.paginate(), True
            else:
                return client.get_alarms(), False
        elif module.params['get_auto_snapshots']:
            if client.can_paginate('get_auto_snapshots'):
                paginator = client.get_paginator('get_auto_snapshots')
                return paginator.paginate(
                    resourceName=module.params['name']
                ), True
            else:
                return client.get_auto_snapshots(
                    resourceName=module.params['name']
                ), False
        elif module.params['get_blueprints']:
            if client.can_paginate('get_blueprints'):
                paginator = client.get_paginator('get_blueprints')
                return paginator.paginate(), True
            else:
                return client.get_blueprints(), False
        elif module.params['get_bundles']:
            if client.can_paginate('get_bundles'):
                paginator = client.get_paginator('get_bundles')
                return paginator.paginate(), True
            else:
                return client.get_bundles(), False
        elif module.params['get_certificates']:
            if client.can_paginate('get_certificates'):
                paginator = client.get_paginator('get_certificates')
                return paginator.paginate(), True
            else:
                return client.get_certificates(), False
        elif module.params['get_cloud_formation_stack_records']:
            if client.can_paginate('get_cloud_formation_stack_records'):
                paginator = client.get_paginator('get_cloud_formation_stack_records')
                return paginator.paginate(), True
            else:
                return client.get_cloud_formation_stack_records(), False
        elif module.params['get_contact_methods']:
            if client.can_paginate('get_contact_methods'):
                paginator = client.get_paginator('get_contact_methods')
                return paginator.paginate(), True
            else:
                return client.get_contact_methods(), False
        elif module.params['get_container_images']:
            if client.can_paginate('get_container_images'):
                paginator = client.get_paginator('get_container_images')
                return paginator.paginate(
                    serviceName=module.params['name']
                ), True
            else:
                return client.get_container_images(
                    serviceName=module.params['name']
                ), False
        elif module.params['get_container_service_deployments']:
            if client.can_paginate('get_container_service_deployments'):
                paginator = client.get_paginator('get_container_service_deployments')
                return paginator.paginate(
                    serviceName=module.params['name'],
                ), True
            else:
                return client.get_container_service_deployments(
                    serviceName=module.params['name'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Lightsail details')


def main():
    argument_spec = dict(
        name=dict(required=False, active_names=['resource_name', 'service_name']),
        get_active_names=dict(required=False, type=bool),
        get_alarms=dict(required=False, type=bool),
        get_auto_snapshots=dict(required=False, type=bool),
        get_blueprints=dict(required=False, type=bool),
        get_bundles=dict(required=False, type=bool),
        get_certificates=dict(required=False, type=bool),
        get_cloud_formation_stack_records=dict(required=False, type=bool),
        get_contact_methods=dict(required=False, type=bool),
        get_container_images=dict(required=False, type=bool),
        get_container_service_deployments=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_auto_snapshots', True, ['name']),
            ('get_container_images', True, ['name']),
            ('get_container_service_deployments', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'get_active_names',
                'get_alarms',
                'get_auto_snapshots',
                'get_blueprints',
                'get_bundles',
                'get_certificates',
                'get_cloud_formation_stack_records',
                'get_contact_methods',
                'get_container_images',
                'get_container_service_deployments',
            )
        ],
    )

    client = module.client('license-manager', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _lightsail(client, module)

    if module.params['get_active_names']:
        module.exit_json(active_names=aws_response_list_parser(paginate, it, 'activeNames'))
    elif module.params['get_alarms']:
        module.exit_json(alarms=aws_response_list_parser(paginate, it, 'alarms'))
    elif module.params['get_auto_snapshots']:
        module.exit_json(auto_snapshots=aws_response_list_parser(paginate, it, 'autoSnapshots'))
    elif module.params['get_blueprints']:
        module.exit_json(blueprints=aws_response_list_parser(paginate, it, 'blueprints'))
    elif module.params['get_bundles']:
        module.exit_json(bundles=aws_response_list_parser(paginate, it, 'bundles'))
    elif module.params['get_certificates']:
        module.exit_json(certificates=aws_response_list_parser(paginate, it, 'certificates'))
    elif module.params['get_cloud_formation_stack_records']:
        module.exit_json(cloud_formation_stack_records=aws_response_list_parser(paginate, it, 'cloudFormationStackRecords'))
    elif module.params['get_contact_methods']:
        module.exit_json(contact_methods=aws_response_list_parser(paginate, it, 'contactMethods'))
    elif module.params['get_container_images']:
        module.exit_json(container_images=aws_response_list_parser(paginate, it, 'containerImages'))
    elif module.params['get_container_service_deployments']:
        module.exit_json(container_service_deployments=aws_response_list_parser(paginate, it, 'deployments'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
