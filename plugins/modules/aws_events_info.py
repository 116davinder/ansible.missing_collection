#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_events_info
short_description: Get Information about Amazon EventBridge.
description:
  - Get Information about Amazon EventBridge.
  - U(https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  name_prefix:
    description:
      - name prefix to filter results.
    required: false
    type: str
  event_source_name:
    description:
      - event source name.
    required: false
    type: str
  list_archives:
    description:
      - do you want to get list of archives for given I(name_prefix)?
    required: false
    type: bool
  list_event_buses:
    description:
      - do you want to get list of event buses for given I(name_prefix)?
    required: false
    type: bool
  list_partner_event_source_accounts:
    description:
      - do you want to get list of partner event source accounts for given I(event_source_name)?
    required: false
    type: bool
  list_partner_event_sources:
    description:
      - do you want to get list of partner event sources for given I(name_prefix)?
    required: false
    type: bool
  list_replays:
    description:
      - do you want to get list of replays for given I(name_prefix)?
    required: false
    type: bool
  list_rules:
    description:
      - do you want to get list of rules for given I(name_prefix)?
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
- name: "get list of archives"
  aws_events_info:
    list_archives: true
    name_prefix: 'test'

- name: "get list of event buses"
  aws_events_info:
    list_event_buses: true
    name_prefix: 'test'

- name: "get list of event sources"
  aws_events_info:
    list_event_sources: true
    name_prefix: 'test'

- name: "get list of partner event source accounts"
  aws_events_info:
    list_partner_event_source_accounts: true
    event_source_name: 'test'

- name: "get list of partner event sources"
  aws_events_info:
    list_partner_event_sources: true
    name_prefix: 'test'

- name: "get list of replays"
  aws_events_info:
    list_replays: true
    name_prefix: 'test'

- name: "get list of rules"
  aws_events_info:
    list_rules: true
    name_prefix: 'test'
"""

RETURN = """
archives:
  description: list of archives.
  returned: when `list_archives` is defined and success
  type: list
event_buses:
  description: list of event buses.
  returned: when `list_event_buses` is defined and success
  type: list
event_sources:
  description: list of event sources.
  returned: when `list_event_sources` is defined and success
  type: list
partner_event_source_accounts:
  description: list of partner event source accounts.
  returned: when `list_partner_event_source_accounts` is defined and success
  type: list
partner_event_sources:
  description: list of partner event sources.
  returned: when `list_partner_event_sources` is defined and success
  type: list
replays:
  description: list of replays.
  returned: when `list_replays` is defined and success
  type: list
rules:
  description: list of rules.
  returned: when `list_rules` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _events(client, module):
    try:
        if module.params['list_archives']:
            if client.can_paginate('list_archives'):
                paginator = client.get_paginator('list_archives')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_archives(
                    NamePrefix=module.params['name_prefix'],
                ), False
        elif module.params['list_event_buses']:
            if client.can_paginate('list_event_buses'):
                paginator = client.get_paginator('list_event_buses')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_event_buses(
                    NamePrefix=module.params['name_prefix'],
                ), False
        elif module.params['list_event_sources']:
            if client.can_paginate('list_event_sources'):
                paginator = client.get_paginator('list_event_sources')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_event_sources(
                    NamePrefix=module.params['name_prefix'],
                ), False
        elif module.params['list_partner_event_source_accounts']:
            if client.can_paginate('list_partner_event_source_accounts'):
                paginator = client.get_paginator('list_partner_event_source_accounts')
                return paginator.paginate(
                    EventSourceName=module.params['event_source_name'],
                ), True
            else:
                return client.list_partner_event_source_accounts(
                    EventSourceName=module.params['event_source_name'],
                ), False
        elif module.params['list_partner_event_sources']:
            if client.can_paginate('list_partner_event_sources'):
                paginator = client.get_paginator('list_partner_event_sources')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_partner_event_sources(
                    NamePrefix=module.params['name_prefix'],
                ), False
        elif module.params['list_replays']:
            if client.can_paginate('list_replays'):
                paginator = client.get_paginator('list_replays')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_replays(
                    NamePrefix=module.params['name_prefix'],
                ), False
        elif module.params['list_rules']:
            if client.can_paginate('list_rules'):
                paginator = client.get_paginator('list_rules')
                return paginator.paginate(
                    NamePrefix=module.params['name_prefix'],
                ), True
            else:
                return client.list_rules(
                    NamePrefix=module.params['name_prefix'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon EventBridge Details')


def main():
    argument_spec = dict(
        name_prefix=dict(required=False),
        event_source_name=dict(required=False),
        list_archives=dict(required=False, type=bool),
        list_event_buses=dict(required=False, type=bool),
        list_event_sources=dict(required=False, type=bool),
        list_partner_event_source_accounts=dict(required=False, type=bool),
        list_partner_event_sources=dict(required=False, type=bool),
        list_replays=dict(required=False, type=bool),
        list_rules=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_archives', True, ['name_prefix']),
            ('list_event_buses', True, ['name_prefix']),
            ('list_event_sources', True, ['name_prefix']),
            ('list_partner_event_source_accounts', True, ['event_source_name']),
            ('list_partner_event_sources', True, ['name_prefix']),
            ('list_replays', True, ['name_prefix']),
            ('list_rules', True, ['name_prefix']),
        ),
        mutually_exclusive=[
            (
                'list_archives',
                'list_event_buses',
                'list_event_sources',
                'list_partner_event_source_accounts',
                'list_partner_event_sources',
                'list_replays',
                'list_rules',
            )
        ],
    )

    client = module.client('events', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _events(client, module)

    if module.params['list_archives']:
        module.exit_json(archives=aws_response_list_parser(paginate, it, 'Archives'))
    elif module.params['list_event_buses']:
        module.exit_json(event_buses=aws_response_list_parser(paginate, it, 'EventBuses'))
    elif module.params['list_event_sources']:
        module.exit_json(event_sources=aws_response_list_parser(paginate, it, 'EventSources'))
    elif module.params['list_partner_event_source_accounts']:
        module.exit_json(partner_event_source_accounts=aws_response_list_parser(paginate, it, 'PartnerEventSourceAccounts'))
    elif module.params['list_partner_event_sources']:
        module.exit_json(partner_event_sources=aws_response_list_parser(paginate, it, 'PartnerEventSources'))
    elif module.params['list_replays']:
        module.exit_json(replays=aws_response_list_parser(paginate, it, 'Replays'))
    elif module.params['list_rules']:
        module.exit_json(rules=aws_response_list_parser(paginate, it, 'Rules'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
