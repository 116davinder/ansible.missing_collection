#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_api_gateway_v2_info
short_description: Get details about AWS API Gateway V2 Service.
description:
  - Get Information about AWS API Gateway V2 Service.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigatewayv2.html)
version_added: 0.0.2
options:
  api_id:
    description:
      - api id of api gateway v2.
    required: false
    type: str
  get_api:
    description:
      - do you want to fetch details about given I(api_id)?
    required: false
    type: bool
  get_deployments:
    description:
      - do you want to fetch deployment details about given I(api_id)?
    required: false
    type: bool
  get_stages:
    description:
      - do you want to fetch stages details about given I(api_id)?
    required: false
    type: bool
  get_routes:
    description:
      - do you want to fetch routes details about given I(api_id)?
    required: false
    type: bool
  domain_name:
    description:
      - name of the domain used in api gateway v2.
    required: false
    type: str
  get_api_mappings:
    description:
      - do you want to fetch api mappings details about given I(domain_name)?
    required: false
    type: bool
  get_vpc_links:
    description:
      - do you want to fetch vpc links details?
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
- name: "list of all api gateways"
  aws_api_gateway_v2_info:
  register: _all

- name: "get details about given api id"
  aws_api_gateway_v2_info:
    api_id: "{{ _all.apis[0].api_id }}"
    get_api: true

- name: "get deployments about given api id"
  aws_api_gateway_v2_info:
    api_id: "{{ _all.apis[0].api_id }}"
    get_deployments: true

- name: "get stages about given api id"
  aws_api_gateway_v2_info:
    api_id: "{{ _all.apis[0].api_id }}"
    get_stages: true

- name: "get routes about given api id"
  aws_api_gateway_v2_info:
    api_id: "{{ _all.apis[0].api_id }}"
    get_routes: true

- name: "get api mappings about given domain name"
  aws_api_gateway_v2_info:
    domain_name: "example.com"
    get_api_mappings: true

- name: "get all vpc links"
  aws_api_gateway_v2_info:
    get_vpc_links: true
"""

RETURN = """
apis:
  description: List of apis.
  returned: when no argument and success
  type: list
  sample: [
    {
        "api_endpoint": "https://feeajf17jg.execute-api.us-east-1.amazonaws.com",
        "api_id": "feeajf17jg",
        "api_key_selection_expression": "$request.header.x-api-key",
        "created_date": "2020-12-25T12:55:45+00:00",
        "disable_execute_api_endpoint": false,
        "name": "test-api",
        "protocol_type": "HTTP",
        "route_selection_expression": "$request.method $request.path",
        "tags": {}
    }
  ]
api:
  description: details about given api id.
  returned: when `get_api=true` and `api_id` is defined and success
  type: dict
  sample: {
    "api_endpoint": "https://feeajf17jg.execute-api.us-east-1.amazonaws.com",
    "api_id": "feeajf17jg",
    "api_key_selection_expression": "$request.header.x-api-key",
    "created_date": "2020-12-25T12:55:45+00:00",
    "disable_execute_api_endpoint": false,
    "name": "test-api",
    "protocol_type": "HTTP",
    "response_metadata": {
        "http_headers": {
            "connection": "keep-alive",
            "content-length": "376",
            "content-type": "application/json",
            "date": "Fri, 25 Dec 2020 13:25:09 GMT",
            "x-amz-apigw-id": "YHE4aHRwoAMFc-g=",
            "x-amzn-requestid": "xxxxxxxxxx-cdc6b34b07f1",
            "x-amzn-trace-id": "Root=1-xxxxxxxxxxxx4da54a46ce7eb1"
        },
        "http_status_code": 200,
        "request_id": "xxxxxxxxxx-b6de-cdc6b34b07f1",
        "retry_attempts": 0
    },
    "route_selection_expression": "$request.method $request.path",
    "tags": {}
  }
deployments:
  description: list of deployments about given api id.
  returned: when `get_deployments=true` and `api_id` is defined and success
  type: list
  sample: [
    {
        'auto_deployed': True,
        'created_date': datetime(2015, 1, 1),
        'deployment_id': 'string',
        'deployment_status': 'DEPLOYED',
        'deployment_status_message': 'string',
        'description': 'string'
    }
  ]
stages:
  description: list of stages about given api id.
  returned: when `get_stages=true` and `api_id` is defined and success
  type: list
  sample: [
    {
        "auto_deploy": true,
        "created_date": "2020-12-25T12:55:46+00:00",
        "default_route_settings": {
            "detailed_metrics_enabled": false
        },
        "last_deployment_status_message": "Deployment attempt failed",
        "last_updated_date": "2020-12-25T13:20:09+00:00",
        "route_settings": {},
        "stage_name": "$default",
        "stage_variables": {},
        "tags": {}
    }
  ]
