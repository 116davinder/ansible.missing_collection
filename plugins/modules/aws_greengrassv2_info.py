#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_greengrassv2_info
short_description: Get Information about Amazon Green Grass V2.
description:
  - Get Information about Amazon Green Grass V2.
  - U(https://docs.aws.amazon.com/greengrass/v2/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  name:
    description:
      - name of core device thing.
    required: false
    type: str
    aliases: ['core_device_thing_name']
  arn:
    description:
      - can be arn of target?
      - can be arn of component?
    required: false
    type: str
  scope:
    description:
      - scope of component.
    required: false
    type: str
    choices: ['PRIVATE', 'PUBLIC']
    default: 'PUBLIC'
  status:
    description:
      - status of core device.
    required: false
    type: str
    choices: ['HEALTHY', 'UNHEALTHY']
    default: 'HEALTHY'
  history_filter:
    description:
      - filter to reduce number of results for deployments.
    required: false
    type: str
    choices: ['ALL', 'LATEST_ONLY']
    default: 'ALL'
  list_component_versions:
    description:
      - do you want to get list of component_versions for given component I(arn)?
    required: false
    type: bool
  list_components:
    description:
      - do you want to get list of components for given I(scope)?
    required: false
    type: bool
  list_core_devices:
    description:
      - do you want to get list of core devices for given I(status)?
    required: false
    type: bool
  list_deployments:
    description:
      - do you want to get list of deployments for given target I(arn) and I(history_filter)?
    required: false
    type: bool
  list_effective_deployments:
    description:
      - do you want to get list of effective deployments for given core device thing I(name)?
    required: false
    type: bool
  list_installed_components:
    description:
      - do you want to get list of installed components for given core device thing I(name)??
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
- name: "get list of component_versions"
  aws_greengrassv2_info:
    list_component_versions: true
    arn: 'component-arn'

- name: "get list of components"
  aws_greengrassv2_info:
    list_components: true
    scope: 'PUBLIC'

- name: "get list of core devices"
  aws_greengrassv2_info:
    list_core_devices: true
    status: 'HEALTHY'

- name: "get list of deployments"
  aws_greengrassv2_info:
    list_deployments: true
    arn: 'target-arn'
    history_filter: 'ALL'

- name: "get list of effective deployments"
  aws_greengrassv2_info:
    list_effective_deployments: true
    name: 'core-device-thing-name'

- name: "get list of installed components"
  aws_greengrassv2_info:
    list_installed_components: true
    name: 'core-device-thing-name'
"""

RETURN = """
component_versions:
  description: list of component versions.
  returned: when `list_component_versions` is defined and success.
  type: list
components:
  description: list of components.
  returned: when `list_components` is defined and success.
  type: list
core_devices:
  description: list of core devices.
  returned: when `list_core_devices` is defined and success.
  type: list
deployments:
  description: list of deployments.
  returned: when `list_deployments` is defined and success.
  type: list
effective_deployments:
  description: list of effective deployments.
  returned: when `list_effective_deployments` is defined and success.
  type: list
installed_components:
  description: list of installed components.
  returned: when `list_installed_components` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _greengrassv2(client, module):
    try:
        if module.params['list_component_versions']:
            if client.can_paginate('list_component_versions'):
                paginator = client.get_paginator('list_component_versions')
                return paginator.paginate(
                    arn=module.params['arn']
                ), True
            else:
                return client.list_component_versions(
                    arn=module.params['arn']
                ), False
        elif module.params['list_components']:
            if client.can_paginate('list_components'):
                paginator = client.get_paginator('list_components')
                return paginator.paginate(
                    scope=module.params['scope']
                ), True
            else:
                return client.list_components(
                    scope=module.params['scope']
                ), False
        elif module.params['list_core_devices']:
            if client.can_paginate('list_core_devices'):
                paginator = client.get_paginator('list_core_devices')
                return paginator.paginate(
                    status=module.params['status']
                ), True
            else:
                return client.list_core_devices(
                    status=module.params['status']
                ), False
        elif module.params['list_deployments']:
            if client.can_paginate('list_deployments'):
                paginator = client.get_paginator('list_deployments')
                return paginator.paginate(
                    targetArn=module.params['arn'],
                    historyFilter=module.params['history_filter']
                ), True
            else:
                return client.list_deployments(
                    targetArn=module.params['arn'],
                    historyFilter=module.params['history_filter']
                ), False
        elif module.params['list_effective_deployments']:
            if client.can_paginate('list_effective_deployments'):
                paginator = client.get_paginator('list_effective_deployments')
                return paginator.paginate(
                    coreDeviceThingName=module.params['name']
                ), True
            else:
                return client.list_effective_deployments(
                    coreDeviceThingName=module.params['name']
                ), False
        elif module.params['list_installed_components']:
            if client.can_paginate('list_installed_components'):
                paginator = client.get_paginator('list_installed_components')
                return paginator.paginate(
                    coreDeviceThingName=module.params['name']
                ), True
            else:
                return client.list_installed_components(
                    coreDeviceThingName=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon greengrassv2 details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        name=dict(required=False, aliases=['core_device_thing_name']),
        scope=dict(required=False, choices=['PRIVATE', 'PUBLIC'], default='PUBLIC'),
        status=dict(required=False, choices=['HEALTHY', 'UNHEALTHY'], default='HEALTHY'),
        history_filter=dict(required=False, choices=['ALL', 'LATEST_ONLY'], default='ALL'),
        list_component_versions=dict(required=False, type=bool),
        list_components=dict(required=False, type=bool),
        list_core_devices=dict(required=False, type=bool),
        list_deployments=dict(required=False, type=bool),
        list_effective_deployments=dict(required=False, type=bool),
        list_installed_components=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_component_versions', True, ['arn']),
            ('list_deployments', True, ['arn']),
            ('list_effective_deployments', True, ['name']),
            ('list_installed_components', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_component_versions',
                'list_components',
                'list_core_devices',
                'list_deployments',
                'list_effective_deployments',
                'list_installed_components',
            )
        ],
    )

    client = module.client('greengrassv2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _greengrassv2(client, module)

    if module.params['list_component_versions']:
        module.exit_json(component_versions=aws_response_list_parser(paginate, it, 'componentVersions'))
    elif module.params['list_components']:
        module.exit_json(components=aws_response_list_parser(paginate, it, 'components'))
    elif module.params['list_core_devices']:
        module.exit_json(core_devices=aws_response_list_parser(paginate, it, 'coreDevices'))
    elif module.params['list_deployments']:
        module.exit_json(deployments=aws_response_list_parser(paginate, it, 'deployments'))
    elif module.params['list_effective_deployments']:
        module.exit_json(effective_deployments=aws_response_list_parser(paginate, it, 'effectiveDeployments'))
    elif module.params['list_installed_components']:
        module.exit_json(installed_components=aws_response_list_parser(paginate, it, 'installedComponents'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
