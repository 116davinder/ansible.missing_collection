#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_worklink_info
short_description: Get Information about Amazon WorkLink.
description:
  - Get Information about Amazon WorkLink.
  - U(https://docs.aws.amazon.com/worklink/latest/api/API_Operations.html)
version_added: 0.1.0
options:
  arn:
    description:
      - arn of fleet.
    required: false
    type: str
    aliases: ['fleet_arn']
  list_devices:
    description:
      - do you want to get list of devices?
    required: false
    type: bool
  list_domains:
    description:
      - do you want to get domains for given I(arn)?
    required: false
    type: bool
  list_fleets:
    description:
      - do you want to get fleets for given I(arn)?
    required: false
    type: bool
  list_website_authorization_providers:
    description:
      - do you want to get website_authorization_providers for given I(arn)?
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
- name: "get list of devices"
  aws_worklink_info:
    list_devices: true
    arn: 'fleet_arn'

- name: "get domains"
  aws_worklink_info:
    list_domains: true
    arn: 'fleet_arn'

- name: "get fleets"
  aws_worklink_info:
    list_fleets: true
    arn: 'fleet_arn'

- name: "get website_authorization_providers"
  aws_worklink_info:
    list_website_authorization_providers: true
    arn: 'fleet_arn'
"""

RETURN = """
devices:
  description: list of devices.
  returned: when `list_devices` is defined and success.
  type: list
domains:
  description: list of domains.
  returned: when `list_domains` is defined and success.
  type: list
fleets:
  description: list of fleets.
  returned: when `list_fleets` is defined and success.
  type: list
website_authorization_providers:
  description: list of website_authorization_providers.
  returned: when `list_website_authorization_providers` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _worklink(client, module):
    try:
        if module.params['list_devices']:
            if client.can_paginate('list_devices'):
                paginator = client.get_paginator('list_devices')
                return paginator.paginate(
                    FleetArn=module.params['arn']
                ), True
            else:
                return client.list_devices(
                    FleetArn=module.params['arn']
                ), False
        elif module.params['list_domains']:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(
                    FleetArn=module.params['arn']
                ), True
            else:
                return client.list_domains(
                    FleetArn=module.params['arn']
                ), False
        elif module.params['list_fleets']:
            if client.can_paginate('list_fleets'):
                paginator = client.get_paginator('list_fleets')
                return paginator.paginate(), True
            else:
                return client.list_fleets(), False
        elif module.params['list_website_authorization_providers']:
            if client.can_paginate('list_website_authorization_providers'):
                paginator = client.get_paginator('list_website_authorization_providers')
                return paginator.paginate(
                    FleetArn=module.params['arn']
                ), True
            else:
                return client.list_website_authorization_providers(
                    FleetArn=module.params['arn']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon WorkLink details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['fleet_arn']),
        list_devices=dict(required=False, type=bool),
        list_domains=dict(required=False, type=bool),
        list_fleets=dict(required=False, type=bool),
        list_website_authorization_providers=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_devices', True, ['arn']),
            ('list_domains', True, ['arn']),
            ('list_website_authorization_providers', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_devices',
                'list_domains',
                'list_fleets',
                'list_website_authorization_providers',
            )
        ],
    )

    client = module.client('worklink', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _worklink(client, module)

    if module.params['list_devices']:
        module.exit_json(devices=aws_response_list_parser(paginate, it, 'Devices'))
    elif module.params['list_domains']:
        module.exit_json(domains=aws_response_list_parser(paginate, it, 'Domains'))
    elif module.params['list_fleets']:
        module.exit_json(fleets=aws_response_list_parser(paginate, it, 'FleetSummaryList'))
    elif module.params['list_website_authorization_providers']:
        module.exit_json(website_authorization_providers=aws_response_list_parser(paginate, it, 'WebsiteAuthorizationProviders'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
