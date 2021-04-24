#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_wafv2_info
short_description: Get Information about AWS WAFV2.
description:
  - Get Information about AWS WAFV2.
  - U(https://docs.aws.amazon.com/waf/latest/APIReference/API_Operations_AWS_WAFV2.html)
version_added: 0.1.0
options:
  scope:
    description:
      - scope of waf.
    required: false
    type: str
    choices: ['CLOUDFRONT', 'REGIONAL']
    default: 'CLOUDFRONT'
  list_available_managed_rule_groups:
    description:
      - do you want to get list of available_managed_rule_groups for given I(scope)?
    required: false
    type: bool
  list_ip_sets:
    description:
      - do you want to get ip_sets for given I(scope)?
    required: false
    type: bool
  list_logging_configurations:
    description:
      - do you want to get logging_configurations for given I(scope)?
    required: false
    type: bool
  list_regex_pattern_sets:
    description:
      - do you want to get regex_pattern_sets for given I(scope)?
    required: false
    type: bool
  list_rule_groups:
    description:
      - do you want to get rule_groups for given I(scope)?
    required: false
    type: bool
  list_web_acls:
    description:
      - do you want to get web_acls for given I(scope)?
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
- name: "get list of available_managed_rule_groups"
  aws_wafv2_info:
    list_available_managed_rule_groups: true
    scope: 'CLOUDFRONT'

- name: "get ip_sets"
  aws_wafv2_info:
    list_ip_sets: true
    scope: 'CLOUDFRONT'

- name: "get logging_configurations"
  aws_wafv2_info:
    list_logging_configurations: true
    scope: 'CLOUDFRONT'

- name: "get regex_pattern_sets"
  aws_wafv2_info:
    list_regex_pattern_sets: true
    scope: 'CLOUDFRONT'

- name: "get rule_groups"
  aws_wafv2_info:
    list_rule_groups: true
    scope: 'CLOUDFRONT'

- name: "get web_acls"
  aws_wafv2_info:
    list_web_acls: true
    scope: 'CLOUDFRONT'
"""

RETURN = """
available_managed_rule_groups:
  description: list of available_managed_rule_groups.
  returned: when `list_available_managed_rule_groups` is defined and success.
  type: list
ip_sets:
  description: list of ip_sets.
  returned: when `list_ip_sets` is defined and success.
  type: list
logging_configurations:
  description: list of logging_configurations.
  returned: when `list_logging_configurations` is defined and success.
  type: list
regex_pattern_sets:
  description: list of regex_pattern_sets.
  returned: when `list_regex_pattern_sets` is defined and success.
  type: list
rule_groups:
  description: list of rule_groups.
  returned: when `list_rule_groups` is defined and success.
  type: list
web_acls:
  description: list of web_acls.
  returned: when `list_web_acls` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _wafv2(client, module):
    try:
        if module.params['list_available_managed_rule_groups']:
            if client.can_paginate('list_available_managed_rule_groups'):
                paginator = client.get_paginator('list_available_managed_rule_groups')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_available_managed_rule_groups(
                    Scope=module.params['scope']
                ), False
        elif module.params['list_ip_sets']:
            if client.can_paginate('list_ip_sets'):
                paginator = client.get_paginator('list_ip_sets')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_ip_sets(
                    Scope=module.params['scope']
                ), False
        elif module.params['list_logging_configurations']:
            if client.can_paginate('list_logging_configurations'):
                paginator = client.get_paginator('list_logging_configurations')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_logging_configurations(
                    Scope=module.params['scope']
                ), False
        elif module.params['list_regex_pattern_sets']:
            if client.can_paginate('list_regex_pattern_sets'):
                paginator = client.get_paginator('list_regex_pattern_sets')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_regex_pattern_sets(
                    Scope=module.params['scope']
                ), False
        elif module.params['list_rule_groups']:
            if client.can_paginate('list_rule_groups'):
                paginator = client.get_paginator('list_rule_groups')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_rule_groups(
                    Scope=module.params['scope']
                ), False
        elif module.params['list_web_acls']:
            if client.can_paginate('list_web_acls'):
                paginator = client.get_paginator('list_web_acls')
                return paginator.paginate(
                    Scope=module.params['scope']
                ), True
            else:
                return client.list_web_acls(
                    Scope=module.params['scope']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS WAFV2 details')


def main():
    argument_spec = dict(
        scope=dict(required=False, choices=['CLOUDFRONT', 'REGIONAL'], default='CLOUDFRONT'),
        list_available_managed_rule_groups=dict(required=False, type=bool),
        list_ip_sets=dict(required=False, type=bool),
        list_logging_configurations=dict(required=False, type=bool),
        list_regex_pattern_sets=dict(required=False, type=bool),
        list_rule_groups=dict(required=False, type=bool),
        list_web_acls=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_available_managed_rule_groups',
                'list_ip_sets',
                'list_logging_configurations',
                'list_regex_pattern_sets',
                'list_rule_groups',
                'list_web_acls',
            )
        ],
    )

    client = module.client('wafv2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _wafv2(client, module)

    if module.params['list_available_managed_rule_groups']:
        module.exit_json(available_managed_rule_groups=aws_response_list_parser(paginate, it, 'ManagedRuleGroups'))
    elif module.params['list_ip_sets']:
        module.exit_json(ip_sets=aws_response_list_parser(paginate, it, 'IPSets'))
    elif module.params['list_logging_configurations']:
        module.exit_json(logging_configurations=aws_response_list_parser(paginate, it, 'LoggingConfigurations'))
    elif module.params['list_regex_pattern_sets']:
        module.exit_json(regex_pattern_sets=aws_response_list_parser(paginate, it, 'RegexPatternSets'))
    elif module.params['list_rule_groups']:
        module.exit_json(rule_groups=aws_response_list_parser(paginate, it, 'RuleGroups'))
    elif module.params['list_web_acls']:
        module.exit_json(web_acls=aws_response_list_parser(paginate, it, 'WebACLs'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
