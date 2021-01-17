#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_datasync_info
short_description: Get Information about AWS DataSync.
description:
  - Get Information about AWS DataSync.
  - U(https://docs.aws.amazon.com/datasync/latest/userguide/API_Operations.html)
version_added: 0.0.5
options:
  task_arn:
    description:
      -  arn of datasync task.
    required: false
    type: str
  agent:
    description:
      -  arn of datasync agent.
    required: false
    type: str
  list_agents:
    description:
      - do you want to get list of data sync agents?
    required: false
    type: bool
  list_locations:
    description:
      - do you want to get list of data sync locations?
    required: false
    type: bool
  list_task_executions:
    description:
      - do you want to get list of data sync task executions for given I(task_arn)?
    required: false
    type: bool
  list_tasks:
    description:
      - do you want to get list of data sync tasks?
    required: false
    type: bool
  describe_task:
    description:
      - do you want to get details data sync task for given I(task_arn)?
    required: false
    type: bool
  describe_agent:
    description:
      - do you want to get details data sync agent for given I(agent_arn)?
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
- name: "list of datasync agents"
  aws_datasync_info:
    list_agents: true

- name: "list of datasync locations"
  aws_datasync_info:
    list_locations: true

- name: "list of datasync task executions"
  aws_datasync_info:
    list_task_executions: true
    task_arn: 'test-arn'

- name: "list of datasync tasks"
  aws_datasync_info:
    list_tasks: true

- name: "describe datasync task"
  aws_datasync_info:
    describe_task: true
    task_arn: 'test-arn'

- name: "describe datasync agent"
  aws_datasync_info:
    describe_agent: true
    agent_arn: 'test-arn'
"""

RETURN = """
agents:
  description: Lists all of the data sync agents.
  returned: when `list_agents` is defined and success
  type: list
  sample: [
    {
        'agent_arn': 'string',
        'name': 'string',
        'status': 'ONLINE'
    },
  ]
locations:
  description: Lists all of the data sync locations.
  returned: when `list_locations` is defined and success
  type: list
  sample: [
    {
        'location_arn': 'string',
        'location_uri': 'string'
    },
  ]
task_executions:
  description: Lists of the data sync task executions.
  returned: when `list_task_executions`, and `task_arn` are defined and success
  type: list
  sample: [
    {
        'task_execution_arn': 'string',
        'status': 'QUEUED'
    },
  ]
tasks:
  description: Lists all of the data sync tasks.
  returned: when `list_tasks` is defined and success
  type: list
  sample: [
    {
        'task_arn': 'string',
        'status': 'AVAILABLE',
        'name': 'string'
    },
  ]
task:
  description: describe data sync task.
  returned: when `describe_task`, and `task_arn` are defined and success
  type: dict
  sample: {
    'task_arn': 'string',
    'status': 'AVAILABLE',
    'name': 'string',
    'current_task_execution_arn': 'string',
    'source_location_arn': 'string',
    'destination_location_arn': 'string',
    'cloud_watch_log_group_arn': 'string',
    'source_network_interface_arns': [],
    'destination_network_interface_arns': [],
    'options': {},
    'excludes': [],
    'schedule': {},
    'error_code': 'string',
    'error_detail': 'string',
    'creation_time': datetime(2015, 1, 1)
  }
agent:
  description: describe data sync agent.
  returned: when `describe_agent`, and `agent_arn` are defined and success
  type: dict
  sample: {
    'agent_arn': 'string',
    'name': 'string',
    'status': 'ONLINE',
    'last_connection_time': datetime(2016, 6, 6),
    'creation_time': datetime(2015, 1, 1),
    'endpoint_type': 'PUBLIC',
    'private_link_config': {
        'vpc_endpoint_id': 'string',
        'private_link_endpoint': 'string',
        'subnet_arns': [
            'string',
        ],
        'security_group_arns': [
            'string',
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
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _datasync(client, module):
    try:
        if module.params['list_agents']:
            if client.can_paginate('list_agents'):
                paginator = client.get_paginator('list_agents')
                return paginator.paginate(), True
            else:
                return client.list_agents(), False
        elif module.params['list_locations']:
            if client.can_paginate('list_locations'):
                paginator = client.get_paginator('list_locations')
                return paginator.paginate(), True
            else:
                return client.list_locations(), False
        elif module.params['list_task_executions']:
            if client.can_paginate('list_task_executions'):
                paginator = client.get_paginator('list_task_executions')
                return paginator.paginate(
                    TaskArn=module.params['task_arn'],
                ), True
            else:
                return client.list_task_executions(
                    TaskArn=module.params['task_arn'],
                ), False
        elif module.params['list_tasks']:
            if client.can_paginate('list_tasks'):
                paginator = client.get_paginator('list_tasks')
                return paginator.paginate(), True
            else:
                return client.list_tasks(), False
        elif module.params['describe_task']:
            return client.describe_task(
                TaskArn=module.params['task_arn'],
            ), False
        elif module.params['describe_agent']:
            return client.describe_agent(
                AgentArn=module.params['agent_arn'],
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Data Sync details')


def main():
    argument_spec = dict(
        task_arn=dict(required=False),
        agent_arn=dict(required=False),
        list_agents=dict(required=False, type=bool),
        list_locations=dict(required=False, type=bool),
        list_task_executions=dict(required=False, type=bool),
        list_tasks=dict(required=False, type=bool),
        describe_task=dict(required=False, type=bool),
        describe_agent=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_task_executions', True, ['task_arn']),
            ('describe_task', True, ['task_arn']),
            ('describe_agent', True, ['agent_arn']),
        ),
        mutually_exclusive=[
            (
                'list_agents',
                'list_locations',
                'list_task_executions',
                'list_tasks',
                'describe_task',
                'describe_agent',
            )
        ],
    )

    client = module.client('datasync', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _datasync(client, module)

    if module.params['list_agents']:
        module.exit_json(agents=aws_response_list_parser(paginate, _it, 'Agents'))
    elif module.params['list_locations']:
        module.exit_json(locations=aws_response_list_parser(paginate, _it, 'Locations'))
    elif module.params['list_task_executions']:
        module.exit_json(task_executions=aws_response_list_parser(paginate, _it, 'TaskExecutions'))
    elif module.params['list_tasks']:
        module.exit_json(tasks=aws_response_list_parser(paginate, _it, 'Tasks'))
    elif module.params['describe_task']:
        module.exit_json(task=camel_dict_to_snake_dict(_it))
    elif module.params['describe_agent']:
        module.exit_json(agent=camel_dict_to_snake_dict(_it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
