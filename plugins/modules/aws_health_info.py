#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_health_info
short_description: Get Information about Amazon Health.
description:
  - Get Information about Amazon Health.
  - U(https://docs.aws.amazon.com/health/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  arn:
    description:
      - arn of event.
    required: false
    type: str
  arns:
    description:
      - list of event arn.
    required: false
    type: list
  services:
    description:
      - list of aws services.
    required: false
    type: list
    default: []
  event_type_categories:
    description:
      - type of event.
    required: false
    type: list
    default: []
  describe_health_service_status_for_organization:
    description:
      - do you want to get health_service_status_for_organization?
    required: false
    type: bool
  describe_events:
    description:
      - do you want to get list of events for given I(services) and I(event_type_categories)?
    required: false
    type: bool
  describe_event_details:
    description:
      - do you want to get event details for given events I(arns)?
    required: false
    type: bool
  describe_affected_accounts_for_organization:
    description:
      - do you want to get affected_accounts_for_organization for given event I(arn)?
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
- name: "get health_service_status_for_organization"
  aws_health_info:
    describe_health_service_status_for_organization: true

- name: "get list of events"
  aws_health_info:
    describe_events: true
    event_type_categories: ['issue']
    services: ['EC2']

- name: "get event_details"
  aws_health_info:
    describe_event_details: true
    arns: ['test']

- name: "get list of affected_accounts_for_organization"
  aws_health_info:
    describe_affected_accounts_for_organization: true
    arn: 'test'

"""

RETURN = """
health_service_status_for_organization:
  description: list of health_service_status_for_organization.
  returned: when `describe_health_service_status_for_organization` is defined and success.
  type: dict
events:
  description: list of events.
  returned: when `describe_events` is defined and success.
  type: list
event_details:
  description: list of event_details.
  returned: when `describe_event_details` is defined and success.
  type: dict
affected_accounts_for_organization:
  description: list of affected_accounts_for_organization.
  returned: when `describe_affected_accounts_for_organization` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _health(client, module):
    try:
        if module.params['describe_health_service_status_for_organization']:
            return client.describe_health_service_status_for_organization(), False
        elif module.params['describe_events']:
            if client.can_paginate('describe_events'):
                paginator = client.get_paginator('describe_events')
                return paginator.paginate(
                    filter={
                        "services": module.params['services'],
                        "eventTypeCategories": module.params['event_type_categories'],
                    }
                ), True
            else:
                return client.describe_events(
                    filter={
                        "services": module.params['services'],
                        "eventTypeCategories": module.params['event_type_categories'],
                    }
                ), False
        elif module.params['describe_event_details']:
            if client.can_paginate('describe_event_details'):
                paginator = client.get_paginator('describe_event_details')
                return paginator.paginate(
                    eventArns=module.params['arns']
                ), True
            else:
                return client.describe_event_details(
                    eventArns=module.params['arns']
                ), False
        elif module.params['describe_affected_accounts_for_organization']:
            return client.describe_affected_accounts_for_organization(
                eventArn=module.params['arn']
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Health details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        arns=dict(required=False, type=list),
        event_type_categories=dict(required=False, type=list, default=[]),
        services=dict(required=False, type=list, default=[]),
        describe_health_service_status_for_organization=dict(required=False, type=bool),
        describe_events=dict(required=False, type=bool),
        describe_event_details=dict(required=False, type=bool),
        describe_affected_accounts_for_organization=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_event_details', True, ['arns']),
            ('describe_affected_accounts_for_organization', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'describe_health_service_status_for_organization',
                'describe_events',
                'describe_event_details',
                'describe_affected_accounts_for_organization',
            )
        ],
    )

    client = module.client('health', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _health(client, module)

    if module.params['describe_health_service_status_for_organization']:
        module.exit_json(health_service_status_for_organization=it['healthServiceAccessStatusForOrganization'])
    elif module.params['describe_events']:
        module.exit_json(events=aws_response_list_parser(paginate, it, 'events'))
    elif module.params['describe_event_details']:
        module.exit_json(event_details=camel_dict_to_snake_dict(it))
    elif module.params['describe_affected_accounts_for_organization']:
        module.exit_json(affected_accounts_for_organization=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
