#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_network_firewall_info
short_description: Get Information about AWS Network Firewall.
description:
  - Get Information about AWS Network Firewall.
  - U(https://docs.aws.amazon.com/network-firewall/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  list_firewall_policies:
    description:
      - do you want to get list of firewall_policies?
    required: false
    type: bool
  list_firewalls:
    description:
      - do you want to get firewalls?
    required: false
    type: bool
  list_rule_groups:
    description:
      - do you want to get list of rule_groups?
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
- name: "get list of firewall_policies"
  aws_network_firewall_info:
    list_firewall_policies: true

- name: "get firewalls"
  aws_network_firewall_info:
    list_firewalls: true

- name: "get list of rule_groups"
  aws_network_firewall_info:
    list_rule_groups: true
"""

RETURN = """
firewall_policies:
  description: list of firewall_policies.
  returned: when `list_firewall_policies` is defined and success.
  type: list
firewalls:
  description: list of firewalls.
  returned: when `list_firewalls` is defined and success.
  type: list
rule_groups:
  description: list of rule_groups.
  returned: when `list_rule_groups` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _network_firewall(client, module):
    try:
        if module.params['list_firewall_policies']:
            if client.can_paginate('list_firewall_policies'):
                paginator = client.get_paginator('list_firewall_policies')
                return paginator.paginate(), True
            else:
                return client.list_firewall_policies(), False
        elif module.params['list_firewalls']:
            if client.can_paginate('list_firewalls'):
                paginator = client.get_paginator('list_firewalls')
                return paginator.paginate(), True
            else:
                return client.list_firewalls(), False
        elif module.params['list_rule_groups']:
            if client.can_paginate('list_rule_groups'):
                paginator = client.get_paginator('list_rule_groups')
                return paginator.paginate(), True
            else:
                return client.list_rule_groups(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Network Firewall details')


def main():
    argument_spec = dict(
        list_firewall_policies=dict(required=False, type=bool),
        list_firewalls=dict(required=False, type=bool),
        list_rule_groups=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_firewall_policies',
                'list_firewalls',
                'list_rule_groups',
            )
        ],
    )

    client = module.client('network-firewall', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _network_firewall(client, module)

    if module.params['list_firewall_policies']:
        module.exit_json(firewall_policies=aws_response_list_parser(paginate, it, 'FirewallPolicies'))
    elif module.params['list_firewalls']:
        module.exit_json(firewalls=aws_response_list_parser(paginate, it, 'Firewalls'))
    elif module.params['list_rule_groups']:
        module.exit_json(rule_groups=aws_response_list_parser(paginate, it, 'RuleGroups'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
