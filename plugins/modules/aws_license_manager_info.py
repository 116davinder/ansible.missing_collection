#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_license_manager_info
short_description: Get Information about AWS License Manager.
description:
  - Get Information about AWS License Manager.
  - U(https://docs.aws.amazon.com/license-manager/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  arn:
    description:
      - can be arn of license_configuration_arn ?
      - can be arn of license_arn?
    required: false
    type: str
    aliases: ['license_configuration_arn', 'license_arn']
  list_associations_for_license_configuration:
    description:
      - do you want to get list of associations_for_license_configuration for given I(arn)?
    required: false
    type: bool
  list_distributed_grants:
    description:
      - do you want to get list of distributed_grants?
    required: false
    type: bool
  list_failures_for_license_configuration_operations:
    description:
      - do you want to get list of key policies for given key I(arn)?
    required: false
    type: bool
  list_license_configurations:
    description:
      - do you want to get list of license_configurations?
    required: false
    type: bool
  list_license_versions:
    description:
      - do you want to get list of license_versions for given I(arn)?
    required: false
    type: bool
  list_received_distributed_grants:
    description:
      - do you want to get list of received_distributed_grants?
    required: false
    type: bool
  list_received_licenses:
    description:
      - do you want to get list of received_licenses?
    required: false
    type: bool
  list_tokens:
    description:
      - do you want to get list of tokens?
    required: false
    type: bool
  list_usage_for_license_configuration:
    description:
      - do you want to get list of usage_for_license_configuration for given I(arn)?
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
- name: "get list of associations_for_license_configuration"
  aws_license_manager_info:
    list_associations_for_license_configuration: true
    arn: 'test-license-config-arn'

- name: "get list of distributed_grants"
  aws_license_manager_info:
    list_distributed_grants: true

- name: "get list of failures_for_license_configuration_operations"
  aws_license_manager_info:
    list_failures_for_license_configuration_operations: true
    arn: 'test-license-config-arn'

- name: "get list of license_configurations"
  aws_license_manager_info:
    list_license_configurations: true

- name: "get list of license_versions"
  aws_license_manager_info:
    list_license_versions: true
    arn: 'test-license-arn'

- name: "get list of licenses"
  aws_license_manager_info:
    list_licenses: true

- name: "get list of received_distributed_grants"
  aws_license_manager_info:
    list_received_distributed_grants: true

- name: "get list of received_licenses"
  aws_license_manager_info:
    list_received_licenses: true

- name: "get list of tokens"
  aws_license_manager_info:
    list_tokens: true

- name: "get list of usage_for_license_configuration"
  aws_license_manager_info:
    list_usage_for_license_configuration: true
    arn: 'test-license-config-arn'
"""

RETURN = """
associations_for_license_configuration:
  description: list of associations_for_license_configuration.
  returned: when `list_associations_for_license_configuration` is defined and success.
  type: list
distributed_grants:
  description: list of distributed_grants.
  returned: when `list_distributed_grants` is defined and success.
  type: list
failures_for_license_configuration_operations:
  description: list of failures_for_license_configuration_operations.
  returned: when `list_failures_for_license_configuration_operations` is defined and success.
  type: list
license_configurations:
  description: list of license_configurations.
  returned: when `list_license_configurations` is defined and success.
  type: list
license_versions:
  description: list of license_versions.
  returned: when `list_license_versions` is defined and success.
  type: list
licenses:
  description: list of licenses.
  returned: when `list_licenses` is defined and success.
  type: list
received_distributed_grants:
  description: list of received_distributed_grants.
  returned: when `list_received_distributed_grants` is defined and success.
  type: list
received_licenses:
  description: list of received_licenses.
  returned: when `list_received_licenses` is defined and success.
  type: list
tokens:
  description: list of tokens.
  returned: when `list_tokens` is defined and success.
  type: list
usage_for_license_configuration:
  description: list of usage_for_license_configuration.
  returned: when `list_usage_for_license_configuration` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _license_manager(client, module):
    try:
        if module.params['list_associations_for_license_configuration']:
            if client.can_paginate('list_associations_for_license_configuration'):
                paginator = client.get_paginator('list_associations_for_license_configuration')
                return paginator.paginate(
                    LicenseConfigurationArn=module.params['arn']
                ), True
            else:
                return client.list_associations_for_license_configuration(
                    LicenseConfigurationArn=module.params['arn']
                ), False
        elif module.params['list_distributed_distributed_grants']:
            if client.can_paginate('list_distributed_distributed_grants'):
                paginator = client.get_paginator('list_distributed_distributed_grants')
                return paginator.paginate(), True
            else:
                return client.list_distributed_distributed_grants(), False
        elif module.params['list_failures_for_license_configuration_operations']:
            if client.can_paginate('list_failures_for_license_configuration_operations'):
                paginator = client.get_paginator('list_failures_for_license_configuration_operations')
                return paginator.paginate(
                    LicenseConfigurationArn=module.params['arn']
                ), True
            else:
                return client.list_failures_for_license_configuration_operations(
                    LicenseConfigurationArn=module.params['arn']
                ), False
        elif module.params['list_license_configurations']:
            if client.can_paginate('list_license_configurations'):
                paginator = client.get_paginator('list_license_configurations')
                return paginator.paginate(), True
            else:
                return client.list_license_configurations(), False
        elif module.params['list_license_versions']:
            if client.can_paginate('list_license_versions'):
                paginator = client.get_paginator('list_license_versions')
                return paginator.paginate(
                    LicenseArn=module.params['arn'],
                ), True
            else:
                return client.list_license_versions(
                    LicenseArn=module.params['arn'],
                ), False
        elif module.params['list_licenses']:
            if client.can_paginate('list_licenses'):
                paginator = client.get_paginator('list_licenses')
                return paginator.paginate(), True
            else:
                return client.list_licenses(), False
        elif module.params['list_received_distributed_grants']:
            if client.can_paginate('list_received_distributed_grants'):
                paginator = client.get_paginator('list_received_distributed_grants')
                return paginator.paginate(), True
            else:
                return client.list_received_distributed_grants(), False
        elif module.params['list_received_licenses']:
            if client.can_paginate('list_received_licenses'):
                paginator = client.get_paginator('list_received_licenses')
                return paginator.paginate(), True
            else:
                return client.list_received_licenses(), False
        elif module.params['list_tokens']:
            if client.can_paginate('list_tokens'):
                paginator = client.get_paginator('list_tokens')
                return paginator.paginate(), True
            else:
                return client.list_tokens(), False
        elif module.params['list_usage_for_license_configuration']:
            if client.can_paginate('list_usage_for_license_configuration'):
                paginator = client.get_paginator('list_usage_for_license_configuration')
                return paginator.paginate(
                    LicenseConfigurationArn=module.params['arn'],
                ), True
            else:
                return client.list_usage_for_license_configuration(
                    LicenseConfigurationArn=module.params['arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon license manager details')


def main():
    argument_spec = dict(
        arn=dict(required=False, associations_for_license_configuration=['license_configuration_arn', 'license_arn']),
        list_associations_for_license_configuration=dict(required=False, type=bool),
        list_distributed_distributed_grants=dict(required=False, type=bool),
        list_failures_for_license_configuration_operations=dict(required=False, type=bool),
        list_license_configurations=dict(required=False, type=bool),
        list_license_versions=dict(required=False, type=bool),
        list_licenses=dict(required=False, type=bool),
        list_received_distributed_grants=dict(required=False, type=bool),
        list_received_licenses=dict(required=False, type=bool),
        list_tokens=dict(required=False, type=bool),
        list_usage_for_license_configuration=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_associations_for_license_configuration', True, ['arn']),
            ('list_failures_for_license_configuration_operations', True, ['arn']),
            ('list_license_versions', True, ['arn']),
            ('list_usage_for_license_configuration', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_associations_for_license_configuration',
                'list_distributed_distributed_grants',
                'list_failures_for_license_configuration_operations',
                'list_license_configurations',
                'list_license_versions',
                'list_licenses',
                'list_received_distributed_grants',
                'list_received_licenses',
                'list_tokens',
                'list_usage_for_license_configuration',
            )
        ],
    )

    client = module.client('license-manager', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _license_manager(client, module)

    if module.params['list_associations_for_license_configuration']:
        module.exit_json(associations_for_license_configuration=aws_response_list_parser(paginate, it, 'LicenseConfigurationAssociations'))
    elif module.params['list_distributed_distributed_grants']:
        module.exit_json(distributed_distributed_grants=aws_response_list_parser(paginate, it, 'distributed_grants'))
    elif module.params['list_failures_for_license_configuration_operations']:
        module.exit_json(failures_for_license_configuration_operations=aws_response_list_parser(paginate, it, 'LicenseOperationFailureList'))
    elif module.params['list_license_configurations']:
        module.exit_json(license_configurations=aws_response_list_parser(paginate, it, 'LicenseConfigurations'))
    elif module.params['list_license_versions']:
        module.exit_json(license_versions=aws_response_list_parser(paginate, it, 'Licenses'))
    elif module.params['list_licenses']:
        module.exit_json(licenses=aws_response_list_parser(paginate, it, 'Licenses'))
    elif module.params['list_received_distributed_grants']:
        module.exit_json(received_distributed_grants=aws_response_list_parser(paginate, it, 'distributed_grants'))
    elif module.params['list_received_licenses']:
        module.exit_json(received_licenses=aws_response_list_parser(paginate, it, 'Licenses'))
    elif module.params['list_tokens']:
        module.exit_json(tokens=aws_response_list_parser(paginate, it, 'Tokens'))
    elif module.params['list_usage_for_license_configuration']:
        module.exit_json(usage_for_license_configuration=aws_response_list_parser(paginate, it, 'LicenseConfigurationUsageList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
