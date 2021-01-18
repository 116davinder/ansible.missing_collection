#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_datapipeline_info
short_description: Get Information about AWS Data Pipeline.
description:
  - Get Information about AWS Data Pipeline.
  - U(https://docs.aws.amazon.com/datapipeline/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  ids:
    description:
      -  ids of the data pipelines.
    required: false
    type: list
  describe_pipelines:
    description:
      - do you want to get details about given I(ids)?
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
- name: "Lists all of the pipelines"
  aws_datapipeline_info:

- name: "describe pipelines"
  aws_datapipeline_info:
    describe_pipelines: true
    ids: ['test']
"""

RETURN = """
pipelines:
  description: list of the data pipelines.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'name': 'string'
    },
  ]
pipeline_description_list:
  description: list of description of data pipelines.
  returned: when `describe_pipelines`, and `ids` are defined and success
  type: list
  sample: [
    {
        'pipeline_id': 'string',
        'name': 'string',
        'fields': [],
        'description': 'string',
        'tags': []
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


def _datapipeline(client, module):
    try:
        if module.params['describe_pipelines']:
            if client.can_paginate('describe_pipelines'):
                paginator = client.get_paginator('describe_pipelines')
                return paginator.paginate(
                    pipelineIds=module.params['ids']
                ), True
            else:
                return client.describe_pipelines(
                    pipelineIds=module.params['ids']
                ), False
        else:
            if client.can_paginate('list_pipelines'):
                paginator = client.get_paginator('list_pipelines')
                return paginator.paginate(), True
            else:
                return client.list_pipelines(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Data Pipeline details')


def main():
    argument_spec = dict(
        ids=dict(required=False, type=list),
        describe_pipelines=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_pipelines', True, ['ids']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('datapipeline', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _datapipeline(client, module)

    if module.params['describe_pipelines']:
        module.exit_json(pipeline_description_list=aws_response_list_parser(paginate, _it, 'pipelineDescriptionList'))
    else:
        module.exit_json(pipelines=aws_response_list_parser(paginate, _it, 'pipelineIdList'))


if __name__ == '__main__':
    main()
