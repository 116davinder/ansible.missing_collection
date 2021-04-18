#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_waf_info
short_description: Get Information about AWS WAF Classic (V1).
description:
  - Get Information about AWS WAF Classic (V1).
  - U(https://docs.aws.amazon.com/waf/latest/APIReference/API_Operations_AWS_WAF.html)
version_added: 0.1.0
options:
  id:
    description:
      - id of the rule group.
    required: false
    type: str
    aliases: ['rule_group_id']
  list_activated_rules_in_rule_group:
    description:
      - do you want to get list of activated_rules_in_rule_group for given I(id)?
    required: false
    type: bool
  list_byte_match_sets:
    description:
      - do you want to get byte_match_sets?
    required: false
    type: bool
  list_geo_match_sets:
    description:
      - do you want to get list of geo_match_sets?
    required: false
    type: bool
  list_ip_sets:
    description:
      - do you want to get ip_sets?
    required: false
    type: bool
  list_logging_configurations:
    description:
      - do you want to get logging_configurations?
    required: false
    type: bool
  list_rate_based_rules:
    description:
      - do you want to get rate_based_rules?
    required: false
    type: bool
  list_regex_match_sets:
    description:
      - do you want to get regex_match_sets?
    required: false
    type: bool
  list_rule_groups:
    description:
      - do you want to get rule_groups?
    required: false
    type: bool
  list_rules:
    description:
      - do you want to get rules?
    required: false
    type: bool
  list_size_constraint_sets:
    description:
      - do you want to get size_constraint_sets?
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
- name: "get list of activated_rules_in_rule_group"
  aws_waf_info:
    list_activated_rules_in_rule_group: true
    id: 'rule_group_id'

- name: "get byte_match_sets"
  aws_waf_info:
    list_byte_match_sets: true

- name: "get list of geo_match_sets"
  aws_waf_info:
    list_geo_match_sets: true

- name: "get ip_sets"
  aws_waf_info:
    list_ip_sets: true

- name: "get logging_configurations"
  aws_waf_info:
    list_logging_configurations: true

- name: "get rate_based_rules"
  aws_waf_info:
    list_rate_based_rules: true

- name: "get regex_match_sets"
  aws_waf_info:
    list_regex_match_sets: true

- name: "get rule_groups"
  aws_waf_info:
    list_rule_groups: true

- name: "get rules"
  aws_waf_info:
    list_rules: true

- name: "get size_constraint_sets"
  aws_waf_info:
    list_size_constraint_sets: true
"""

RETURN = """
activated_rules_in_rule_group:
  description: list of activated_rules_in_rule_group.
  returned: when `list_activated_rules_in_rule_group` is defined and success.
  type: list
byte_match_sets:
  description: get of byte_match_sets.
  returned: when `list_byte_match_sets` is defined and success.
  type: list
geo_match_sets:
  description: list of geo_match_sets.
  returned: when `list_geo_match_sets` is defined and success.
  type: list
ip_sets:
  description: list of ip_sets.
  returned: when `list_ip_sets` is defined and success.
  type: list
logging_configurations:
  description: list of logging_configurations.
  returned: when `list_logging_configurations` is defined and success.
  type: list
rate_based_rules:
  description: list of rate_based_rules.
  returned: when `list_rate_based_rules` is defined and success.
  type: list
regex_match_sets:
  description: list of regex_match_sets.
  returned: when `list_regex_match_sets` is defined and success.
  type: list
rule_groups:
  description: list of rule_groups.
  returned: when `list_rule_groups` is defined and success.
  type: list
rules:
  description: list of rules.
  returned: when `list_rules` is defined and success.
  type: list
size_constraint_sets:
  description: list of size_constraint_sets.
  returned: when `list_size_constraint_sets` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _waf(client, module):
    try:
        if module.params['list_activated_rules_in_rule_group']:
            if client.can_paginate('list_activated_rules_in_rule_group'):
                paginator = client.get_paginator('list_activated_rules_in_rule_group')
                return paginator.paginate(
                    RuleGroupId=module.params['id']
                ), True
            else:
                return client.list_activated_rules_in_rule_group(
                    RuleGroupId=module.params['id']
                ), False
        elif module.params['list_byte_match_sets']:
            if client.can_paginate('list_byte_match_sets'):
                paginator = client.get_paginator('list_byte_match_sets')
                return paginator.paginate(), True
            else:
                return client.list_byte_match_sets(), False
        elif module.params['list_geo_match_sets']:
            if client.can_paginate('list_geo_match_sets'):
                paginator = client.get_paginator('list_geo_match_sets')
                return paginator.paginate(), True
            else:
                return client.list_geo_match_sets(), False
        elif module.params['list_ip_sets']:
            if client.can_paginate('list_ip_sets'):
                paginator = client.get_paginator('list_ip_sets')
                return paginator.paginate(), True
            else:
                return client.list_ip_sets(), False
        elif module.params['list_logging_configurations']:
            if client.can_paginate('list_logging_configurations'):
                paginator = client.get_paginator('list_logging_configurations')
                return paginator.paginate(), True
            else:
                return client.list_logging_configurations(), False
        elif module.params['list_rate_based_rules']:
            if client.can_paginate('list_rate_based_rules'):
                paginator = client.get_paginator('list_rate_based_rules')
                return paginator.paginate(), True
            else:
                return client.list_rate_based_rules(), False
        elif module.params['list_regex_match_sets']:
            if client.can_paginate('list_regex_match_sets'):
                paginator = client.get_paginator('list_regex_match_sets')
                return paginator.paginate(), True
            else:
                return client.list_regex_match_sets(), False
        elif module.params['list_rule_groups']:
            if client.can_paginate('list_rule_groups'):
                paginator = client.get_paginator('list_rule_groups')
                return paginator.paginate(), True
            else:
                return client.list_rule_groups(), False
        elif module.params['list_rules']:
            if client.can_paginate('list_rules'):
                paginator = client.get_paginator('list_rules')
                return paginator.paginate(), True
            else:
                return client.list_rules(), False
        elif module.params['list_size_constraint_sets']:
            if client.can_paginate('list_size_constraint_sets'):
                paginator = client.get_paginator('list_size_constraint_sets')
                return paginator.paginate(), True
            else:
                return client.list_size_constraint_sets(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS WAF Classic (V1) details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['rule_group_id']),
        list_activated_rules_in_rule_group=dict(required=False, type=bool),
        list_byte_match_sets=dict(required=False, type=bool),
        list_geo_match_sets=dict(required=False, type=bool),
        list_ip_sets=dict(required=False, type=bool),
        list_logging_configurations=dict(required=False, type=bool),
        list_rate_based_rules=dict(required=False, type=bool),
        list_regex_match_sets=dict(required=False, type=bool),
        list_rule_groups=dict(required=False, type=bool),
        list_rules=dict(required=False, type=bool),
        list_size_constraint_sets=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_activated_rules_in_rule_group', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_activated_rules_in_rule_group',
                'list_byte_match_sets',
                'list_geo_match_sets',
                'list_ip_sets',
                'list_logging_configurations',
                'list_rate_based_rules',
                'list_regex_match_sets',
                'list_rule_groups',
                'list_rules',
                'list_size_constraint_sets',
            )
        ],
    )

    client = module.client('waf', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _waf(client, module)

    if module.params['list_activated_rules_in_rule_group']:
        module.exit_json(activated_rules_in_rule_group=aws_response_list_parser(paginate, it, 'ActivatedRules'))
    elif module.params['list_byte_match_sets']:
        module.exit_json(byte_match_sets=aws_response_list_parser(paginate, it, 'ByteMatchSets'))
    elif module.params['list_geo_match_sets']:
        module.exit_json(geo_match_sets=aws_response_list_parser(paginate, it, 'GeoMatchSets'))
    elif module.params['list_ip_sets']:
        module.exit_json(ip_sets=aws_response_list_parser(paginate, it, 'IPSets'))
    elif module.params['list_logging_configurations']:
        module.exit_json(logging_configurations=aws_response_list_parser(paginate, it, 'LoggingConfigurations'))
    elif module.params['list_rate_based_rules']:
        module.exit_json(rate_based_rules=aws_response_list_parser(paginate, it, 'Rules'))
    elif module.params['list_regex_match_sets']:
        module.exit_json(regex_match_sets=aws_response_list_parser(paginate, it, 'RegexMatchSets'))
    elif module.params['list_rule_groups']:
        module.exit_json(rule_groups=aws_response_list_parser(paginate, it, 'RuleGroups'))
    elif module.params['list_rules']:
        module.exit_json(rules=aws_response_list_parser(paginate, it, 'Rules'))
    elif module.params['list_size_constraint_sets']:
        module.exit_json(size_constraint_sets=aws_response_list_parser(paginate, it, 'SizeConstraintSets'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
