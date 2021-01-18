#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_connect_info
short_description: Get Information about Amazon Connect.
description:
  - Get Information about Amazon Connect.
  - U(https://docs.aws.amazon.com/connect/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  instance_id:
    description:
      - The id of connect instance.
    required: false
    type: str
  routing_profile_id:
    description:
      - id of connect routing profile.
    required: false
    type: str
  list_approved_origins:
    description:
      - do you want to get list of approved origins for given I(instance_id)?
    required: false
    type: bool
  list_contact_flows:
    description:
      - do you want to get list of contact flows for given I(instance_id)?
    required: false
    type: bool
  list_hours_of_operations:
    description:
      - do you want to get list of hours of operations for given I(instance_id)?
    required: false
    type: bool
  list_instance_attributes:
    description:
      - do you want to get list of instance attributes for given I(instance_id)?
    required: false
    type: bool
  list_integration_associations:
    description:
      - do you want to get list of integration associations for given I(instance_id)?
    required: false
    type: bool
  list_lambda_functions:
    description:
      - do you want to get list of lambda functions for given I(instance_id)?
    required: false
    type: bool
  list_lex_bots:
    description:
      - do you want to get list of lex bots for given I(instance_id)?
    required: false
    type: bool
  list_phone_numbers:
    description:
      - do you want to get list of phone numbers for given I(instance_id)?
    required: false
    type: bool
  list_prompts:
    description:
      - do you want to get list of prompts for given I(instance_id)?
    required: false
    type: bool
  list_queues:
    description:
      - do you want to get list of queues for given I(instance_id)?
    required: false
    type: bool
  list_quick_connects:
    description:
      - do you want to get list of quick connects for given I(instance_id)?
    required: false
    type: bool
  list_routing_profile_queues:
    description:
      - do you want to get list of routing profile queues for given I(instance_id) and I(routing_profile_id)?
    required: false
    type: bool
  list_routing_profiles:
    description:
      - do you want to get list of routing profiles for given I(instance_id)?
    required: false
    type: bool
  list_security_keys:
    description:
      - do you want to get list of security keys for given I(instance_id)?
    required: false
    type: bool
  list_security_profiles:
    description:
      - do you want to get list of security profiles for given I(instance_id)?
    required: false
    type: bool
  list_user_hierarchy_groups:
    description:
      - do you want to get list of user hierarchy groups for given I(instance_id)?
    required: false
    type: bool
  list_users:
    description:
      - do you want to get list of users for given I(instance_id)?
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
- name: "list of connect instances."
  aws_connect_info:

- name: "list of contact flows."
  aws_connect_info:
    list_contact_flows: true
    instance_id: 'test'

- name: "list of instance hour of operations."
  aws_connect_info:
    list_hours_of_operations: true
    instance_id: 'test'

- name: "list of instance instance_attributes."
  aws_connect_info:
    list_instance_attributes: true
    instance_id: 'test'

- name: "list of instance integration associations."
  aws_connect_info:
    list_integration_associations: true
    instance_id: 'test'

- name: "list of instance lambda functions."
  aws_connect_info:
    list_lambda_functions: true
    instance_id: 'test'

- name: "list of instance lex bots."
  aws_connect_info:
    list_lex_bots: true
    instance_id: 'test'

- name: "list of phone numbers"
  aws_connect_info:
    list_phone_numbers: true
    instance_id: 'test'

- name: "list of prompts"
  aws_connect_info:
    list_prompts: true
    instance_id: 'test'

- name: "list of queues"
  aws_connect_info:
    list_queues: true
    instance_id: 'test'

- name: "list of quick connects."
  aws_connect_info:
    list_quick_connects: true
    instance_id: 'test'

- name: "list of routing profile queues"
  aws_connect_info:
    list_routing_profile_queues: true
    instance_id: 'test'
    routing_profile_id: 'test'

- name: "list of routing profiles"
  aws_connect_info:
    list_routing_profiles: true
    instance_id: 'test'

- name: "list of security keys"
  aws_connect_info:
    list_security_keys: true
    instance_id: 'test'

- name: "list of security profiles"
  aws_connect_info:
    list_security_profiles: true
    instance_id: 'test'

- name: "list of user hierarchy groups"
  aws_connect_info:
    list_user_hierarchy_groups: true
    instance_id: 'test'

- name: "list of users"
  aws_connect_info:
    list_users: true
    instance_id: 'test'
"""

RETURN = """
instances:
  description: list of connect instances.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'identity_management_type': 'SAML',
        'instance_alias': 'string',
        'created_time': datetime(2015, 1, 1),
        'service_role': 'string',
        'instance_status': 'CREATION_IN_PROGRESS',
        'inbound_calls_enabled': True|False,
        'outbound_calls_enabled': True|False
    },
  ]
