#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_opsworkscm_info
short_description: Get Information about AWS OpsWorks CM (OpsWorksCM).
description:
  - Get Information about AWS OpsWorks CM (OpsWorksCM).
  - U(https://docs.aws.amazon.com/opsworks-cm/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  describe_account_attributes:
    description:
      - do you want to get list of account_attributes?
    required: false
    type: bool
  describe_backups:
    description:
      - do you want to get backups?
    required: false
    type: bool
  describe_servers:
    description:
      - do you want to get list of servers?
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
- name: "get list of account_attributes"
  aws_opsworkscm_info:
    describe_account_attributes: true

- name: "get backups"
  aws_opsworkscm_info:
    describe_backups: true

- name: "get list of servers"
  aws_opsworkscm_info:
    describe_servers: true
"""

RETURN = """
account_attributes:
  description: list of account_attributes.
  returned: when `describe_account_attributes` is defined and success.
  type: list
backups:
  description: get of backups.
  returned: when `describe_backups` is defined and success.
  type: list
servers:
  description: list of servers.
  returned: when `describe_servers` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _opsworkscm(client, module):
    try:
        if module.params['describe_account_attributes']:
            if client.can_paginate('describe_account_attributes'):
                paginator = client.get_paginator('describe_account_attributes')
                return paginator.paginate(), True
            else:
                return client.describe_account_attributes(), False
        elif module.params['describe_backups']:
            if client.can_paginate('describe_backups'):
                paginator = client.get_paginator('describe_backups')
                return paginator.paginate(), True
            else:
                return client.describe_backups(), False
        elif module.params['describe_servers']:
            if client.can_paginate('describe_servers'):
                paginator = client.get_paginator('describe_servers')
                return paginator.paginate(), True
            else:
                return client.describe_servers(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS OpsWorks CM (OpsWorksCM) details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['stack_id']),
        describe_account_attributes=dict(required=False, type=bool),
        describe_backups=dict(required=False, type=bool),
        describe_servers=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'describe_account_attributes',
                'describe_backups',
                'describe_servers',
            )
        ],
    )

    client = module.client('opsworkscm', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _opsworkscm(client, module)

    if module.params['describe_account_attributes']:
        module.exit_json(account_attributes=aws_response_list_parser(paginate, it, 'Attributes'))
    elif module.params['describe_backups']:
        module.exit_json(backups=aws_response_list_parser(paginate, it, 'Backups'))
    elif module.params['describe_servers']:
        module.exit_json(servers=aws_response_list_parser(paginate, it, 'Servers'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