routes:
  description: list of routes about given api id.
  returned: when `get_routes=true` and `api_id` is defined and success
  type: list
  sample: [
    {
        "api_key_required": false,
        "authorization_type": "NONE",
        "route_id": "xxxx",
        "route_key": "ANY /"
    }
  ]
mappings:
  description: list of mappings about given domain name.
  returned: when `get_api_mappings=true` and `domain_name` is defined and success
  type: list
  sample: [
    {
        'api_id': 'string',
        'api_mapping_id': 'string',
        'api_mapping_key': 'string',
        'stage': 'string'
    }
 ]
vpc_links:
  description: list of vpc links.
  returned: when `get_vpc_links=true` and success
  type: list
  sample: [
    {
        'created_date': datetime(2015, 1, 1),
        'name': 'string',
        'security_group_ids': [
            'string',
        ],
        'subnet_ids': [
            'string',
        ],
        'tags': {
            'string': 'string'
        },
        'vpc_link_id': 'string',
        'vpc_link_status': 'AVAILABLE',
        'vpc_link_status_message': 'string',
        'vpc_link_version': 'V2'
    }
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
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _api_gateway_v2(client, module):
    try:
        if module.params['get_api']:
            return client.get_api(
                ApiId=module.params['api_id']
            ), False
        elif module.params['get_deployments']:
            if client.can_paginate('get_deployments'):
                paginator = client.get_paginator('get_deployments')
                return paginator.paginate(
                    ApiId=module.params['api_id']
                ), True
            else:
                return client.get_deployments(
                    ApiId=module.params['api_id']
                ), False
        elif module.params['get_api_mappings']:
            if client.can_paginate('get_api_mappings'):
                paginator = client.get_paginator('get_api_mappings')
                return paginator.paginate(
                    DomainName=module.params['domain_name']
                ), True
            else:
                return client.get_api_mappings(
                    DomainName=module.params['domain_name']
                ), False
        elif module.params['get_stages']:
            if client.can_paginate('get_stages'):
                paginator = client.get_paginator('get_stages')
                return paginator.paginate(
                    ApiId=module.params['api_id']
                ), True
            else:
                return client.get_stages(
                    ApiId=module.params['api_id']
                ), False
        elif module.params['get_routes']:
            if client.can_paginate('get_routes'):
                paginator = client.get_paginator('get_routes')
                return paginator.paginate(
                    ApiId=module.params['api_id']
                ), True
            else:
                return client.get_routes(
                    ApiId=module.params['api_id']
                ), False
        elif module.params['get_vpc_links']:
            if client.can_paginate('get_vpc_links'):
                paginator = client.get_paginator('get_vpc_links')
                return paginator.paginate(), True
            else:
                return client.get_vpc_links(), False
        else:
            if client.can_paginate('get_apis'):
                paginator = client.get_paginator('get_apis')
                return paginator.paginate(), True
            else:
                return client.get_apis(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws api gateway v2 details')


def main():
    argument_spec = dict(
        api_id=dict(required=False),
        get_api=dict(required=False, type=bool),
        get_deployments=dict(required=False, type=bool),
        domain_name=dict(required=False),
        get_api_mappings=dict(required=False, type=bool),
        get_stages=dict(required=False, type=bool),
        get_routes=dict(required=False, type=bool),
        get_vpc_links=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('get_api', True, ['api_id']),
            ('get_deployments', True, ['api_id']),
            ('get_stages', True, ['api_id']),
            ('get_routes', True, ['api_id']),
            ('get_api_mappings', True, ['domain_name']),
        ],
        mutually_exclusive=[
            (
                'get_api',
                'get_deployments',
                'get_api_mappings',
                'get_stages',
                'get_routes',
                'get_vpc_links'
            ),
        ],
    )

    _gateway = module.client('apigatewayv2', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _api_gateway_v2(_gateway, module)
    _return = []

    if module.params['get_api']:
        module.exit_json(api=camel_dict_to_snake_dict(_it))
    elif module.params['get_deployments']:
        module.exit_json(deployments=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['get_api_mappings']:
        module.exit_json(mappings=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['get_stages']:
        module.exit_json(stages=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['get_routes']:
        module.exit_json(routes=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['get_vpc_links']:
        module.exit_json(vpc_links=aws_response_list_parser(paginate, _it, 'Items'))
    else:
        module.exit_json(apis=aws_response_list_parser(paginate, _it, 'Items'))


if __name__ == '__main__':
    main()
