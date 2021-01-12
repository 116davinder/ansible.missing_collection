#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codestar_notifications_info
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
        if module.params['list_event_types']:
            if client.can_paginate('list_event_types'):
                paginator = client.get_paginator('list_event_types')
                return paginator.paginate(), True
            else:
                return client.list_event_types(), False
        elif module.params['list_targets']:
            if client.can_paginate('list_targets'):
                paginator = client.get_paginator('list_targets')
                return paginator.paginate(), True
            else:
                return client.list_targets(), False
        elif module.params['describe_notification_rule']:
            return client.describe_notification_rule(
                Arn=module.params['arn']
            ), False
        else:
            if client.can_paginate('list_notification_rules'):
                paginator = client.get_paginator('list_notification_rules')
                return paginator.paginate(), True
            else:
                return client.list_notification_rules(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codestar notifications details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        list_event_types=dict(required=False, type=bool),
        list_targets=dict(required=False, type=bool),
        describe_notification_rule=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_notification_rule', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_event_types',
                'list_targets',
                'describe_notification_rule',
            )
        ],
    )

    client = module.client('codestar-notifications', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codestar(client, module)

    if module.params['list_event_types']:
        module.exit_json(event_types=aws_response_list_parser(paginate, _it, 'EventTypes'))
    elif module.params['list_targets']:
        module.exit_json(targets=aws_response_list_parser(paginate, _it, 'Targets'))
    elif module.params['describe_notification_rule']:
        module.exit_json(rule=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(rules=aws_response_list_parser(paginate, _it, 'NotificationRules'))


if __name__ == '__main__':
    main()
