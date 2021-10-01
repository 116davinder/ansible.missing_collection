#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sms_info
short_description: Get Information about Amazon SNS SMS.
description:
  - Get Information about Amazon SNS SMS.
version_added: 0.4.0
options:
  get_sms_sandbox_account_status:
    description:
      - do you want to get sandbox account status?
    required: false
    type: bool
  list_phone_numbers_opted_out:
    description:
      - do you want to get list of phone number opted out?
    required: false
    type: bool
  list_sms_sandbox_phone_numbers:
    description:
      - do you want to get list of phone numbers registered with account?
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
- name: "get sms sandbox account status"
  community.missing_collection.aws_sms_info:
    get_sms_sandbox_account_status: true

- name: "get list of phones opted out"
  community.missing_collection.aws_sms_info:
    list_phone_numbers_opted_out: true

- name: "get list of sandbox registered numbers"
  community.missing_collection.aws_sms_info:
    list_sms_sandbox_phone_numbers: true
"""

RETURN = """
is_in_sandbox:
  description: sms sandbox account status.
  returned: when I(get_sms_sandbox_account_status) is defined and success.
  type: bool
  sample: true
phone_numbers_opted_out:
  description: list of phones opted out.
  returned: when I(list_phone_numbers_opted_out) is defined and success.
  type: list
phone_numbers:
  description: list of sandbox registered numbers.
  returned: when I(list_sms_sandbox_phone_numbers) is defined and success.
  type: list
  sample: [{"phone_number": "+359888XXXXX", "status": "Verified"}]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sms(client, module):
    try:
        if module.params['get_sms_sandbox_account_status']:
            return client.get_sms_sandbox_account_status(), False
        elif module.params['list_phone_numbers_opted_out']:
            if client.can_paginate('list_phone_numbers_opted_out'):
                paginator = client.get_paginator('list_phone_numbers_opted_out')
                return paginator.paginate(), True
            else:
                return client.list_phone_numbers_opted_out(), False
        elif module.params['list_sms_sandbox_phone_numbers']:
            if client.can_paginate('list_sms_sandbox_phone_numbers'):
                paginator = client.get_paginator('list_sms_sandbox_phone_numbers')
                return paginator.paginate(), True
            else:
                return client.list_sms_sandbox_phone_numbers(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon SNS SMS details')


def main():
    argument_spec = dict(
        get_sms_sandbox_account_status=dict(required=False, type=bool),
        list_phone_numbers_opted_out=dict(required=False, type=bool),
        list_sms_sandbox_phone_numbers=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            (
                'get_sms_sandbox_account_status',
                'list_phone_numbers_opted_out',
                'list_sms_sandbox_phone_numbers',
            )
        ],
    )

    client = module.client('sns', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sms(client, module)

    if module.params['get_sms_sandbox_account_status']:
        module.exit_json(is_in_sandbox=it['IsInSandbox'])
    elif module.params['list_phone_numbers_opted_out']:
        module.exit_json(phone_numbers_opted_out=aws_response_list_parser(paginate, it, 'phoneNumbers'))
    elif module.params['list_sms_sandbox_phone_numbers']:
        module.exit_json(phone_numbers=aws_response_list_parser(paginate, it, 'PhoneNumbers'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