contact_flows:
  description: list of contact flows.
  returned: when `list_contact_flows`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string',
        'contact_flow_type': 'CONTACT_FLOW'
    },
  ]
hour_of_operations:
  description: list of instance hour of operations.
  returned: when `list_hours_of_operations`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string'
    },
  ]
instance_attributes:
  description: list of instance instance_attributes.
  returned: when `list_instance_attributes`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'attribute_type': 'INBOUND_CALLS',
        'value': 'string'
    },
  ]
integration_associations:
  description: list of instance integration associations.
  returned: when `list_integration_associations`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'integration_association_id': 'string',
        'integration_association_arn': 'string',
        'instance_id': 'string',
        'integration_type': 'EVENT',
        'integration_arn': 'string',
        'source_application_url': 'string',
        'source_application_name': 'string',
        'source_type': 'SALESFORCE'
    },
  ]
lambda_functions:
  description: list of instance lambda functions.
  returned: when `list_lambda_functions`, and `instance_id` are defined and success
  type: list
  sample: [
    'string',
  ]
lex_bots:
  description: list of instance lex bots.
  returned: when `list_lex_bots`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'lex_region': 'string'
    },
  ]
phone_numbers:
  description: list of instance phone numbers.
  returned: when `list_phone_numbers`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'phone_number': 'string',
        'phone_number_type': 'TOLL_FREE',
        'phone_number_country_code': 'AF'
    },
  ]
prompts:
  description: list of instance prompts.
  returned: when `list_prompts`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string'
    },
  ]
queues:
  description: list of instance queues.
  returned: when `list_queues`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string',
        'queue_type': 'STANDARD'
    },
  ]
quick_connects:
  description: list of quick connects.
  returned: when `list_quick_connects`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string',
        'quick_connect_type': 'USER'
    },
  ]
routing_profile_queues:
  description: list of routing profile queues.
  returned: when `list_routing_profile_queues`, `routing_profile_id`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'queue_id': 'string',
        'queue_arn': 'string',
        'queue_name': 'string',
        'priority': 123,
        'delay': 123,
        'channel': 'VOICE'
    },
  ]
routing_profiles:
  description: list of approved routing profiles.
  returned: when `list_routing_profiles`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string'
    },
  ]
security_keys:
  description: list of approved security keys.
  returned: when `list_security_keys`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'association_id': 'string',
        'key': 'string',
        'creation_time': datetime(2015, 1, 1)
    },
  ]
security_profiles:
  description: list of approved security profiles.
  returned: when `list_security_profiles`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string'
    },
  ]
user_hierarchy_groups:
  description: list of user hierarchy groups.
  returned: when `list_user_hierarchy_groups`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'name': 'string'
    },
  ]
users:
  description: list of users.
  returned: when `list_users`, and `instance_id` are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'arn': 'string',
        'username': 'string'
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except ValueError:
                    _return.append(_app)
    else:
        for _app in iterator[resource_field]:
            try:
                _return.append(camel_dict_to_snake_dict(_app))
            except ValueError:
                _return.append(_app)
    return _return


