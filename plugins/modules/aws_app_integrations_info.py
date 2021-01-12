#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_app_integrations_info
short_description: Get details about Amazon AppIntegrations Service.
description:
  - Get Information about Amazon AppIntegrations Service.
  - U(https://docs.aws.amazon.com/appintegrations/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  name:
    description:
      - name of event integration.
    required: false
    type: str
    aliases: ['event_integration_name']
  list_event_integration_associations:
    description:
      - do you want to fetch all event integrations associations for given I(name)?
    required: false
    type: bool
  describe_event_integration:
    description:
      - do you want to describe given I(name)?
    required: false
    type: str
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
- name: "list workspaces for given alias"
  aws_app_integrations_info:

- name: "list of app integration associations given event name"
  aws_app_integrations_info:
    name: 'test'
    list_event_integration_associations: true

- name: "describe aws app event integrations"
  aws_app_integrations_info:
    name: 'test'
    describe_event_integration: true
"""

RETURN = """
event_integrations:
  description: List of event integrations.
  returned: when no argument and success
  type: list
  sample: [
    {
        'event_integration_arn': 'string',
        'name': 'string',
        'description': 'string',
        'event_filter': {
            'source': 'string'
        },
        'event_bridge_bus': 'string',
        'tags': {
            'string': 'string'
        }
    },
  ]
event_integration_associations:
  description: List of event integrations associations for given event name.
  returned: when `name` is defined and `list_event_integration_associations=true` and success
  type: list
  sample: [
    {
        'event_integration_association_arn': 'string',
        'event_integration_association_id': 'string',
        'event_integration_name': 'string',
        'client_id': 'string',
        'event_bridge_rule_name': 'string',
        'client_association_metadata': {
            'string': 'string'
        }
    },
  ]
event_integration:
  description: details about given event name.
  returned: when `name` is defined and `describe_event_integration=true` and success
  type: dict
  sample: {
    'name': 'string',
    'description': 'string',
    'event_integration_arn': 'string',
    'event_bridge_bus': 'string',
    'event_filter': {
        'source': 'string'
    },
    'tags': {
        'string': 'string'
    }
  }
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _appintegrations(client, module):
    try:
        if module.params['list_event_integration_associations']:
            if client.can_paginate('list_event_integration_associations'):
                paginator = client.get_paginator('list_event_integration_associations')
                return paginator.paginate(
                    EventIntegrationName=module.params['name']
                ), True
            else:
                return client.list_event_integration_associations(
                    EventIntegrationName=module.params['name']
                ), False
        elif module.params['describe_event_integration']:
            if client.can_paginate('get_event_integration'):
                paginator = client.get_paginator('get_event_integration')
                return paginator.paginate(
                    Name=module.params['name']
                ), True
            else:
                return client.get_event_integration(
                    Name=module.params['name']
                ), False
        else:
            if client.can_paginate('list_event_integrations'):
                paginator = client.get_paginator('list_event_integrations')
                return paginator.paginate(), True
            else:
                return client.list_event_integrations(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws app integrations details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['event_integration_name']),
        list_event_integration_associations=dict(required=False, type=bool),
        describe_event_integration=dict(required=False, type=bool)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_event_integration_associations', True, ['name']),
            ('describe_event_integration', True, ['name']),
        ],
        mutually_exclusive=[
            ('list_event_integration_associations', 'describe_event_integration')
        ],
    )

    # remove below warning once service become GA
    module.warn("aws app integration service is preview on 25-12-2020")

    appintegrations = module.client('appintegrations', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _appintegrations(appintegrations, module)

    if module.params['list_event_integration_associations']:
        module.exit_json(event_integration_associations=aws_response_list_parser(paginate, _it, 'EventIntegrationAssociations'))
    elif module.params['describe_event_integration']:
        module.exit_json(event_integration=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(event_integrations=aws_response_list_parser(paginate, _it, 'EventIntegrations'))


if __name__ == '__main__':
    main()
