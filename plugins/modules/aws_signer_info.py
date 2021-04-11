#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_signer_info
short_description: Get Information about Amazon Signer.
description:
  - Get Information about Amazon Signer.
  - U(https://docs.aws.amazon.com/ses/latest/APIReference-V2/API_Operations.html)
version_added: 0.0.9
options:
  name:
    description:
      - name of the profile.
    required: false
    type: str
    aliases: ['profile_name']
  status:
    description:
      - status of the profile.
    required: false
    type: str
    choices: ['Active', 'Canceled', 'Revoked']
    default: 'Active'
  list_profile_permissions:
    description:
      - do you want to get list of profile_permissions for given I(name)?
    required: false
    type: bool
  list_signing_platforms:
    description:
      - do you want to get signing_platforms?
    required: false
    type: bool
  list_signing_profiles:
    description:
      - do you want to get list of signing_profiles for given I(status)?
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
- name: "get list of profile_permissions"
  aws_signer_info:
    list_profile_permissions: true
    name: 'profile_name'

- name: "get signing_platforms"
  aws_signer_info:
    list_signing_platforms: true

- name: "get list of signing_profiles"
  aws_signer_info:
    list_signing_profiles: true
    status: 'Active'
"""

RETURN = """
profile_permissions:
  description: list of profile_permissions.
  returned: when `list_profile_permissions` is defined and success.
  type: list
signing_platforms:
  description: list of signing_platforms.
  returned: when `list_signing_platforms` is defined and success.
  type: list
signing_profiles:
  description: list of signing_profiles.
  returned: when `list_signing_profiles` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _signer(client, module):
    try:
        if module.params['list_profile_permissions']:
            if client.can_paginate('list_profile_permissions'):
                paginator = client.get_paginator('list_profile_permissions')
                return paginator.paginate(
                    profileName=module.params['name']
                ), True
            else:
                return client.list_profile_permissions(
                    profileName=module.params['name']
                ), False
        elif module.params['list_signing_platforms']:
            if client.can_paginate('list_signing_platforms'):
                paginator = client.get_paginator('list_signing_platforms')
                return paginator.paginate(), True
            else:
                return client.list_signing_platforms(), False
        elif module.params['list_signing_profiles']:
            if client.can_paginate('list_signing_profiles'):
                paginator = client.get_paginator('list_signing_profiles')
                return paginator.paginate(
                    statuses=[module.params['status']]
                ), True
            else:
                return client.list_signing_profiles(
                    statuses=[module.params['status']]
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Signer details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['profile_name']),
        status=dict(required=False, choices=['Active', 'Canceled', 'Revoked'], default='Active'),
        list_profile_permissions=dict(required=False, type=bool),
        list_signing_platforms=dict(required=False, type=bool),
        list_signing_profiles=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_profile_permissions', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_profile_permissions',
                'list_signing_platforms',
                'list_signing_profiles',
            )
        ],
    )

    client = module.client('signer', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _signer(client, module)

    if module.params['list_profile_permissions']:
        module.exit_json(profile_permissions=aws_response_list_parser(paginate, it, 'permissions'))
    elif module.params['list_signing_platforms']:
        module.exit_json(signing_platforms=aws_response_list_parser(paginate, it, 'platforms'))
    elif module.params['list_signing_profiles']:
        module.exit_json(signing_profiles=aws_response_list_parser(paginate, it, 'profiles'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
