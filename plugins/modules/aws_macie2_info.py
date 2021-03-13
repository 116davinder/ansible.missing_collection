#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_macie2_info
short_description: Get Information about Amazon Macie 2.
description:
  - Get Information about Amazon Macie 2.
  - U(https://docs.aws.amazon.com/macie/latest/APIReference/resources.html)
version_added: 0.0.7
options:
  job_status:
    description:
      - filter out classifications jobs based on status.
    required: false
    type: str
    choices: ['RUNNING', 'PAUSED', 'CANCELLED', 'COMPLETE', 'IDLE', 'USER_PAUSED']
    default: 'RUNNING'
  list_classification_jobs:
    description:
      - do you want to get list of classification_jobs for given I(job_status)?
    required: false
    type: bool
  list_custom_data_identifiers:
    description:
      - do you want to get list of custom_data_identifiers?
    required: false
    type: bool
  list_findings_filters:
    description:
      - do you want to get list of findings_filters?
    required: false
    type: bool
  list_invitations:
    description:
      - do you want to get list of invitations?
    required: false
    type: bool
  list_members:
    description:
      - do you want to get list of members?
    required: false
    type: bool
  list_organization_admin_accounts:
    description:
      - do you want to get list of organization_admin_accounts?
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
- name: "get list of classification_jobs"
  aws_macie2_info:
    list_classification_jobs: true
    job_status: 'RUNNING'

- name: "get list of custom_data_identifiers"
  aws_macie2_info:
    list_custom_data_identifiers: true

- name: "get list of findings_filters"
  aws_macie2_info:
    list_findings_filters: true

- name: "get list of Invitations"
  aws_macie2_info:
    list_invitations: true

- name: "get list of members"
  aws_macie2_info:
    list_members: true

- name: "get list of organization_admin_accounts"
  aws_macie2_info:
    list_organization_admin_accounts: true
"""

RETURN = """
classification_jobs:
  description: list of classification_jobs.
  returned: when `list_classification_jobs` is defined and success.
  type: list
custom_data_identifiers:
  description: list of custom_data_identifiers.
  returned: when `list_custom_data_identifiers` is defined and success.
  type: list
findings_filters:
  description: list of findings_filters.
  returned: when `list_findings_filters` is defined and success.
  type: list
invitations:
  description: list of invitations.
  returned: when `list_invitations` is defined and success.
  type: list
members:
  description: list of members.
  returned: when `list_members` is defined and success.
  type: list
organization_admin_accounts:
  description: list of organization_admin_accounts.
  returned: when `list_organization_admin_accounts` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _macie2(client, module):
    try:
        if module.params['list_classification_jobs']:
            if client.can_paginate('list_classification_jobs'):
                paginator = client.get_paginator('list_classification_jobs')
                return paginator.paginate(
                    filterCriteria={
                        'includes': [
                            {
                                'comparator': 'EQ',
                                'key': 'jobStatus',
                                'values': [module.params['job_status']]
                            },
                        ]
                    }
                ), True
            else:
                return client.list_classification_jobs(
                    filterCriteria={
                        'includes': [
                            {
                                'comparator': 'EQ',
                                'key': 'jobStatus',
                                'values': [module.params['job_status']]
                            },
                        ]
                    }
                ), False
        elif module.params['list_custom_data_identifiers']:
            if client.can_paginate('list_custom_data_identifiers'):
                paginator = client.get_paginator('list_custom_data_identifiers')
                return paginator.paginate(), True
            else:
                return client.list_custom_data_identifiers(), False
        elif module.params['list_findings_filters']:
            if client.can_paginate('list_findings_filters'):
                paginator = client.get_paginator('list_findings_filters')
                return paginator.paginate(), True
            else:
                return client.list_findings_filters(), False
        elif module.params['list_invitations']:
            if client.can_paginate('list_invitations'):
                paginator = client.get_paginator('list_invitations')
                return paginator.paginate(), True
            else:
                return client.list_invitations(), False
        elif module.params['list_members']:
            if client.can_paginate('list_members'):
                paginator = client.get_paginator('list_members')
                return paginator.paginate(), True
            else:
                return client.list_members(), False
        elif module.params['list_organization_admin_accounts']:
            if client.can_paginate('list_organization_admin_accounts'):
                paginator = client.get_paginator('list_organization_admin_accounts')
                return paginator.paginate(), True
            else:
                return client.list_organization_admin_accounts(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Macie 2 details')


def main():
    argument_spec = dict(
        job_status=dict(
            required=False,
            choices=['RUNNING', 'PAUSED', 'CANCELLED', 'COMPLETE', 'IDLE', 'USER_PAUSED'],
            default='RUNNING'
        ),
        list_classification_jobs=dict(required=False, type=bool),
        list_custom_data_identifiers=dict(required=False, type=bool),
        list_findings_filters=dict(required=False, type=bool),
        list_invitations=dict(required=False, type=bool),
        list_members=dict(required=False, type=bool),
        list_organization_admin_accounts=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_classification_jobs',
                'list_custom_data_identifiers',
                'list_findings_filters',
                'list_invitations',
                'list_members',
                'list_organization_admin_accounts',
            )
        ],
    )

    client = module.client('macie2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _macie2(client, module)

    if module.params['list_classification_jobs']:
        module.exit_json(classification_jobs=aws_response_list_parser(paginate, it, 'items'))
    elif module.params['list_custom_data_identifiers']:
        module.exit_json(custom_data_identifiers=aws_response_list_parser(paginate, it, 'items'))
    elif module.params['list_findings_filters']:
        module.exit_json(findings_filters=aws_response_list_parser(paginate, it, 'findingsFilterListItems'))
    elif module.params['list_invitations']:
        module.exit_json(invitations=aws_response_list_parser(paginate, it, 'invitations'))
    elif module.params['list_members']:
        module.exit_json(members=aws_response_list_parser(paginate, it, 'members'))
    elif module.params['list_organization_admin_accounts']:
        module.exit_json(organization_admin_accounts=aws_response_list_parser(paginate, it, 'adminAccounts'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
