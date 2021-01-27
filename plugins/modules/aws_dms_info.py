#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_dms_info
short_description: Get Information about AWS Database Migration Service.
description:
  - Get Information about AWS Database Migration Service
  - U(https://docs.aws.amazon.com/dms/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  arn:
    description:
      - endpoint arn.
    required: false
    type: str
  source_type:
    description:
      - type of source.
    required: false
    type: str
    choices: ['replication-instance', 'replication-task']
    default: 'replication-instance'
  describe_replication_instances:
    description:
      - do you want to get list of replication instances?
    required: false
    type: bool
  describe_certificates:
    description:
      - do you want to get list of certificates?
    required: false
    type: bool
  describe_endpoints:
    description:
      - do you want to get list of endpoints?
    required: false
    type: bool
  describe_event_categories:
    description:
      - do you want to get list of event categories?
    required: false
    type: bool
  describe_event_subscriptions:
    description:
      - do you want to get list of event subscriptions?
    required: false
    type: bool
  describe_events:
    description:
      - do you want to get list of events for I(source_type)?
    required: false
    type: bool
  describe_pending_maintenance_actions:
    description:
      - do you want to get list of pending maintenance actions?
    required: false
    type: bool
  describe_replication_subnet_groups:
    description:
      - do you want to get list of replication subnet groups?
    required: false
    type: bool
  describe_replication_tasks:
    description:
      - do you want to get list of replication tasks?
    required: false
    type: bool
  describe_schemas:
    description:
      - do you want to get list of schemas for I(arn)?
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
- name: "get list of replication instances."
  aws_dms_info:
    describe_replication_instances: true

- name: "get list of certificates."
  aws_dms_info:
    describe_certificates: true

- name: "get list of endpoints."
  aws_dms_info:
    describe_endpoints: true

- name: "get list of event categories."
  aws_dms_info:
    describe_event_categories: true

- name: "get list of event subscriptions."
  aws_dms_info:
    describe_event_subscriptions: true

- name: "get list of events."
  aws_dms_info:
    describe_events: true
    source_type: 'replication-instance'

- name: "get list of pending maintenance actions."
  aws_dms_info:
    describe_pending_maintenance_actions: true

- name: "get list of replication subnet groups."
  aws_dms_info:
    describe_replication_subnet_groups: true

- name: "get list of replication tasks."
  aws_dms_info:
    describe_replication_tasks: true

- name: "get list of schemas."
  aws_dms_info:
    describe_schemas: true
    arn: 'test-endpoint-arn'
"""

RETURN = """
replication_instances:
  description: list of replication instances.
  returned: when `describe_replication_instances` is defined and success
  type: list
certificates:
  description: list of certificates.
  returned: when `describe_certificates` is defined and success
  type: list
endpoints:
  description: list of endpoints.
  returned: when `describe_endpoints` is defined and success
  type: list
event_categories:
  description: list of event categories.
  returned: when `describe_event_categories` is defined and success
  type: list
event_subscriptions:
  description: list of event subscriptions.
  returned: when `describe_event_subscriptions` is defined and success
  type: list
events:
  description: list of events.
  returned: when `describe_events` is defined and success
  type: list
pending_maintenance_actions:
  description: list of pending maintenance actions.
  returned: when `describe_pending_maintenance_actions` is defined and success
  type: list
replication_subnet_groups:
  description: list of replication subnet groups.
  returned: when `describe_replication_subnet_groups` is defined and success
  type: list
replication_tasks:
  description: list of replication tasks.
  returned: when `describe_replication_tasks` is defined and success
  type: list
schemas:
  description: list of schemas.
  returned: when `describe_schemas` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _dms(client, module):
    try:
        if module.params['describe_replication_instances']:
            if client.can_paginate('describe_replication_instances'):
                paginator = client.get_paginator('describe_replication_instances')
                return paginator.paginate(), True
            else:
                return client.describe_replication_instances(), False
        elif module.params['describe_certificates']:
            if client.can_paginate('describe_certificates'):
                paginator = client.get_paginator('describe_certificates')
                return paginator.paginate(), True
            else:
                return client.describe_certificates(), False
        elif module.params['describe_endpoints']:
            if client.can_paginate('describe_endpoints'):
                paginator = client.get_paginator('describe_endpoints')
                return paginator.paginate(), True
            else:
                return client.describe_endpoints(), False
        elif module.params['describe_event_categories']:
            if client.can_paginate('describe_event_categories'):
                paginator = client.get_paginator('describe_event_categories')
                return paginator.paginate(), True
            else:
                return client.describe_event_categories(), False
        elif module.params['describe_event_subscriptions']:
            if client.can_paginate('describe_event_subscriptions'):
                paginator = client.get_paginator('describe_event_subscriptions')
                return paginator.paginate(), True
            else:
                return client.describe_event_subscriptions(), False
        elif module.params['describe_events']:
            if client.can_paginate('describe_events'):
                paginator = client.get_paginator('describe_events')
                return paginator.paginate(
                    SourceType=module.params['source_type'],
                ), True
            else:
                return client.describe_events(
                    SourceType=module.params['source_type'],
                ), False
        elif module.params['describe_pending_maintenance_actions']:
            if client.can_paginate('describe_pending_maintenance_actions'):
                paginator = client.get_paginator('describe_pending_maintenance_actions')
                return paginator.paginate(), True
            else:
                return client.describe_pending_maintenance_actions(), False
        elif module.params['describe_replication_subnet_groups']:
            if client.can_paginate('describe_replication_subnet_groups'):
                paginator = client.get_paginator('describe_replication_subnet_groups')
                return paginator.paginate(), True
            else:
                return client.describe_replication_subnet_groups(), False
        elif module.params['describe_replication_tasks']:
            if client.can_paginate('describe_replication_tasks'):
                paginator = client.get_paginator('describe_replication_tasks')
                return paginator.paginate(), True
            else:
                return client.describe_replication_tasks(), False
        elif module.params['describe_schemas']:
            if client.can_paginate('describe_schemas'):
                paginator = client.get_paginator('describe_schemas')
                return paginator.paginate(
                    EndpointArn=module.params['arn'],
                ), True
            else:
                return client.describe_schemas(
                    EndpointArn=module.params['arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS DMS details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        source_type=dict(required=False, choices=['replication-instance', 'replication-task'], default='replication-instance'),
        describe_replication_instances=dict(required=False, type=bool),
        describe_certificates=dict(required=False, type=bool),
        describe_endpoints=dict(required=False, type=bool),
        describe_event_categories=dict(required=False, type=bool),
        describe_event_subscriptions=dict(required=False, type=bool),
        describe_events=dict(required=False, type=bool),
        describe_pending_maintenance_actions=dict(required=False, type=bool),
        describe_replication_subnet_groups=dict(required=False, type=bool),
        describe_replication_tasks=dict(required=False, type=bool),
        describe_schemas=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_schemas', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'describe_replication_instances',
                'describe_certificates',
                'describe_endpoints',
                'describe_event_categories',
                'describe_event_subscriptions',
                'describe_events',
                'describe_pending_maintenance_actions',
                'describe_replication_subnet_groups',
                'describe_replication_tasks',
                'describe_schemas',
            )
        ],
    )

    client = module.client('dms', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _dms(client, module)

    if module.params['describe_replication_instances']:
        module.exit_json(replication_instances=aws_response_list_parser(paginate, it, 'ReplicationInstances'))
    elif module.params['describe_certificates']:
        module.exit_json(certificates=aws_response_list_parser(paginate, it, 'Certificates'))
    elif module.params['describe_endpoints']:
        module.exit_json(endpoints=aws_response_list_parser(paginate, it, 'Endpoints'))
    elif module.params['describe_event_categories']:
        module.exit_json(event_categories=aws_response_list_parser(paginate, it, 'EventCategoryGroupList'))
    elif module.params['describe_event_subscriptions']:
        module.exit_json(event_subscriptions=aws_response_list_parser(paginate, it, 'EventSubscriptionsList'))
    elif module.params['describe_events']:
        module.exit_json(events=aws_response_list_parser(paginate, it, 'Events'))
    elif module.params['describe_pending_maintenance_actions']:
        module.exit_json(pending_maintenance_actions=aws_response_list_parser(paginate, it, 'PendingMaintenanceActions'))
    elif module.params['describe_replication_subnet_groups']:
        module.exit_json(replication_subnet_groups=aws_response_list_parser(paginate, it, 'ReplicationSubnetGroups'))
    elif module.params['describe_replication_tasks']:
        module.exit_json(replication_tasks=aws_response_list_parser(paginate, it, 'ReplicationTasks'))
    elif module.params['describe_schemas']:
        module.exit_json(schemas=aws_response_list_parser(paginate, it, 'Schemas'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
