#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_kinesisanalyticsv2_info
short_description: Get Information about Amazon Kinesis Analytics V2.
description:
  - Get Information about Amazon Kinesis Analytics V2.
  - U(https://docs.aws.amazon.com/kinesisanalytics/latest/apiv2/API_Operations.html)
version_added: 0.0.7
options:
  name:
    description:
      - name of application.
    required: false
    type: bool
  list_applications:
    description:
      - do you want to get list of applications?
    required: false
    type: bool
  list_application_snapshots:
    description:
      - do you want to get list of  snapshots for given application I(name)?
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
- name: "get list of applications"
  aws_kinesisanalyticsv2_info:
    list_applications: true

- name: "get list of applications snapshots"
  aws_kinesisanalyticsv2_info:
    list_application_snapshots: true
    name: 'test-application'
"""

RETURN = """
applications:
  description: list of applications.
  returned: when `list_applications` is defined and success.
  type: list
application_snapshots:
  description: list of application snapshots.
  returned: when `list_application_snapshots` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _kinesisanalyticsv2(client, module):
    try:
        if module.params['list_applications']:
            if client.can_paginate('list_applications'):
                paginator = client.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return client.list_applications(), False
        elif module.params['list_application_snapshots']:
            if client.can_paginate('list_application_snapshots'):
                paginator = client.get_paginator('list_application_snapshots')
                return paginator.paginate(
                    ApplicationName=module.params['name']
                ), True
            else:
                return client.list_application_snapshots(
                    ApplicationName=module.params['name']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Kinesis Analytics V2 details')


def main():
    argument_spec = dict(
        name=dict(required=False),
        list_applications=dict(required=False, type=bool),
        list_application_snapshots=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_application_snapshots', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_applications',
                'list_application_snapshots',
            )
        ],
    )

    client = module.client('kinesisanalyticsv2', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _kinesisanalyticsv2(client, module)

    if module.params['list_applications']:
        module.exit_json(applications=aws_response_list_parser(paginate, it, 'ApplicationSummaries'))
    elif module.params['list_application_snapshots']:
        module.exit_json(application_snapshots=aws_response_list_parser(paginate, it, 'SnapshotSummaries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
