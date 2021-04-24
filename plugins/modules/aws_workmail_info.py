#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_workmail_info
short_description: Get Information about Amazon WorkMail.
description:
  - Get Information about Amazon WorkMail.
  - U(https://docs.aws.amazon.com/workmail/latest/APIReference/API_Operations_Amazon_WorkMail.html)
version_added: 0.1.0
options:
  id:
    description:
      - id of Organization.
    required: false
    type: str
    aliases: ['organization_id']
  list_access_control_rules:
    description:
      - do you want to get list of access_control_rules for given I(id)?
    required: false
    type: bool
  list_groups:
    description:
      - do you want to get groups for given I(id)?
    required: false
    type: bool
  list_mailbox_export_jobs:
    description:
      - do you want to get mailbox_export_jobs for given I(id)?
    required: false
    type: bool
  list_mobile_device_access_rules:
    description:
      - do you want to get mobile_device_access_rules for given I(id)?
    required: false
    type: bool
  list_organizations:
    description:
      - do you want to get organizations?
    required: false
    type: bool
  list_resources:
    description:
      - do you want to get resources for given I(id)?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get users for given I(id)?
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
- name: "get list of access_control_rules"
  aws_workmail_info:
    list_access_control_rules: true
    id: 'organization_id'

- name: "get groups"
  aws_workmail_info:
    list_groups: true
    id: 'organization_id'

- name: "get mailbox_export_jobs"
  aws_workmail_info:
    list_mailbox_export_jobs: true
    id: 'organization_id'

- name: "get mobile_device_access_rules"
  aws_workmail_info:
    list_mobile_device_access_rules: true
    id: 'organization_id'

- name: "get organizations"
  aws_workmail_info:
    list_organizations: true

- name: "get resources"
  aws_workmail_info:
    list_resources: true
    id: 'organization_id'

- name: "get users"
  aws_workmail_info:
    list_users: true
    id: 'organization_id'
"""

RETURN = """
access_control_rules:
  description: list of access_control_rules.
  returned: when `list_access_control_rules` is defined and success.
  type: list
groups:
  description: list of groups.
  returned: when `list_groups` is defined and success.
  type: list
mailbox_export_jobs:
  description: list of mailbox_export_jobs.
  returned: when `list_mailbox_export_jobs` is defined and success.
  type: list
mobile_device_access_rules:
  description: list of mobile_device_access_rules.
  returned: when `list_mobile_device_access_rules` is defined and success.
  type: list
organizations:
  description: list of organizations.
  returned: when `list_organizations` is defined and success.
  type: list
resources:
  description: list of resources.
  returned: when `list_resources` is defined and success.
  type: list
users:
  description: list of users.
  returned: when `list_users` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _workmail(client, module):
    try:
        if module.params['list_access_control_rules']:
            if client.can_paginate('list_access_control_rules'):
                paginator = client.get_paginator('list_access_control_rules')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_access_control_rules(
                    OrganizationId=module.params['id']
                ), False
        elif module.params['list_groups']:
            if client.can_paginate('list_groups'):
                paginator = client.get_paginator('list_groups')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_groups(
                    OrganizationId=module.params['id']
                ), False
        elif module.params['list_mailbox_export_jobs']:
            if client.can_paginate('list_mailbox_export_jobs'):
                paginator = client.get_paginator('list_mailbox_export_jobs')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_mailbox_export_jobs(
                    OrganizationId=module.params['id']
                ), False
        elif module.params['list_mobile_device_access_rules']:
            if client.can_paginate('list_mobile_device_access_rules'):
                paginator = client.get_paginator('list_mobile_device_access_rules')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_mobile_device_access_rules(
                    OrganizationId=module.params['id']
                ), False
        elif module.params['list_organizations']:
            if client.can_paginate('list_organizations'):
                paginator = client.get_paginator('list_organizations')
                return paginator.paginate(), True
            else:
                return client.list_organizations(), False
        elif module.params['list_resources']:
            if client.can_paginate('list_resources'):
                paginator = client.get_paginator('list_resources')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_resources(
                    OrganizationId=module.params['id']
                ), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    OrganizationId=module.params['id']
                ), True
            else:
                return client.list_users(
                    OrganizationId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon WorkMail details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['organization_id']),
        list_access_control_rules=dict(required=False, type=bool),
        list_groups=dict(required=False, type=bool),
        list_mailbox_export_jobs=dict(required=False, type=bool),
        list_mobile_device_access_rules=dict(required=False, type=bool),
        list_organizations=dict(required=False, type=bool),
        list_resources=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_access_control_rules', True, ['id']),
            ('list_groups', True, ['id']),
            ('list_mailbox_export_jobs', True, ['id']),
            ('list_mobile_device_access_rules', True, ['id']),
            ('list_resources', True, ['id']),
            ('list_users', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_access_control_rules',
                'list_groups',
                'list_mailbox_export_jobs',
                'list_mobile_device_access_rules',
                'list_organizations',
                'list_resources',
                'list_users',
            )
        ],
    )

    client = module.client('workmail', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _workmail(client, module)

    if module.params['list_access_control_rules']:
        module.exit_json(access_control_rules=aws_response_list_parser(paginate, it, 'Rules'))
    elif module.params['list_groups']:
        module.exit_json(groups=aws_response_list_parser(paginate, it, 'Groups'))
    elif module.params['list_mailbox_export_jobs']:
        module.exit_json(mailbox_export_jobs=aws_response_list_parser(paginate, it, 'Jobs'))
    elif module.params['list_mobile_device_access_rules']:
        module.exit_json(mobile_device_access_rules=aws_response_list_parser(paginate, it, 'Rules'))
    elif module.params['list_organizations']:
        module.exit_json(organizations=aws_response_list_parser(paginate, it, 'OrganizationSummaries'))
    elif module.params['list_resources']:
        module.exit_json(resources=aws_response_list_parser(paginate, it, 'Resources'))
    elif module.params['list_users']:
        module.exit_json(users=aws_response_list_parser(paginate, it, 'Users'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
