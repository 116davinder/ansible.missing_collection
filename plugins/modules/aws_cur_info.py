#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cur_info
short_description: Get Information about AWS Cost and Usage Report Service.
description:
  - Get Information about AWS Cost and Usage Report Service.
  - U(https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options: None
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
- name: "Lists the AWS Cost and Usage reports"
  aws_cur_info:
"""

RETURN = """
report_definitions:
  description: Lists the AWS Cost and Usage reports available to this account.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'report_name': 'string',
        'time_unit': 'HOURLY',
        'format': 'textORcsv',
        'compression': 'ZIP',
        'additional_schema_elements': [
            'RESOURCES',
        ],
        's3_bucket': 'string',
        's3_prefix': 'string',
        's3_region': 'af-south-1',
        'additional_artifacts': [
            'REDSHIFT',
        ],
        'refresh_closed_reports': True,
        'report_versioning': 'CREATE_NEW_REPORT'
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _cur(client, module):
    try:
        if client.can_paginate('describe_report_definitions'):
            paginator = client.get_paginator('describe_report_definitions')
            return paginator.paginate(), True
        else:
            return client.describe_report_definitions(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cur details')


def main():
    argument_spec = dict()

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[],
    )

    client = module.client('cur', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cur(client, module)

    module.exit_json(report_definitions=aws_response_list_parser(paginate, _it, 'ReportDefinitions'))


if __name__ == '__main__':
    main()
