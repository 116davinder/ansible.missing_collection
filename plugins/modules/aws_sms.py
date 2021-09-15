#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sms
short_description: Send Mobile SMS with AWS SNS.
description:
  - Send Mobile SMS with AWS SNS.
version_added: 0.4.0
options:
  phone:
    description:
      - The phone number to which you want to deliver an SMS message.
      - Use E.164 format.
    required: true
    type: str
  message:
    description:
      - For SMS, each message can contain up to 140 characters.
      - This character limit depends on the encoding schema.
      - For example, an SMS message can contain 160 GSM characters,
      - 140 ASCII characters, or 70 UCS-2 characters.
      - If you publish a message that exceeds this size limit,
      - Amazon SNS sends the message as multiple messages,
      - each fitting within the size limit.
      - Messages aren't truncated mid-word but are cut off at whole-word boundaries.
      - The total size limit for a single SMS Publish action is 1,600 characters.
    required: true
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
- name: send sms using aws sns
  community.missing_collection.aws_sms:
    phone: '+359888XXXXXX'
    message: 'I am using ansible missing collection'
"""

RETURN = """
result:
  description: response of aws sns api.
  returned: when success
  type: dict
  sample: {
    'message_id': 'string'
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _sms(sns, module):
    try:
        resp = sns.publish(
            PhoneNumber=module.params['phone'],
            Message=module.params['message']
        )
        module.exit_json(result=camel_dict_to_snake_dict(resp))
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='failed to send sms')


def main():
    argument_spec = dict(
        phone=dict(required=True),
        message=dict(required=True),
    )

    module = AnsibleAWSModule(argument_spec=argument_spec)
    sns = module.client('sns')

    _sms(sns, module)


if __name__ == '__main__':
    main()
