#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_guardduty_info
short_description: Get Information about Amazon GuardDuty.
description:
  - Get Information about Amazon GuardDuty.
  - U(https://docs.aws.amazon.com/guardduty/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of detector.
    required: false
    type: str
  list_detectors:
    description:
      - do you want to get list of detectors?
    required: false
    type: bool
  list_filters:
    description:
      - do you want to get list of filters for given I(id)?
    required: false
    type: bool
  list_findings:
    description:
      - do you want to get list of findings for given I(id)?
    required: false
    type: bool
  list_invitations:
    description:
      - do you want to get list of invitation?
    required: false
    type: bool
  list_ip_sets:
    description:
      - do you want to get list of ip_sets for given I(id)?
    required: false
    type: bool
  list_members:
    description:
      - do you want to get list of members for given I(id)?
    required: false
    type: bool
  list_organization_admin_accounts:
    description:
      - do you want to get list of organization admin accounts?
    required: false
    type: bool
  list_publishing_destinations:
    description:
      - do you want to get list of publishing destinations for given I(id)?
    required: false
    type: bool
  list_threat_intel_sets:
    description:
      - do you want to get list of threat intel sets for given I(id)?
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
- name: "get list of detectors"
  aws_guardduty_info:
    list_detectors: true

- name: "get list of filters"
  aws_guardduty_info:
    list_filters: true
    id: 'test'

- name: "get list of findings"
  aws_guardduty_info:
    list_findings: true
    id: 'test'

- name: "get list of invitations"
  aws_guardduty_info:
    list_invitations: true

- name: "get list of ip_sets"
  aws_guardduty_info:
    list_ip_sets: true
    id: 'test'

- name: "get list of members"
  aws_guardduty_info:
    list_members: true
    id: 'test'

- name: "get list of organization admin accounts"
  aws_guardduty_info:
    list_organization_admin_accounts: true

- name: "get list of publishing destinations"
  aws_guardduty_info:
    list_publishing_destinations: true
    id: 'test'

- name: "get list of threat intel sets"
  aws_guardduty_info:
    list_threat_intel_sets: true
    id: 'test'
"""

RETURN = """
detectors:
  description: list of detectors.
  returned: when `list_detectors` is defined and success.
  type: list
filters:
  description: list of filters.
  returned: when `list_filters` is defined and success.
  type: list
findings:
  description: list of findings.
  returned: when `list_findings` is defined and success.
  type: list
invitations:
  description: list of invitations.
  returned: when `list_invitations` is defined and success.
  type: list
ip_sets:
  description: list of ip sets.
  returned: when `list_ip_sets` is defined and success.
  type: list
members:
  description: list of members.
  returned: when `list_members` is defined and success.
  type: list
organization_admin_accounts:
  description: list of organization admin accounts.
  returned: when `list_organization_admin_accounts` is defined and success.
  type: list
publishing_destinations:
  description: list of publishing destinations.
  returned: when `list_publishing_destinations` is defined and success.
  type: list
threat_intel_sets:
  description: list of threat intel sets.
  returned: when `list_threat_intel_sets` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _guardduty(client, module):
    try:
        if module.params['list_detectors']:
            if client.can_paginate('list_detectors'):
                paginator = client.get_paginator('list_detectors')
                return paginator.paginate(), True
            else:
                return client.list_detectors(), False
        elif module.params['list_filters']:
            if client.can_paginate('list_filters'):
                paginator = client.get_paginator('list_filters')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_filters(
                    DetectorId=module.params['id']
                ), False
        elif module.params['list_findings']:
            if client.can_paginate('list_findings'):
                paginator = client.get_paginator('list_findings')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_findings(
                    DetectorId=module.params['id']
                ), False
        elif module.params['list_ip_sets']:
            if client.can_paginate('list_ip_sets'):
                paginator = client.get_paginator('list_ip_sets')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_ip_sets(
                    DetectorId=module.params['id']
                ), False
        elif module.params['list_members']:
            if client.can_paginate('list_members'):
                paginator = client.get_paginator('list_members')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_members(
                    DetectorId=module.params['id']
                ), False
        elif module.params['list_organization_admin_accounts']:
            if client.can_paginate('list_organization_admin_accounts'):
                paginator = client.get_paginator('list_organization_admin_accounts')
                return paginator.paginate(), True
            else:
                return client.list_organization_admin_accounts(), False
        elif module.params['list_publishing_destinations']:
            if client.can_paginate('list_publishing_destinations'):
                paginator = client.get_paginator('list_publishing_destinations')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_publishing_destinations(
                    DetectorId=module.params['id']
                ), False
        elif module.params['list_threat_intel_sets']:
            if client.can_paginate('list_threat_intel_sets'):
                paginator = client.get_paginator('list_threat_intel_sets')
                return paginator.paginate(
                    DetectorId=module.params['id']
                ), True
            else:
                return client.list_threat_intel_sets(
                    DetectorId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Guard Duty details')


def main():
    argument_spec = dict(
        id=dict(required=False),
        list_detectors=dict(required=False, type=bool),
        list_filters=dict(required=False, type=bool),
        list_findings=dict(required=False, type=bool),
        list_invitations=dict(required=False, type=bool),
        list_ip_sets=dict(required=False, type=bool),
        list_members=dict(required=False, type=bool),
        list_organization_admin_accounts=dict(required=False, type=bool),
        list_publishing_destinations=dict(required=False, type=bool),
        list_threat_intel_sets=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_filters', True, ['id']),
            ('list_findings', True, ['id']),
            ('list_ip_sets', True, ['id']),
            ('list_members', True, ['id']),
            ('list_publishing_destinations', True, ['id']),
            ('list_threat_intel_sets', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_detectors',
                'list_filters',
                'list_findings',
                'list_invitations',
                'list_ip_sets',
                'list_ip_sets',
                'list_members',
                'list_organization_admin_accounts',
                'list_publishing_destinations',
                'list_threat_intel_sets',
            )
        ],
    )

    client = module.client('guardduty', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _guardduty(client, module)

    if module.params['list_detectors']:
        module.exit_json(detectors=aws_response_list_parser(paginate, it, 'DetectorIds'))
    elif module.params['list_filters']:
        module.exit_json(filters=aws_response_list_parser(paginate, it, 'FilterNames'))
    elif module.params['list_findings']:
        module.exit_json(findings=aws_response_list_parser(paginate, it, 'FindingIds'))
    elif module.params['list_invitations']:
        module.exit_json(invitations=aws_response_list_parser(paginate, it, 'Invitations'))
    elif module.params['list_ip_sets']:
        module.exit_json(ip_sets=aws_response_list_parser(paginate, it, 'IpSetIds'))
    elif module.params['list_members']:
        module.exit_json(members=aws_response_list_parser(paginate, it, 'Members'))
    elif module.params['list_organization_admin_accounts']:
        module.exit_json(organization_admin_accounts=aws_response_list_parser(paginate, it, 'AdminAccounts'))
    elif module.params['list_publishing_destinations']:
        module.exit_json(publishing_destinations=aws_response_list_parser(paginate, it, 'Destinations'))
    elif module.params['list_threat_intel_sets']:
        module.exit_json(threat_intel_sets=aws_response_list_parser(paginate, it, 'ThreatIntelSetIds'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
