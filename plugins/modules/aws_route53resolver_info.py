#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_route53resolver_info
short_description: Get Information about Amazon Route 53 Resolver.
description:
  - Get Information about Amazon Route 53 Resolver.
  - U(https://docs.aws.amazon.com/Route53/latest/APIReference/API_Operations_Amazon_Route_53_Resolver.html)
version_added: 0.0.8
options:
  id:
    description:
      - can be id of firewall rule group?
      - can be id of resolver endpoint?
    required: false
    type: str
    aliases: ['firewall_rule_group_id', 'resolver_endpoint_id']
  list_firewall_configs:
    description:
      - do you want to get list of firewall_configs?
    required: false
    type: bool
  list_firewall_domain_lists:
    description:
      - do you want to get firewall_domain_lists?
    required: false
    type: bool
  list_firewall_rule_groups:
    description:
      - do you want to get list of firewall_rule_groups?
    required: false
    type: bool
  list_firewall_rules:
    description:
      - do you want to get firewall_rules for given I(id)?
    required: false
    type: bool
  list_resolver_dnssec_configs:
    description:
      - do you want to get resolver_dnssec_configs?
    required: false
    type: bool
  list_resolver_endpoint_ip_addresses:
    description:
      - do you want to get resolver_endpoint_ip_addresses for given I(id)?
    required: false
    type: bool
  list_resolver_endpoints:
    description:
      - do you want to get resolver_endpoints?
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
- name: "get list of firewall_configs"
  aws_route53resolver_info:
    list_firewall_configs: true

- name: "get firewall_domain_lists"
  aws_route53resolver_info:
    list_firewall_domain_lists: true

- name: "get list of firewall_rule_groups"
  aws_route53resolver_info:
    list_firewall_rule_groups: true

- name: "get firewall_rules"
  aws_route53resolver_info:
    list_firewall_rules: true
    id: 'firewall_rule_group_id'

- name: "get resolver_dnssec_configs"
  aws_route53resolver_info:
    list_resolver_dnssec_configs: true

- name: "get resolver_endpoint_ip_addresses"
  aws_route53resolver_info:
    list_resolver_endpoint_ip_addresses: true
    id: 'resolver_endpoint_id'

- name: "get resolver_endpoints"
  aws_route53resolver_info:
    list_resolver_endpoints: true
"""

RETURN = """
firewall_configs:
  description: list of firewall_configs.
  returned: when `list_firewall_configs` is defined and success.
  type: list
firewall_domain_lists:
  description: get of firewall_domain_lists.
  returned: when `list_firewall_domain_lists` is defined and success.
  type: list
firewall_rule_groups:
  description: list of firewall_rule_groups.
  returned: when `list_firewall_rule_groups` is defined and success.
  type: list
firewall_rules:
  description: list of firewall_rules.
  returned: when `list_firewall_rules` is defined and success.
  type: list
resolver_dnssec_configs:
  description: list of resolver_dnssec_configs.
  returned: when `list_resolver_dnssec_configs` is defined and success.
  type: list
resolver_endpoint_ip_addresses:
  description: list of resolver_endpoint_ip_addresses.
  returned: when `list_resolver_endpoint_ip_addresses` is defined and success.
  type: list
resolver_endpoints:
  description: list of resolver_endpoints.
  returned: when `list_resolver_endpoints` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _route53resolver(client, module):
    try:
        if module.params['list_firewall_configs']:
            if client.can_paginate('list_firewall_configs'):
                paginator = client.get_paginator('list_firewall_configs')
                return paginator.paginate(), True
            else:
                return client.list_firewall_configs(), False
        elif module.params['list_firewall_domain_lists']:
            if client.can_paginate('list_firewall_domain_lists'):
                paginator = client.get_paginator('list_firewall_domain_lists')
                return paginator.paginate(), True
            else:
                return client.list_firewall_domain_lists(), False
        elif module.params['list_firewall_rule_groups']:
            if client.can_paginate('list_firewall_rule_groups'):
                paginator = client.get_paginator('list_firewall_rule_groups')
                return paginator.paginate(), True
            else:
                return client.list_firewall_rule_groups(), False
        elif module.params['list_firewall_rules']:
            if client.can_paginate('list_firewall_rules'):
                paginator = client.get_paginator('list_firewall_rules')
                return paginator.paginate(
                    FirewallRuleGroupId=module.params['id']
                ), True
            else:
                return client.list_firewall_rules(
                    FirewallRuleGroupId=module.params['id']
                ), False
        elif module.params['list_resolver_dnssec_configs']:
            if client.can_paginate('list_resolver_dnssec_configs'):
                paginator = client.get_paginator('list_resolver_dnssec_configs')
                return paginator.paginate(), True
            else:
                return client.list_resolver_dnssec_configs(), False
        elif module.params['list_resolver_endpoint_ip_addresses']:
            if client.can_paginate('list_resolver_endpoint_ip_addresses'):
                paginator = client.get_paginator('list_resolver_endpoint_ip_addresses')
                return paginator.paginate(
                    ResolverEndpointId=module.params['id']
                ), True
            else:
                return client.list_resolver_endpoint_ip_addresses(
                    ResolverEndpointId=module.params['id']
                ), False
        elif module.params['list_resolver_endpoints']:
            if client.can_paginate('list_resolver_endpoints'):
                paginator = client.get_paginator('list_resolver_endpoints')
                return paginator.paginate(), True
            else:
                return client.list_resolver_endpoints(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Route 53 Resolver details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['firewall_rule_group_id', 'resolver_endpoint_id']),
        list_firewall_configs=dict(required=False, type=bool),
        list_firewall_domain_lists=dict(required=False, type=bool),
        list_firewall_rule_groups=dict(required=False, type=bool),
        list_firewall_rules=dict(required=False, type=bool),
        list_resolver_dnssec_configs=dict(required=False, type=bool),
        list_resolver_endpoint_ip_addresses=dict(required=False, type=bool),
        list_resolver_endpoints=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_firewall_rules', True, ['id']),
            ('list_resolver_endpoint_ip_addresses', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_firewall_configs',
                'list_firewall_domain_lists',
                'list_firewall_rule_groups',
                'list_firewall_rules',
                'list_resolver_dnssec_configs',
                'list_resolver_endpoint_ip_addresses',
                'list_resolver_endpoints',
            )
        ],
    )

    client = module.client('route53resolver', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _route53resolver(client, module)

    if module.params['list_firewall_configs']:
        module.exit_json(firewall_configs=aws_response_list_parser(paginate, it, 'FirewallConfigs'))
    elif module.params['list_firewall_domain_lists']:
        module.exit_json(firewall_domain_lists=aws_response_list_parser(paginate, it, 'FirewallDomainLists'))
    elif module.params['list_firewall_rule_groups']:
        module.exit_json(firewall_rule_groups=aws_response_list_parser(paginate, it, 'FirewallRuleGroups'))
    elif module.params['list_firewall_rules']:
        module.exit_json(firewall_rules=aws_response_list_parser(paginate, it, 'FirewallRules'))
    elif module.params['list_resolver_dnssec_configs']:
        module.exit_json(resolver_dnssec_configs=aws_response_list_parser(paginate, it, 'ResolverDnssecConfigs'))
    elif module.params['list_resolver_endpoint_ip_addresses']:
        module.exit_json(resolver_endpoint_ip_addresses=aws_response_list_parser(paginate, it, 'IpAddresses'))
    elif module.params['list_resolver_endpoints']:
        module.exit_json(resolver_endpoints=aws_response_list_parser(paginate, it, 'ResolverEndpoints'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
