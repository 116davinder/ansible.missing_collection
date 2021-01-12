#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_appflow_info
short_description: Get details about AWS AppFlow Service.
description:
  - Get Information about AWS AppFlow Service.
  - U(https://docs.aws.amazon.com/appflow/1.0/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  name:
    description:
      - name of aws appflow.
    required: false
    type: str
    aliases: ['flow_name']
  describe_flow:
    description:
      - do you want to describe aws appflow for given I(name).
      - U(https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeFlow.html)
    required: false
    type: bool
  describe_connectors:
    description:
      - do you want to describe aws appflow connector for given list of I(describe_connector_types).
      - U(https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html)
    required: false
    type: bool
  describe_connector_types:
    description:
      - list of type of appflow connectors.
      - U(https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html)
    required: false
    type: list
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
- name: "list aws app flows"
  aws_appflow_info:

- name: "describe aws app flow name"
  aws_appflow_info:
    name: 'test'
    describe_flow: true

- name: "describe aws app flow connector"
  aws_appflow_info:
    describe_connectors: true
    describe_connector_types: ['S3']
"""

RETURN = """
flows:
  description: List of aws appflows.
  returned: when no arguments and success
  type: list
  sample: [
    {
        "created_at": "2020-12-26T18:52:43.076000+02:00",
        "created_by": "arn:aws:iam::xxxx:user/xxxx",
        "description": "test flow",
        "destination_connector_type": "S3",
        "flow_arn": "arn:aws:appflow:us-east-1:xxxxxxxx:flow/test",
        "flow_name": "test",
        "flow_status": "Active",
        "last_updated_at": "2020-12-26T18:52:43.076000+02:00",
        "last_updated_by": "arn:aws:iam::xxxxxxxxxx:user/xxxxx",
        "source_connector_type": "S3",
        "tags": {},
        "trigger_type": "OnDemand"
    }
  ]
flow:
  description: Information about given flow name.
  returned: when `flow_name` is defined and `describe_flow=true` and success
  type: dict
  sample: {
    "created_at": "2020-12-26T18:52:43.076000+02:00",
    "created_by": "arn:aws:iam::xxxxxxxxxxx:user/xxxxxxxxxxxx",
    "description": "test flow",
    "destination_flow_config_list": [
        {
            "connector_type": "S3",
            "destination_connector_properties": {
                "s3": {
                    "bucket_name": "test-bucket-s3",
                    "s3_output_format_config": {
                        "aggregation_config": {
                            "aggregation_type": "None"
                        },
                        "file_type": "JSON",
                        "prefix_config": {}
                    }
                }
            }
        }
    ],
    "flow_arn": "arn:aws:appflow:us-east-1:xxxxxxxxxxxx:flow/test",
    "flow_name": "test",
    "flow_status": "Active",
    "kms_arn": "arn:aws:kms:us-east-1:xxxxxxxxxxx:key/xxxxxxxxxxx-a32c-59fe2257d2b4",
    "last_updated_at": "2020-12-26T18:52:43.076000+02:00",
    "last_updated_by": "arn:aws:iam::xxxxxxxxxxx:user/xxxxxxxxxxx",
    "response_metadata": {
        "http_headers": {
            "connection": "keep-alive",
            "content-length": "3157",
            "content-type": "application/json",
            "date": "Sat, 26 Dec 2020 16:55:16 GMT",
            "x-amz-apigw-id": "YK2xxxxxxxxxxxxxxFVMw=",
            "x-amzn-requestid": "xxxxxxxxxxxxx-86f9-ceb6cfe1ce41",
            "x-amzn-trace-id": "Root=1-xxxxxxxxxxxxxxxd30a371c2a38"
        },
        "http_status_code": 200,
        "request_id": "769ebe3d-4407-45a4-86f9-ceb6cfe1ce41",
        "retry_attempts": 0
    },
    "source_flow_config": {
        "connector_type": "S3",
        "source_connector_properties": {
            "s3": {
                "bucket_name": "test-s3-bucket",
                "bucket_prefix": "sample"
            }
        }
    },
    "tags": {},
    "tasks": [
        {
            "connector_operator": {
                "s3": "PROJECTION"
            },
            "source_fields": [
                "{  "
            ],
            "task_properties": {},
            "task_type": "Filter"
        },
        {
            "connector_operator": {
                "s3": "NO_OP"
            },
            "destination_field": "{  ",
            "source_fields": [
                "{  "
            ],
            "task_properties": {},
            "task_type": "Map"
        }
    ],
    "trigger_config": {
        "trigger_properties": {},
        "trigger_type": "OnDemand"
    }
  }
connector_configurations:
  description: Information about given appflow connector configurations.
  returned: when `describe_connectors` and `describe_connector_types` are defined and success
  type: dict
  sample: {
    "s3": {
        "can_use_as_destination": true,
        "can_use_as_source": true,
        "connector_metadata": {
            "s3": {}
        },
        "is_private_link_enabled": false,
        "is_private_link_endpoint_url_required": false,
        "supported_destination_connectors": [
            "Salesforce",
            "Snowflake",
            "Redshift",
            "S3"
        ],
        "supported_scheduling_frequencies": [
            "BYMINUTE",
            "HOURLY",
            "DAILY",
            "WEEKLY",
            "MONTHLY",
            "ONCE"
        ],
        "supported_trigger_types": [
            "Scheduled",
            "OnDemand"
        ]
    }
  }
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _appflow(client, module):
    try:
        if module.params['describe_flow']:
            if client.can_paginate('describe_flow'):
                paginator = client.get_paginator('describe_flow')
                return paginator.paginate(
                    flowName=module.params['name']
                ), True
            else:
                return client.describe_flow(
                    flowName=module.params['name']
                ), False
        elif module.params['describe_connectors']:
            if client.can_paginate('describe_connectors'):
                paginator = client.get_paginator('describe_connectors')
                return paginator.paginate(
                    connectorTypes=module.params['describe_connector_types']
                ), True
            else:
                return client.describe_connectors(
                    connectorTypes=module.params['describe_connector_types']
                ), False
        else:
            if client.can_paginate('list_flows'):
                paginator = client.get_paginator('list_flows')
                return paginator.paginate(
                    maxResults=100          # default value is not set, minor bug in boto3
                ), True
            else:
                return client.list_flows(
                    maxResults=100          # default value is not set, minor bug in boto3
                ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws appflow details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['flow_name']),
        describe_flow=dict(required=False, type=bool),
        describe_connectors=dict(required=False, type=bool),
        describe_connector_types=dict(required=False, type=list)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_flow', True, ['name']),
            ('describe_connectors', True, ['describe_connector_types'])
        ],
        mutually_exclusive=[
            ('describe_flow', 'describe_connectors'),
        ],
    )

    appflow = module.client('appflow', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _appflow(appflow, module)

    if module.params['describe_flow']:
        module.exit_json(flow=camel_dict_to_snake_dict(_it))
    elif module.params['describe_connectors']:
        module.exit_json(connector_configurations=camel_dict_to_snake_dict(_it['connectorConfigurations']))
    else:
        module.exit_json(flows=aws_response_list_parser(paginate, _it, 'flows'))


if __name__ == '__main__':
    main()
