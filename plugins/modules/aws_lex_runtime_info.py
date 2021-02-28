#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_lex_runtime_info
short_description: Get Information about Amazon Lex Runtime Service.
description:
  - Get Information about Amazon Lex Runtime Service.
  - U(https://docs.aws.amazon.com/lex/latest/dg/API_Operations_Amazon_Lex_Runtime_Service.html)
version_added: 0.0.7
options:
  bot_name:
    description:
      - name of bot.
    required: false
    type: str
  bot_alias:
    description:
      - bot alias.
    required: false
    type: str
  user_id:
    description:
      - The ID of the client application user.
    required: false
    type: str
  get_session:
    description:
      - do you want to get session details?
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
- name: "get list of resources"
  aws_lex_runtime_info:
    get_session: true
    bot_name: 'test'
    bot_alias: 'test'
    user_id: 'test'
"""

RETURN = """
session:
  description: get session.
  returned: when `get_session` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _lex_runtime(client, module):
    try:
        if module.params['get_session']:
            return client.get_session(
                botName=module.params['bot_name'],
                botAlias=module.params['bot_alias'],
                userId=module.params['user_id'],
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon lex_runtime details')


def main():
    argument_spec = dict(
        bot_name=dict(required=False),
        bot_alias=dict(required=False),
        user_id=dict(required=False),
        get_session=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_session', True, ['bot_name', 'bot_alias', 'user_id']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('lex-runtime', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _lex_runtime(client, module)

    if module.params['get_session']:
        module.exit_json(session=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
