#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_swf_info
short_description: Get Information about Amazon Simple Workflow Service (SWF).
description:
  - Get Information about Amazon Simple Workflow Service (SWF).
  - U(https://docs.aws.amazon.com/swf/latest/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  domain:
    description:
      - name of domain.
    required: false
    type: str
  registration_status:
    description:
      - registration status of workflow.
    required: false
    type: str
    choices: ['REGISTERED', 'DEPRECATED']
    default: 'REGISTERED'
  list_activity_types:
    description:
      - do you want to get list of activity_types for given I(domain) and I(registration_status)?
    required: false
    type: bool
  list_domains:
    description:
      - do you want to get domains for given I(registration_status)?
    required: false
    type: bool
  list_workflow_types:
    description:
      - do you want to get list of workflow_types for given I(domain) and I(registration_status)?
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
- name: "get list of activity_types"
  aws_swf_info:
    list_activity_types: true
    domain: 'domain_name'
    registration_status: 'REGISTERED'

- name: "get domains"
  aws_swf_info:
    list_domains: true
    registration_status: 'REGISTERED'

- name: "get list of workflow_types"
  aws_swf_info:
    list_workflow_types: true
    domain: 'domain_name'
    registration_status: 'REGISTERED'
"""

RETURN = """
activity_types:
  description: list of activity_types.
  returned: when `list_activity_types` is defined and success.
  type: list
domains:
  description: get of domains.
  returned: when `list_domains` is defined and success.
  type: list
workflow_types:
  description: list of workflow_types.
  returned: when `list_workflow_types` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _swf(client, module):
    try:
        if module.params['list_activity_types']:
            if client.can_paginate('list_activity_types'):
                paginator = client.get_paginator('list_activity_types')
                return paginator.paginate(
                    domain=module.params['domain'],
                    registrationStatus=module.params['registration_status'],
                ), True
            else:
                return client.list_activity_types(
                    domain=module.params['domain'],
                    registrationStatus=module.params['registration_status'],
                ), False
        elif module.params['list_domains']:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(
                    registrationStatus=module.params['registration_status'],
                ), True
            else:
                return client.list_domains(
                    registrationStatus=module.params['registration_status'],
                ), False
        elif module.params['list_workflow_types']:
            if client.can_paginate('list_workflow_types'):
                paginator = client.get_paginator('list_workflow_types')
                return paginator.paginate(
                    domain=module.params['domain'],
                    registrationStatus=module.params['registration_status'],
                ), True
            else:
                return client.list_workflow_types(
                    domain=module.params['domain'],
                    registrationStatus=module.params['registration_status'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Simple Workflow Service (SWF) details')


def main():
    argument_spec = dict(
        domain=dict(required=False),
        registration_status=dict(required=False, choices=['REGISTERED', 'DEPRECATED'], default='REGISTERED'),
        list_activity_types=dict(required=False, type=bool),
        list_domains=dict(required=False, type=bool),
        list_workflow_types=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_activity_types', True, ['domain']),
            ('list_workflow_types', True, ['domain']),
        ),
        mutually_exclusive=[
            (
                'list_activity_types',
                'list_domains',
                'list_workflow_types',
            )
        ],
    )

    client = module.client('swf', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _swf(client, module)

    if module.params['list_activity_types']:
        module.exit_json(activity_types=aws_response_list_parser(paginate, it, 'typeInfos'))
    elif module.params['list_domains']:
        module.exit_json(domains=aws_response_list_parser(paginate, it, 'domainInfos'))
    elif module.params['list_workflow_types']:
        module.exit_json(workflow_types=aws_response_list_parser(paginate, it, 'typeInfos'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
