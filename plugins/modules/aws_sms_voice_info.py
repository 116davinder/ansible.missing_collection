#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sms-voice_info
short_description: Get Information about Amazon PinPoint Sms Voice.
description:
  - Get Information about Amazon PinPoint Sms Voice.
  - U(https://docs.aws.amazon.com/pinpoint-sms-voice/latest/APIReference/resources.html)
version_added: 0.0.8
options:
  name:
    description:
      - configuration set name.
    required: false
    type: str
    aliases: ['configuration_set_name']
  get_configuration_set_event_destinations:
    description:
      - do you want to get list of configuration_set_event_destinations for given configuration set I(name)?
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
- name: "get list of configuration_set_event_destinations"
  aws_sms-voice_info:
    get_configuration_set_event_destinations: true
    name: 'configuration_set_name'
"""

RETURN = """
configuration_set_event_destinations:
  description: list of configuration_set_event_destinations.
  returned: when `get_configuration_set_event_destinations` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sms_voice(client, module):
    try:
        if module.params['get_configuration_set_event_destinations']:
            if client.can_paginate('get_configuration_set_event_destinations'):
                paginator = client.get_paginator('get_configuration_set_event_destinations')
                return paginator.paginate(
                    ConfigurationSetName=module.params['name']
                ), True
            else:
                return client.get_configuration_set_event_destinations(
                    ConfigurationSetName=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS PinPoint Sms-voice details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['configuration_set_name']),
        get_configuration_set_event_destinations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_configuration_set_event_destinations', True, ['name']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('sms-voice', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sms_voice(client, module)

    if module.params['get_configuration_set_event_destinations']:
        module.exit_json(configuration_set_event_destinations=aws_response_list_parser(paginate, it, 'EventDestinations'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
