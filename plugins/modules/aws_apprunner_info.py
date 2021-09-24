#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_apprunner_info
short_description: Get Information about AWS Apprunner.
description:
  - Get Information about AWS Apprunner.
version_added: 0.2.0
options:
  arn:
    description:
      - service arn of apprunner.
    required: false
    type: str
    aliases: ['service_arn']
  list_auto_scaling_configurations:
    description:
      - do you want to fetch all the asg configurations?
    required: false
    type: bool
  list_connections:
    description:
      - do you want to fetch all the connections?
    required: false
    type: bool
  list_operations:
    description:
      - do you want to fetch all the apprunner operations of I(arn)?
    required: false
    type: bool
  list_services:
    description:
      - do you want to fetch all the services of apprunner?
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
- name: "get list of autoscaling configurations of apprunner"
  aws_apprunner_info:
    list_auto_scaling_configurations: true

- name: "get list of connections of apprunner"
  aws_apprunner_info:
    list_connections: true

- name: "get list of operations of apprunner"
  aws_apprunner_info:
    list_operations: true
    arn: 'test:arn'

- name: "get list of services of apprunner"
  aws_apprunner_info:
    list_services: true
"""

RETURN = """
auto_scaling_configuration_summary:
  description: List of ASG Configurations.
  returned: when I(list_auto_scaling_configurations) is defined and success
  type: list
  sample: [
    {
      "auto_scaling_configuration_arn": "arn:aws:apprunner:us-east-1:xxxxxx:autoscalingconfiguration/DefaultConfiguration/1/00000000000000000000000000000001",
      "auto_scaling_configuration_name": "DefaultConfiguration",
      "auto_scaling_configuration_revision": 1
    }
  ]
connection_summary:
  description: List of connections for apprunner.
  returned: when I(list_connections) and success
  type: list
  sample: [
      {
          'ConnectionName': 'string',
          'ConnectionArn': 'string',
          'ProviderType': 'GITHUB',
          'Status': 'PENDING_HANDSHAKE',
          'CreatedAt': "<date>"
      },
  ]
operation_summary:
  description: List of operations for given service I(arn).
  returned: when I(list_operations) and success
  type: list
  sample: [
      {
          'Id': 'string',
          'Type': 'START_DEPLOYMENT',
          'Status': 'PENDING',
          'TargetArn': 'string',
          'StartedAt': '<date>',
          'EndedAt': '<date>',
          'UpdatedAt': '<date>'
      },
  ]
services:
  description: List of apprunner services.
  returned: when I(services) and success
  type: list
  sample: [
      {
          'ServiceName': 'string',
          'ServiceId': 'string',
          'ServiceArn': 'string',
          'ServiceUrl': 'string',
          'CreatedAt': '<date>',
          'UpdatedAt': '<date>',
          'Status': 'CREATE_FAILED'
      },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _apprunner(module):
    try:
        apprunner = module.client('apprunner')

        if module.params['list_auto_scaling_configurations']:
            if apprunner.can_paginate('list_auto_scaling_configurations'):
                paginator = apprunner.get_paginator('list_auto_scaling_configurations')
                return paginator.paginate(
                    LatestOnly=False
                ), True
            else:
                return apprunner.list_auto_scaling_configurations(
                    LatestOnly=False
                ), False
        elif module.params['list_connections']:
            if apprunner.can_paginate('list_connections'):
                paginator = apprunner.get_paginator('list_connections')
                return paginator.paginate(), True
            else:
                return apprunner.list_connections(), False
        elif module.params['list_operations']:
            if apprunner.can_paginate('list_operations'):
                paginator = apprunner.get_paginator('list_operations')
                return paginator.paginate(
                    ServiceArn=module.params['arn']
                ), True
            else:
                return apprunner.list_operations(
                    ServiceArn=module.params['arn']
                ), False
        elif module.params['list_services']:
            if apprunner.can_paginate('list_services'):
                paginator = apprunner.get_paginator('list_services')
                return paginator.paginate(), True
            else:
                return apprunner.list_services(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws apprunner details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['service_arn']),
        list_auto_scaling_configurations=dict(required=False, type=bool),
        list_connections=dict(required=False, type=bool),
        list_operations=dict(required=False, type=bool),
        list_services=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_operations', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_auto_scaling_configurations',
                'list_connections',
                'list_operations',
                'list_services',
            )
        ],
    )

    _it, _paginate = _apprunner(module)
    if _it is not None:
        if module.params['list_auto_scaling_configurations']:
            module.exit_json(auto_scaling_configuration_summary=aws_response_list_parser(_paginate, _it, 'AutoScalingConfigurationSummaryList'))
        elif module.params['list_connections']:
            module.exit_json(connection_summary=aws_response_list_parser(_paginate, _it, 'ConnectionSummaryList'))
        elif module.params['list_operations']:
            module.exit_json(operation_summary=aws_response_list_parser(_paginate, _it, 'OperationSummaryList'))
        elif module.params['list_services']:
            module.exit_json(services=aws_response_list_parser(_paginate, _it, 'ServiceSummaryList'))


if __name__ == '__main__':
    main()
