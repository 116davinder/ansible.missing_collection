#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: aws_lexv2_runtime_info
short_description: Get Information about Amazon Lex Runtime Service (V2).
description:
  - Get Information about Amazon Lex Runtime Service (V2).
  - U(https://docs.aws.amazon.com/lexv2/latest/dg/API_Operations_Amazon_Lex_Runtime_V2.html)
version_added: 0.0.7
options:
  bot_id:
    description:
      - id of bot.
    required: false
    type: str
  bot_alias_id:
    description:
      - id of bot alias.
    required: false
    type: str
  locale_id:
    description:
      - The locale where the session is in use.
    required: false
    type: str
  session_id:
    description:
      - id of session.
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
- name: "get session details"
  aws_lexv2_runtime_info:
    get_session: true
    bot_id: 'test'
    bot_alias_id: 'test'
    locale_id: 'test'
    session_id: 'test'
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
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _lexv2_runtime(client, module):
    try:
        if module.params["get_session"]:
            return (
                client.get_session(
                    botId=module.params["bot_id"],
                    botAliasId=module.params["bot_alias_id"],
                    localeId=module.params["locale_id"],
                    sessionId=module.params["session_id"],
                ),
                False,
            )
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg="Failed to fetch Amazon lexv2_runtime details")


def main():
    argument_spec = dict(
        bot_id=dict(required=False),
        bot_alias_id=dict(required=False),
        locale_id=dict(required=False),
        session_id=dict(required=False),
        get_session=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            (
                "get_session",
                True,
                ["bot_id", "bot_alias_id", "locale_id", "session_id"],
            ),
        ),
        mutually_exclusive=[],
    )

    client = module.client(
        "lexv2-runtime", retry_decorator=AWSRetry.exponential_backoff()
    )
    it, _ = _lexv2_runtime(client, module)

    if module.params["get_session"]:
        module.exit_json(session=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == "__main__":
    main()
