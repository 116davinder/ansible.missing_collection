#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_secretsmanager_info
short_description: Get Information about AWS Secrets Manager.
description:
  - Get Information about AWS Secrets Manager.
  - U(https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_Operations.html)
version_added: 0.0.9
options:
  describe_secret:
    description:
      - do you want to get details of secret for given I(id)?
    required: false
    type: bool
  list_secrets:
    description:
      - do you want to get of secrets?
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
- name: "get details of secret"
  aws_secretsmanager_info:
    describe_secret: true
    id: 'secret_id'

- name: "get list of secrets"
  aws_secretsmanager_info:
    list_secrets: true
"""

RETURN = """
secret:
  description: details of secret.
  returned: when `describe_secret` is defined and success.
  type: dict
secrets:
  description: get of secrets.
  returned: when `list_secrets` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _secretsmanager(client, module):
    try:
        if module.params['describe_secret']:
            if client.can_paginate('describe_secret'):
                paginator = client.get_paginator('describe_secret')
                return paginator.paginate(
                    SecretId=module.params['id']
                ), True
            else:
                return client.describe_secret(
                    SecretId=module.params['id']
                ), False
        elif module.params['list_secrets']:
            if client.can_paginate('list_secrets'):
                paginator = client.get_paginator('list_secrets')
                return paginator.paginate(), True
            else:
                return client.list_secrets(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Secrets Manager details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['secret_id']),
        describe_secret=dict(required=False, type=bool),
        list_secrets=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_secret', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_secret',
                'list_secrets',
            )
        ],
    )

    client = module.client('secretsmanager', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _secretsmanager(client, module)

    if module.params['describe_secret']:
        module.exit_json(secret=camel_dict_to_snake_dict(it))
    elif module.params['list_secrets']:
        module.exit_json(secrets=aws_response_list_parser(paginate, it, 'SecretList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
