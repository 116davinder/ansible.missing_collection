#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_pinpoint_email_info
short_description: Get Information about Amazon Pinpoint Email.
description:
  - Get Information about Amazon Pinpoint Email.
  - U(https://docs.aws.amazon.com/pinpoint-email/latest/APIReference/API_Operations.html)
version_added: 0.0.8
options:
  list_configuration_sets:
    description:
      - do you want to get configuration_sets?
    required: false
    type: bool
  list_dedicated_ip_pools:
    description:
      - do you want to get dedicated_ip_pools?
    required: false
    type: bool
  list_deliverability_test_reports:
    description:
      - do you want to get deliverability_test_reports?
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
- name: "get configuration_sets"
  aws_pinpoint_email_info:
    list_configuration_sets: true

- name: "get dedicated_ip_pools"
  aws_pinpoint_email_info:
    list_dedicated_ip_pools: true

- name: "get deliverability_test_reports"
  aws_pinpoint_email_info:
    list_deliverability_test_reports: true
"""

RETURN = """
configuration_sets:
  description: list of configuration_sets.
  returned: when `list_configuration_sets` is defined and success.
  type: list
dedicated_ip_pools:
  description: get of dedicated_ip_pools.
  returned: when `list_dedicated_ip_pools` is defined and success.
  type: list
deliverability_test_reports:
  description: list of deliverability_test_reports.
  returned: when `list_deliverability_test_reports` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _pinpoint_email(client, module):
    try:
        if module.params['list_configuration_sets']:
            if client.can_paginate('list_configuration_sets'):
                if client.can_paginate('list_configuration_sets'):
                    paginator = client.get_paginator('list_configuration_sets')
                    return paginator.paginate(), True
                else:
                    return client.list_configuration_sets(), False
        elif module.params['list_dedicated_ip_pools']:
            if client.can_paginate('list_dedicated_ip_pools'):
                paginator = client.get_paginator('list_dedicated_ip_pools')
                return paginator.paginate(), True
            else:
                return client.list_dedicated_ip_pools(), False
        elif module.params['list_deliverability_test_reports']:
            if client.can_paginate('list_deliverability_test_reports'):
                paginator = client.get_paginator('list_deliverability_test_reports')
                return paginator.paginate(), True
            else:
                return client.list_deliverability_test_reports(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Pinpoint Email details')


def main():
    argument_spec = dict(
        list_configuration_sets=dict(required=False, type=bool),
        list_dedicated_ip_pools=dict(required=False, type=bool),
        list_deliverability_test_reports=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_configuration_sets',
                'list_dedicated_ip_pools',
                'list_deliverability_test_reports',
            )
        ],
    )

    client = module.client('pinpoint-email', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _pinpoint_email(client, module)

    if module.params['list_configuration_sets']:
        module.exit_json(configuration_sets=aws_response_list_parser(paginate, it, 'ConfigurationSets'))
    elif module.params['list_dedicated_ip_pools']:
        module.exit_json(dedicated_ip_pools=aws_response_list_parser(paginate, it, 'DedicatedIpPools'))
    elif module.params['list_deliverability_test_reports']:
        module.exit_json(deliverability_test_reports=aws_response_list_parser(paginate, it, 'DeliverabilityTestReports'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
