#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ses_info
short_description: Get Information about Amazon Simple Email Service (SES).
description:
  - Get Information about Amazon Simple Email Service (SES).
  - U(https://docs.aws.amazon.com/ses/latest/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  identity_type:
    description:
      - type of identity.
    required: false
    type: str
  list_configuration_sets:
    description:
      - do you want to get list of configuration_sets?
    required: false
    type: bool
  list_custom_verification_email_templates:
    description:
      - do you want to get custom_verification_email_templates?
    required: false
    type: bool
  list_identities:
    description:
      - do you want to get list of identities for given I(identity_type)?
    required: false
    type: bool
  list_receipt_rule_sets:
    description:
      - do you want to get receipt_rule_sets?
    required: false
    type: bool
  list_templates:
    description:
      - do you want to get templates?
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
- name: "get list of configuration_sets"
  aws_ses_info:
    list_configuration_sets: true

- name: "get custom_verification_email_templates"
  aws_ses_info:
    list_custom_verification_email_templates: true

- name: "get list of identities"
  aws_ses_info:
    list_identities: true
    identity_type: 'EmailAddress'

- name: "get receipt_rule_sets"
  aws_ses_info:
    list_receipt_rule_sets: true

- name: "get templates"
  aws_ses_info:
    list_templates: true
"""

RETURN = """
configuration_sets:
  description: list of configuration_sets.
  returned: when `list_configuration_sets` is defined and success.
  type: list
custom_verification_email_templates:
  description: get of custom_verification_email_templates.
  returned: when `list_custom_verification_email_templates` is defined and success.
  type: list
identities:
  description: list of identities.
  returned: when `list_identities` is defined and success.
  type: list
receipt_rule_sets:
  description: list of receipt_rule_sets.
  returned: when `list_receipt_rule_sets` is defined and success.
  type: list
templates:
  description: list of templates.
  returned: when `list_templates` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _ses(client, module):
    try:
        if module.params['list_configuration_sets']:
            if client.can_paginate('list_configuration_sets'):
                paginator = client.get_paginator('list_configuration_sets')
                return paginator.paginate(), True
            else:
                return client.list_configuration_sets(), False
        elif module.params['list_custom_verification_email_templates']:
            if client.can_paginate('list_custom_verification_email_templates'):
                paginator = client.get_paginator('list_custom_verification_email_templates')
                return paginator.paginate(), True
            else:
                return client.list_custom_verification_email_templates(), False
        elif module.params['list_identities']:
            if client.can_paginate('list_identities'):
                paginator = client.get_paginator('list_identities')
                return paginator.paginate(
                    IdentityType=module.params['identity_type']
                ), True
            else:
                return client.list_identities(
                    IdentityType=module.params['identity_type']
                ), False
        elif module.params['list_receipt_rule_sets']:
            if client.can_paginate('list_receipt_rule_sets'):
                paginator = client.get_paginator('list_receipt_rule_sets')
                return paginator.paginate(), True
            else:
                return client.list_receipt_rule_sets(), False
        elif module.params['list_templates']:
            if client.can_paginate('list_templates'):
                paginator = client.get_paginator('list_templates')
                return paginator.paginate(), True
            else:
                return client.list_templates(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Simple Email Service (SES) details')


def main():
    argument_spec = dict(
        identity_type=dict(required=False, choices=['EmailAddress', 'Domain'], default='EmailAddress'),
        list_configuration_sets=dict(required=False, type=bool),
        list_custom_verification_email_templates=dict(required=False, type=bool),
        list_identities=dict(required=False, type=bool),
        list_receipt_rule_sets=dict(required=False, type=bool),
        list_templates=dict(required=False, type=bool),
        list_resolver_endpoint_ip_addresses=dict(required=False, type=bool),
        list_resolver_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_identities', True, ['identity_type']),
        ),
        mutually_exclusive=[
            (
                'list_configuration_sets',
                'list_custom_verification_email_templates',
                'list_identities',
                'list_receipt_rule_sets',
                'list_templates',
            )
        ],
    )

    client = module.client('ses', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ses(client, module)

    if module.params['list_configuration_sets']:
        module.exit_json(configuration_sets=aws_response_list_parser(paginate, it, 'ConfigurationSets'))
    elif module.params['list_custom_verification_email_templates']:
        module.exit_json(custom_verification_email_templates=aws_response_list_parser(paginate, it, 'CustomVerificationEmailTemplates'))
    elif module.params['list_identities']:
        module.exit_json(identities=aws_response_list_parser(paginate, it, 'Identities'))
    elif module.params['list_receipt_rule_sets']:
        module.exit_json(receipt_rule_sets=aws_response_list_parser(paginate, it, 'RuleSets'))
    elif module.params['list_templates']:
        module.exit_json(templates=aws_response_list_parser(paginate, it, 'TemplatesMetadata'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
