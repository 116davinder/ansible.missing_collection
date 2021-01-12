#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_connections_info
short_description: Get Information about AWS CodePipeline.
description:
  - Get Information about AWS CodePipeline.
  - U(https://docs.aws.amazon.com/codepipeline/latest/APIReference/API_Operations.html)
version_added: 0.0.4
options:
  name:
    description:
      - name of the code pipeline.
    required: false
    type: str
  list_action_executions:
    description:
      - do you want to get list of execution actions details about given I(name)?
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
"""

RETURN = """
pipelines:
  description: get list of code pipelines.
  returned: when no argument and success
  type: list
  sample: [
    {
        'name': 'string',
        'version': 123,
        'created': datetime(2015, 1, 1),
        'updated': datetime(2016, 6, 6)
    },
  ]
pipeline:
  description: get detail about given pipeline name.
  returned: when `get_pipeline` is defined and success
  type: dict
  sample: {
    'name': 'string',
    'role_arn': 'string',
    'artifact_store': {},
    'artifact_stores': {},
    'stages': [],
    'version': 123
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
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _codestar(client, module):
    try:
        if module.params['list_connections']:
            if client.can_paginate('list_connections'):
                paginator = client.get_paginator('list_connections')
                return paginator.paginate(
                    ProviderTypeFilter=module.params['provider_type_filter']
                ), True
            else:
                return client.list_connections(
                    ProviderTypeFilter=module.params['provider_type_filter']
                ), False
        elif module.params['list_hosts']:
            if client.can_paginate('list_hosts'):
                paginator = client.get_paginator('list_hosts')
                return paginator.paginate(), True
            else:
                return client.list_hosts(), False
        elif module.params['get_connection']:
            return client.get_connection(
                ConnectionArn=module.params['arn']
            ), False
        elif module.params['get_host']:
            return client.get_host(
                HostArn=module.params['arn']
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codestar connections details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        provider_type_filter=dict(required=False, choices=['Bitbucket', 'GitHub', 'GitHubEnterpriseServer'], default='Bitbucket'),
        list_connections=dict(required=False, type=bool),
        list_hosts=dict(required=False, type=bool),
        get_connection=dict(required=False, type=bool),
        get_host=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_connection', True, ['arn']),
            ('get_host', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_connections',
                'list_hosts',
                'get_connection',
                'get_host',
            )
        ],
    )

    client = module.client('codestar-connections', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codestar(client, module)

    if module.params['list_connections']:
        module.exit_json(connections=aws_response_list_parser(paginate, _it, 'Connections'))
    elif module.params['list_hosts']:
        module.exit_json(hosts=aws_response_list_parser(paginate, _it, 'Hosts'))
    elif module.params['get_connection']:
        module.exit_json(connection=camel_dict_to_snake_dict(_it['Connection']))
    elif module.params['get_host']:
        module.exit_json(host=camel_dict_to_snake_dict(_it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