def _connect(client, module):
    try:
        if module.params['list_approved_origins']:
            if client.can_paginate('list_approved_origins'):
                paginator = client.get_paginator('list_approved_origins')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_approved_origins(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_contact_flows']:
            if client.can_paginate('list_contact_flows'):
                paginator = client.get_paginator('list_contact_flows')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_contact_flows(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_hours_of_operations']:
            if client.can_paginate('list_hours_of_operations'):
                paginator = client.get_paginator('list_hours_of_operations')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_hours_of_operations(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_instance_attributes']:
            if client.can_paginate('list_instance_attributes'):
                paginator = client.get_paginator('list_instance_attributes')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_instance_attributes(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_integration_associations']:
            if client.can_paginate('list_integration_associations'):
                paginator = client.get_paginator('list_integration_associations')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_integration_associations(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_lambda_functions']:
            if client.can_paginate('list_lambda_functions'):
                paginator = client.get_paginator('list_lambda_functions')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_lambda_functions(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_lex_bots']:
            if client.can_paginate('list_lex_bots'):
                paginator = client.get_paginator('list_lex_bots')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_lex_bots(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_phone_numbers']:
            if client.can_paginate('list_phone_numbers'):
                paginator = client.get_paginator('list_phone_numbers')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_phone_numbers(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_prompts']:
            if client.can_paginate('list_prompts'):
                paginator = client.get_paginator('list_prompts')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_prompts(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_queues']:
            if client.can_paginate('list_queues'):
                paginator = client.get_paginator('list_queues')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_queues(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_quick_connects']:
            if client.can_paginate('list_quick_connects'):
                paginator = client.get_paginator('list_quick_connects')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_quick_connects(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_routing_profile_queues']:
            if client.can_paginate('list_routing_profile_queues'):
                paginator = client.get_paginator('list_routing_profile_queues')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                    RoutingProfileId=module.params['routing_profile_id'],
                ), True
            else:
                return client.list_routing_profile_queues(
                    InstanceId=module.params['instance_id'],
                    RoutingProfileId=module.params['routing_profile_id'],
                ), False
        elif module.params['list_routing_profiles']:
            if client.can_paginate('list_routing_profiles'):
                paginator = client.get_paginator('list_routing_profiles')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_routing_profiles(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_security_keys']:
            if client.can_paginate('list_security_keys'):
                paginator = client.get_paginator('list_security_keys')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_security_keys(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_security_profiles']:
            if client.can_paginate('list_security_profiles'):
                paginator = client.get_paginator('list_security_profiles')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_security_profiles(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_user_hierarchy_groups']:
            if client.can_paginate('list_user_hierarchy_groups'):
                paginator = client.get_paginator('list_user_hierarchy_groups')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_user_hierarchy_groups(
                    InstanceId=module.params['instance_id'],
                ), False
        elif module.params['list_users']:
            if client.can_paginate('list_users'):
                paginator = client.get_paginator('list_users')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                ), True
            else:
                return client.list_users(
                    InstanceId=module.params['instance_id'],
                ), False
        else:
            if client.can_paginate('list_instances'):
                paginator = client.get_paginator('list_instances')
                return paginator.paginate(), True
            else:
                return client.list_instances(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws connect details')


def main():
    argument_spec = dict(
        instance_id=dict(required=False),
        routing_profile_id=dict(required=False),
        list_approved_origins=dict(required=False, type=bool),
        list_contact_flows=dict(required=False, type=bool),
        list_hours_of_operations=dict(required=False, type=bool),
        list_instance_attributes=dict(required=False, type=bool),
        list_integration_associations=dict(required=False, type=bool),
        list_lambda_functions=dict(required=False, type=bool),
        list_lex_bots=dict(required=False, type=bool),
        list_phone_numbers=dict(required=False, type=bool),
        list_prompts=dict(required=False, type=bool),
        list_queues=dict(required=False, type=bool),
        list_quick_connects=dict(required=False, type=bool),
        list_routing_profile_queues=dict(required=False, type=bool),
        list_routing_profiles=dict(required=False, type=bool),
        list_security_keys=dict(required=False, type=bool),
        list_security_profiles=dict(required=False, type=bool),
        list_user_hierarchy_groups=dict(required=False, type=bool),
        list_users=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_approved_origins', True, ['instance_id']),
            ('list_contact_flows', True, ['instance_id']),
            ('list_hours_of_operations', True, ['instance_id']),
            ('list_instance_attributes', True, ['instance_id']),
            ('list_integration_associations', True, ['instance_id']),
            ('list_lambda_functions', True, ['instance_id']),
            ('list_lex_bots', True, ['instance_id']),
            ('list_phone_numbers', True, ['instance_id']),
            ('list_prompts', True, ['instance_id']),
            ('list_queues', True, ['instance_id']),
            ('list_quick_connects', True, ['instance_id']),
            ('list_routing_profile_queues', True, ['instance_id', 'routing_profile_id']),
            ('list_routing_profiles', True, ['instance_id']),
            ('list_security_keys', True, ['instance_id']),
            ('list_security_profiles', True, ['instance_id']),
            ('list_user_hierarchy_groups', True, ['instance_id']),
            ('list_users', True, ['instance_id']),
        ),
        mutually_exclusive=[
            (
                'list_approved_origins',
                'list_contact_flows',
                'list_hours_of_operations',
                'list_instance_attributes',
                'list_integration_associations',
                'list_lambda_functions',
                'list_lex_bots',
                'list_phone_numbers',
                'list_prompts',
                'list_queues',
                'list_quick_connects',
                'list_routing_profile_queues',
                'list_routing_profiles',
                'list_security_keys',
                'list_security_profiles',
                'list_user_hierarchy_groups',
                'list_users',
            )
        ],
    )

    client = module.client('connect', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _connect(client, module)

    if module.params['list_approved_origins']:
        module.exit_json(approved_origins=aws_response_list_parser(paginate, _it, 'Origins'))
    elif module.params['list_contact_flows']:
        module.exit_json(contact_flows=aws_response_list_parser(paginate, _it, 'ContactFlowSummaryList'))
    elif module.params['list_hours_of_operations']:
        module.exit_json(hour_of_operations=aws_response_list_parser(paginate, _it, 'HoursOfOperationSummaryList'))
    elif module.params['list_instance_attributes']:
        module.exit_json(instance_attributes=aws_response_list_parser(paginate, _it, 'Attributes'))
    elif module.params['list_integration_associations']:
        module.exit_json(integration_associations=aws_response_list_parser(paginate, _it, 'IntegrationAssociationSummaryList'))
    elif module.params['list_lambda_functions']:
        module.exit_json(lambda_functions=aws_response_list_parser(paginate, _it, 'LambdaFunctions'))
    elif module.params['list_lex_bots']:
        module.exit_json(lex_bots=aws_response_list_parser(paginate, _it, 'LexBots'))
    elif module.params['list_phone_numbers']:
        module.exit_json(phone_numbers=aws_response_list_parser(paginate, _it, 'PhoneNumberSummaryList'))
    elif module.params['list_prompts']:
        module.exit_json(prompts=aws_response_list_parser(paginate, _it, 'PromptSummaryList'))
    elif module.params['list_queues']:
        module.exit_json(queues=aws_response_list_parser(paginate, _it, 'QueueSummaryList'))
    elif module.params['list_quick_connects']:
        module.exit_json(quick_connects=aws_response_list_parser(paginate, _it, 'QuickConnectSummaryList'))
    elif module.params['list_routing_profile_queues']:
        module.exit_json(routing_profile_queues=aws_response_list_parser(paginate, _it, 'RoutingProfileQueueConfigSummaryList'))
    elif module.params['list_routing_profiles']:
        module.exit_json(routing_profiles=aws_response_list_parser(paginate, _it, 'RoutingProfileSummaryList'))
    elif module.params['list_security_keys']:
        module.exit_json(security_keys=aws_response_list_parser(paginate, _it, 'SecurityKeys'))
    elif module.params['list_security_profiles']:
        module.exit_json(security_profiles=aws_response_list_parser(paginate, _it, 'SecurityProfileSummaryList'))
    elif module.params['list_user_hierarchy_groups']:
        module.exit_json(user_hierarchy_groups=aws_response_list_parser(paginate, _it, 'UserHierarchyGroupSummaryList'))
    elif module.params['list_users']:
        module.exit_json(users=aws_response_list_parser(paginate, _it, 'UserSummaryList'))
    else:
        module.exit_json(instances=aws_response_list_parser(paginate, _it, 'InstanceSummaryList'))


if __name__ == '__main__':
    main()
