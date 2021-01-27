#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_notifications_info
short_description: Get Information about AWS CodeStar Notifications.
description:
  - Get Information about AWS CodeStar Notifications.
  - U(https://docs.aws.amazon.com/codestar-notifications/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  arn:
    description:
      - arn of codestar notification rule.
    required: false
    type: str
  list_event_types:
    description:
      - do you want to get list of event types?
    required: false
    type: bool
  list_targets:
    description:
      - do you want to get list of targets?
    required: false
    type: bool
  describe_notification_rule:
    description:
      - do you want to get details about notification rule?
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
- name: "get list of codestar notification rules"
  aws_codestar_notifications_info:

- name: "get list of codestar targets"
  aws_codestar_notifications_info:
    list_targets: true

- name: "get details about notification rule"
  aws_codestar_notifications_info:
    describe_notification_rule: true
    arn: 'test-notification-rule-arn'
"""

RETURN = """
rules:
  description: get list of codestar notifications rules.
  returned: when no argument and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string'
    },
  ]
event_types:
  description: get list of event types.
  returned: when `list_event_types` is defined and success
  type: list
  sample: [
    {
        'event_type_id': 'string',
        'service_name': 'string',
        'event_type_name': 'string',
        'resource_type': 'string'
    },
  ]
targets:
  description: get list of targets.
  returned: when `list_targets` is defined and success
  type: list
  sample: [
    {
        'target_address': 'string',
        'target_type': 'string',
        'target_status': 'PENDING'
    },
  ]
rule:
  description: get details about notification rule.
  returned: when `describe_notification_rule` and `arn` are defined and success
  type: dict
  sample: {
    'arn': 'string',
    'name': 'string',
    'event_types': [],
    'resource': 'string',
    'targets': [],
    'detail_type': 'BASIC',
    'created_by': 'string',
    'status': 'ENABLED',
    'created_timestamp': datetime(2016, 6, 6),
    'last_modified_timestamp': datetime(2015, 1, 1),
    'Tags': {}
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _codestar(client, module):
    try:
        if module.params['list_event_types']:
            if client.can_paginate('list_event_types'):
                paginator = client.get_paginator('list_event_types')
                return paginator.paginate(), True
            else:
                return client.list_event_types(), False
        elif module.params['list_targets']:
            if client.can_paginate('list_targets'):
                paginator = client.get_paginator('list_targets')
                return paginator.paginate(), True
            else:
                return client.list_targets(), False
        elif module.params['describe_notification_rule']:
            return client.describe_notification_rule(
                Arn=module.params['arn']
            ), False
        else:
            if client.can_paginate('list_notification_rules'):
                paginator = client.get_paginator('list_notification_rules')
                return paginator.paginate(), True
            else:
                return client.list_notification_rules(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codestar notifications details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        list_event_types=dict(required=False, type=bool),
        list_targets=dict(required=False, type=bool),
        describe_notification_rule=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_notification_rule', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_event_types',
                'list_targets',
                'describe_notification_rule',
            )
        ],
    )

    client = module.client('codestar-notifications', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codestar(client, module)

    if module.params['list_event_types']:
        module.exit_json(event_types=aws_response_list_parser(paginate, _it, 'EventTypes'))
    elif module.params['list_targets']:
        module.exit_json(targets=aws_response_list_parser(paginate, _it, 'Targets'))
    elif module.params['describe_notification_rule']:
        module.exit_json(rule=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(rules=aws_response_list_parser(paginate, _it, 'NotificationRules'))


if __name__ == '__main__':
    main()
