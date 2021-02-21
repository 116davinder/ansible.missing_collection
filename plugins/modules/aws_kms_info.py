#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kms_info
short_description: Get Information about AWS KMS.
description:
  - Get Information about AWS KMS.
  - U(https://docs.aws.amazon.com/kms/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  id:
    description:
      - id of key.
    required: false
    type: str
    aliases: ['key_id']
  retiring_principal:
    description:
      - id of retiring principal for grants.
    required: false
    type: str
  list_aliases:
    description:
      - do you want to get list of aliases?
    required: false
    type: bool
  list_grants:
    description:
      - do you want to get list of grants for given key I(id)?
    required: false
    type: bool
  list_key_policies:
    description:
      - do you want to get list of key policies for given key I(id)?
    required: false
    type: bool
  list_keys:
    description:
      - do you want to get list of keys?
    required: false
    type: bool
  list_retirable_grants:
    description:
      - do you want to get list of retirable_grants for given I(retiring_principal)?
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
- name: "get list of aliases"
  aws_kms_info:
    list_aliases: true

- name: "get list of grants"
  aws_kms_info:
    list_grants: true
    id: 'key_id'

- name: "get list of key_policies"
  aws_kms_info:
    list_key_policies: true
    id: 'key-id'

- name: "get list of keys"
  aws_kms_info:
    list_keys: true

- name: "get list of retirable_grants"
  aws_kms_info:
    list_retirable_grants: true
    retiring_principal: 'test-retiring-principal'
"""

RETURN = """
aliases:
  description: list of aliases.
  returned: when `list_aliases` is defined and success.
  type: list
grants:
  description: list of grants.
  returned: when `list_grants` or `list_retirable_grants` is defined and success.
  type: list
key_policies:
  description: list of key_policies.
  returned: when `list_key_policies` is defined and success.
  type: list
keys:
  description: list of keys.
  returned: when `list_keys` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kms(client, module):
    try:
        if module.params['list_aliases']:
            if client.can_paginate('list_aliases'):
                paginator = client.get_paginator('list_aliases')
                return paginator.paginate(), True
            else:
                return client.list_aliases(), False
        elif module.params['list_grants']:
            if client.can_paginate('list_grants'):
                paginator = client.get_paginator('list_grants')
                return paginator.paginate(
                    KeyId=module.params['id'],
                ), True
            else:
                return client.list_grants(
                    KeyId=module.params['id'],
                ), False
        elif module.params['list_key_policies']:
            if client.can_paginate('list_key_policies'):
                paginator = client.get_paginator('list_key_policies')
                return paginator.paginate(
                    KeyId=module.params['id'],
                ), True
            else:
                return client.list_key_policies(
                    KeyId=module.params['id'],
                ), False
        elif module.params['list_keys']:
            if client.can_paginate('list_keys'):
                paginator = client.get_paginator('list_keys')
                return paginator.paginate(), True
            else:
                return client.list_keys(), False
        elif module.params['list_retirable_grants']:
            if client.can_paginate('list_retirable_grants'):
                paginator = client.get_paginator('list_retirable_grants')
                return paginator.paginate(
                    RetiringPrincipal=module.params['retiring_principal'],
                ), True
            else:
                return client.list_retirable_grants(
                    RetiringPrincipal=module.params['retiring_principal'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon kms details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['key_id']),
        retiring_principal=dict(required=False),
        list_aliases=dict(required=False, type=bool),
        list_grants=dict(required=False, type=bool),
        list_key_policies=dict(required=False, type=bool),
        list_keys=dict(required=False, type=bool),
        list_retirable_grants=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_grants', True, ['id']),
            ('list_key_policies', True, ['id']),
            ('list_retirable_grants', True, ['retiring_principal']),
        ),
        mutually_exclusive=[
            (
                'list_aliases',
                'list_grants',
                'list_key_policies',
                'list_keys',
                'list_retirable_grants',
            )
        ],
    )

    client = module.client('kms', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kms(client, module)

    if module.params['list_aliases']:
        module.exit_json(aliases=aws_response_list_parser(paginate, it, 'Aliases'))
    elif module.params['list_grants'] or module.params['list_retirable_grants']:
        module.exit_json(grants=aws_response_list_parser(paginate, it, 'Grants'))
    elif module.params['list_key_policies']:
        module.exit_json(key_policies=aws_response_list_parser(paginate, it, 'PolicyNames'))
    elif module.params['list_keys']:
        module.exit_json(keys=aws_response_list_parser(paginate, it, 'Keys'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
