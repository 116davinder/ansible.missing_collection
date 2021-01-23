#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_discovery_info
short_description: (WIP) Get Information about AWS Application Discovery Service.
description:
  - Get Information about AWS Application Discovery Service.
  - U(https://docs.aws.amazon.com/application-discovery/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  ids:
    description:
      - list of ids for respective task.
    required: false
    type: list
  configuration_type:
    description:
      - type of configuration.
    required: false
    type: str
    choices: ['SERVER', 'PROCESS', 'CONNECTION', 'APPLICATION']
    default: 'SERVER'
  list_configurations:
    description:
      - do you want to get list of configuration for given I(configuration_type)?
    required: false
    type: bool
  describe_agents:
    description:
      - do you want to get list of agents?
    required: false
    type: bool
  describe_configurations:
    description:
      - do you want to Retrieves attributes for a list of configuration for I(ids)?
    required: false
    type: bool
  describe_continuous_exports:
    description:
      - do you want to Lists exports as specified for I(ids)?
    required: false
    type: bool
  describe_export_tasks:
    description:
      - do you want to Retrieve status of one or more export tasks for I(ids)?
    required: false
    type: bool
  describe_import_tasks:
    description:
      - do you want to Retrieve status of one or more import tasks for I(ids)?
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
- name: "get list of configurations."
  aws_discovery_info:
    list_configurations: true
    configuration_type: 'SERVER'

- name: "describe list of configurations."
  aws_discovery_info:
    describe_configurations: true
    ids: ['test']

- name: "get list of agents"
  aws_discovery_info:
    describe_agents: true

- name: "get list of exports."
  aws_discovery_info:
    describe_continuous_exports: true
    ids: ['test-export-id']

- name: "get list of export tasks."
  aws_discovery_info:
    describe_export_tasks: true
    ids: ['test-export-id']

- name: "get list of import tasks."
  aws_discovery_info:
    describe_import_tasks: true
"""

RETURN = """
configurations:
  description: list of configurations.
  returned: when `list_configurations` and `describe_configurations` are defined and success
  type: list
agents:
  description: list of agents.
  returned: when `describe_agents` is defined and success
  type: list
continuous_exports:
  description: list of exports.
  returned: when `describe_continuous_exports` is defined and success
  type: list
export_tasks:
  description: list of export tasks.
  returned: when `describe_export_tasks` is defined and success
  type: list
import_tasks:
  description: list of import tasks.
  returned: when `describe_import_tasks` is defined and success
  type: list
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


def _discovery(client, module):
    try:
        if module.params['list_configurations']:
            if client.can_paginate('list_configurations'):
                paginator = client.get_paginator('list_configurations')
                return paginator.paginate(
                    configurationType=module.params['configuration_type'],
                ), True
            else:
                return client.list_configurations(
                    configurationType=module.params['configuration_type'],
                ), False
        elif module.params['describe_agents']:
            if client.can_paginate('describe_agents'):
                paginator = client.get_paginator('describe_agents')
                return paginator.paginate(), True
            else:
                return client.describe_agents(), False
        elif module.params['describe_configurations']:
            if client.can_paginate('describe_configurations'):
                paginator = client.get_paginator('describe_configurations')
                return paginator.paginate(
                    configurationIds=module.params['ids'],
                ), True
            else:
                return client.describe_configurations(
                    configurationIds=module.params['ids'],
                ), False
        elif module.params['describe_continuous_exports']:
            if client.can_paginate('describe_continuous_exports'):
                paginator = client.get_paginator('describe_continuous_exports')
                return paginator.paginate(), True
            else:
                return client.describe_continuous_exports(), False
        elif module.params['describe_export_tasks']:
            if client.can_paginate('describe_export_tasks'):
                paginator = client.get_paginator('describe_export_tasks')
                return paginator.paginate(
                    exportIds=module.params['ids'],
                ), True
            else:
                return client.describe_export_tasks(
                    exportIds=module.params['ids'],
                ), False
        elif module.params['describe_import_tasks']:
            if client.can_paginate('describe_import_tasks'):
                paginator = client.get_paginator('describe_import_tasks')
                return paginator.paginate(), True
            else:
                return client.describe_import_tasks(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Discovery details')


def main():
    argument_spec = dict(
        ids=dict(required=False, type=list),
        configuration_type=dict(required=False, choices=['SERVER', 'PROCESS', 'CONNECTION', 'APPLICATION'], default='SERVER'),
        list_configurations=dict(required=False, type=bool),
        describe_agents=dict(required=False, type=bool),
        describe_configurations=dict(required=False, type=bool),
        describe_continuous_exports=dict(required=False, type=bool),
        describe_export_tasks=dict(required=False, type=bool),
        describe_import_tasks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_configurations', True, ['ids']),
            ('describe_export_tasks', True, ['ids']),
        ),
        mutually_exclusive=[
            (
                'list_configurations',
                'describe_agents',
                'describe_configurations',
                'describe_continuous_exports',
                'describe_export_tasks',
                'describe_import_tasks',
            )
        ],
    )

    client = module.client('discovery', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _discovery(client, module)

    if module.params['list_configurations'] or module.params['describe_configurations']:
        module.exit_json(configurations=aws_response_list_parser(paginate, it, 'configurations'))
    elif module.params['describe_agents']:
        module.exit_json(agents=aws_response_list_parser(paginate, it, 'agentsInfo'))
    elif module.params['describe_continuous_exports']:
        module.exit_json(continuous_exports=aws_response_list_parser(paginate, it, 'descriptions'))
    elif module.params['describe_export_tasks']:
        module.exit_json(export_tasks=aws_response_list_parser(paginate, it, 'exportsInfo'))
    elif module.params['describe_import_tasks']:
        module.exit_json(import_tasks=aws_response_list_parser(paginate, it, 'tasks'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
