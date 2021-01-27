#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_amp_info
short_description: Get details about AWS Prometheus Service.
description:
  - Get Information about AWS Prometheus Service.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html)
version_added: 0.0.2
options:
  alias:
    description:
      - alias of AWS AMP Resource.
    required: false
    type: str
  list_workspace:
    description:
      - do you want to fetch all workspaces for given I(alias)?
    required: false
    type: bool
  workspace_id:
    description:
      - workspace id for AWS AMP Resource.
    required: false
    type: str
  describe_workspace:
    description:
      - do you want to describe workspace for given I(workspace_id).
    required: false
    type: str
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
- name: "list workspaces for given alias"
  aws_amp_info:
    alias: 'test'
    list_workspace: true
  register: _l_w

- name: "describe workspace for given workspace id"
  aws_amp_info:
    workspace_id: '{{ _l_w.workspaces[0].workspace_id }}'
    describe_workspace: true
"""

RETURN = """
workspaces:
  description: List of workspaces from given aws amp alias.
  returned: when `alias` is defined and `list_workspace=true` and success
  type: list
  sample: [
    {
        "alias": "test",
        "arn": "arn:aws:aps:us-east-1:xxxxxx:workspace/ws-xxxxxxxxx-b0c8-0ae28d089ff2",
        "created_at": "2020-12-25T03:38:59.974000+02:00",
        "status": {
            "status_code": "ACTIVE"
        },
        "workspace_id": "ws-xxxxxxxxx-b0c8-0ae28d089ff2"
    }
  ]
workspace:
  description: Information about given workspace id.
  returned: when `workspace_id` is defined and `describe_workspace=true` and success
  type: dict
  sample: {
    "alias": "test",
    "arn": "arn:aws:aps:us-east-1:xxxxxxxxx:workspace/ws-xxxxxxxxx-b0c8-0ae28d089ff2",
    "created_at": "2020-12-25T03:38:59.974000+02:00",
    "prometheus_endpoint": "https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-xxxxxxxxx-b0c8-0ae28d089ff2/",
    "status": {
        "status_code": "ACTIVE"
    },
    "workspace_id": "ws-xxxxxxxxx-b0c8-0ae28d089ff2"
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _amp(client, module):
    try:
        if client.can_paginate('list_workspaces'):
            paginator = client.get_paginator('list_workspaces')
            return paginator.paginate(
                alias=module.params['alias']
            ), True
        else:
            return client.list_workspaces(
                alias=module.params['alias']
            ), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws amp details')


def main():
    argument_spec = dict(
        alias=dict(required=False),
        list_workspace=dict(required=False, type=bool),
        workspace_id=dict(required=False),
        describe_workspace=dict(required=False, type=bool)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ('list_workspace', 'describe_workspace')
        ]
    )

    amp = module.client('amp', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _amp(amp, module)

    if module.params['list_workspace']:
        module.exit_json(workspaces=aws_response_list_parser(paginate, _it, 'workspaces'))
    elif module.params['describe_workspace']:
        try:
            _des = amp.describe_workspace(
                workspaceId=module.params['workspace_id']
            )
            module.exit_json(workspace=camel_dict_to_snake_dict(_des['workspace']))
        except amp.exceptions.ResourceNotFoundException:
            module.fail_json(msg="workspace not found")
    else:
        module.fail_json(msg="unknown options are passed")


if __name__ == '__main__':
    main()
