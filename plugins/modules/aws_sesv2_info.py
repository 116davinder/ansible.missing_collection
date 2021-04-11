#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sesv2_info
short_description: Get Information about Amazon Simple Email Service (SES V2).
description:
  - Get Information about Amazon Simple Email Service (SES V2).
  - U(https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_Operations.html)
version_added: 0.0.9
options:
  name:
    description:
      - name of the contact list.
    required: false
    type: str
    aliases: ['contact_list_name']
  list_configuration_sets:
    description:
      - do you want to get list of configuration_sets?
    required: false
    type: bool
  list_contact_lists:
    description:
      - do you want to get contact_lists?
    required: false
    type: bool
  list_contacts:
    description:
      - do you want to get list of contacts for given I(name)
    required: false
    type: bool
  list_custom_verification_email_templates:
    description:
      - do you want to get custom_verification_email_templates?
    required: false
    type: bool
  list_dedicated_ip_pools:
    description:
      - do you want to get dedicated_ip_pools?
    required: false
    type: bool
  list_deliverability_test_reports:
    description:
      - do you want to get deliverability_test_reports?
    required: false
    type: bool
  list_email_identities:
    description:
      - do you want to get email_identities?
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
  aws_sesv2_info:
    list_configuration_sets: true

- name: "get contact_lists"
  aws_sesv2_info:
    list_contact_lists: true

- name: "get list of contacts"
  aws_sesv2_info:
    list_contacts: true
    name: 'contact_list_name'

- name: "get custom_verification_email_templates"
  aws_sesv2_info:
    list_custom_verification_email_templates: true

- name: "get dedicated_ip_pools"
  aws_sesv2_info:
    list_dedicated_ip_pools: true

- name: "get deliverability_test_reports"
  aws_sesv2_info:
    list_deliverability_test_reports: true

- name: "get email_identities"
  aws_sesv2_info:
    list_email_identities: true
"""

RETURN = """
configuration_sets:
  description: list of configuration_sets.
  returned: when `list_configuration_sets` is defined and success.
  type: list
contact_lists:
  description: list of contact_lists.
  returned: when `list_contact_lists` is defined and success.
  type: list
contacts:
  description: list of contacts.
  returned: when `list_contacts` is defined and success.
  type: list
custom_verification_email_templates:
  description: list of custom_verification_email_templates.
  returned: when `list_custom_verification_email_templates` is defined and success.
  type: list
dedicated_ip_pools:
  description: list of dedicated_ip_pools.
  returned: when `list_dedicated_ip_pools` is defined and success.
  type: list
deliverability_test_reports:
  description: list of deliverability_test_reports.
  returned: when `list_deliverability_test_reports` is defined and success.
  type: list
email_identities:
  description: list of email_identities.
  returned: when `list_email_identities` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sesv2(client, module):
    try:
        if module.params['list_configuration_sets']:
            if client.can_paginate('list_configuration_sets'):
                paginator = client.get_paginator('list_configuration_sets')
                return paginator.paginate(), True
            else:
                return client.list_configuration_sets(), False
        elif module.params['list_contact_lists']:
            if client.can_paginate('list_contact_lists'):
                paginator = client.get_paginator('list_contact_lists')
                return paginator.paginate(), True
            else:
                return client.list_contact_lists(), False
        elif module.params['list_contacts']:
            if client.can_paginate('list_contacts'):
                paginator = client.get_paginator('list_contacts')
                return paginator.paginate(
                    ContactListName=module.params['name']
                ), True
            else:
                return client.list_contacts(
                    ContactListName=module.params['name']
                ), False
        elif module.params['list_custom_verification_email_templates']:
            if client.can_paginate('list_custom_verification_email_templates'):
                paginator = client.get_paginator('list_custom_verification_email_templates')
                return paginator.paginate(), True
            else:
                return client.list_custom_verification_email_templates(), False
        elif module.params['list_dedicated_ip_pools']:
            if client.can_paginate('list_dedicated_ip_pools'):
                paginator = client.get_paginator('list_dedicated_ip_pools')
                return paginator.paginate(), True
            else:
                return client.list_dedicated_ip_pools(), False
        elif module.params['list_deliverability_test_reports']:
            if client.can_paginate('list_deliverability_test_reports'):
                paginator = client.get_paginator('list_deliverability_test_reports')
                return paginator.paginate(), True
            else:
                return client.list_deliverability_test_reports(), False
        elif module.params['list_email_identities']:
            if client.can_paginate('list_email_identities'):
                paginator = client.get_paginator('list_email_identities')
                return paginator.paginate(), True
            else:
                return client.list_email_identities(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Simple Email Service (SES V2) details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['contact_list_name']),
        list_configuration_sets=dict(required=False, type=bool),
        list_contact_lists=dict(required=False, type=bool),
        list_contacts=dict(required=False, type=bool),
        list_custom_verification_email_templates=dict(required=False, type=bool),
        list_dedicated_ip_pools=dict(required=False, type=bool),
        list_deliverability_test_reports=dict(required=False, type=bool),
        list_email_identities=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_contacts', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_configuration_sets',
                'list_contact_lists',
                'list_contacts',
                'list_custom_verification_email_templates',
                'list_dedicated_ip_pools',
                'list_deliverability_test_reports',
                'list_email_identities',
            )
        ],
    )

    client = module.client('sesv2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sesv2(client, module)

    if module.params['list_configuration_sets']:
        module.exit_json(configuration_sets=aws_response_list_parser(paginate, it, 'ConfigurationSets'))
    elif module.params['list_contact_lists']:
        module.exit_json(contact_lists=aws_response_list_parser(paginate, it, 'ContactLists'))
    elif module.params['list_contacts']:
        module.exit_json(contacts=aws_response_list_parser(paginate, it, 'Contacts'))
    elif module.params['list_custom_verification_email_templates']:
        module.exit_json(custom_verification_email_templates=aws_response_list_parser(paginate, it, 'CustomVerificationEmailTemplates'))
    elif module.params['list_dedicated_ip_pools']:
        module.exit_json(dedicated_ip_pools=aws_response_list_parser(paginate, it, 'DedicatedIpPools'))
    elif module.params['list_deliverability_test_reports']:
        module.exit_json(deliverability_test_reports=aws_response_list_parser(paginate, it, 'DeliverabilityTestReports'))
    elif module.params['list_email_identities']:
        module.exit_json(email_identities=aws_response_list_parser(paginate, it, 'EmailIdentities'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
