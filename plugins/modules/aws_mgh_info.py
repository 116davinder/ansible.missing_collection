#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_mgh_info
short_description: Get Information about AWS Migration Hub.
description:
  - Get Information about AWS Migration Hub.
  - U(https://docs.aws.amazon.com/migrationhub/latest/ug/API_Operations.html)
version_added: 0.0.7
options:
  name:
    description:
      - migration task name.
    required: false
    type: str
    aliases: ['migration_task_name']
  progress_update_stream:
    description:
      - name of progress_update_stream.
    required: false
    type: str
  list_application_states:
    description:
      - do you want to get list of application_states?
    required: false
    type: bool
  list_created_artifacts:
    description:
      - do you want to get created_artifacts for given migration task I(name) and I(progress_update_stream)?
    required: false
    type: bool
  list_discovered_resources:
    description:
      - do you want to get list of discovered_resources for given migration task I(name) and I(progress_update_stream)?
    required: false
    type: bool
  list_migration_tasks:
    description:
      - do you want to get migration_tasks?
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
- name: "get list of application_states"
  aws_mgh_info:
    list_application_states: true

- name: "get created_artifacts"
  aws_mgh_info:
    list_created_artifacts: true
    name: 'migration_task_name'
    progress_update_stream: 'name of progress_update_stream'

- name: "get list of discovered_resources"
  aws_mgh_info:
    list_discovered_resources: true
    name: 'migration_task_name'
    progress_update_stream: 'name of progress_update_stream'

- name: "get migration_tasks"
  aws_mgh_info:
    list_migration_tasks: true
    name: 'source-location-name'
"""

RETURN = """
application_states:
  description: list of application_states.
  returned: when `list_application_states` is defined and success.
  type: list
created_artifacts:
  description: get of created_artifacts.
  returned: when `list_created_artifacts` is defined and success.
  type: list
discovered_resources:
  description: list of discovered_resources.
  returned: when `list_discovered_resources` is defined and success.
  type: list
migration_tasks:
  description: list of migration_tasks.
  returned: when `list_migration_tasks` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _mgh(client, module):
    try:
        if module.params['list_application_states']:
            if client.can_paginate('list_application_states'):
                paginator = client.get_paginator('list_application_states')
                return paginator.paginate(), True
            else:
                return client.list_application_states(), False
        elif module.params['list_created_artifacts']:
            if client.can_paginate('list_created_artifacts'):
                paginator = client.get_paginator('list_created_artifacts')
                return paginator.paginate(
                    MigrationTaskName=module.params['name'],
                    ProgressUpdateStream=module.params['progress_update_stream']
                ), True
            else:
                return client.list_created_artifacts(
                    MigrationTaskName=module.params['name'],
                    ProgressUpdateStream=module.params['progress_update_stream']
                ), False
        elif module.params['list_discovered_resources']:
            if client.can_paginate('list_discovered_resources'):
                paginator = client.get_paginator('list_discovered_resources')
                return paginator.paginate(
                    MigrationTaskName=module.params['name'],
                    ProgressUpdateStream=module.params['progress_update_stream']
                ), True
            else:
                return client.list_discovered_resources(
                    MigrationTaskName=module.params['name'],
                    ProgressUpdateStream=module.params['progress_update_stream']
                ), False
        elif module.params['list_migration_tasks']:
            if client.can_paginate('list_migration_tasks'):
                paginator = client.get_paginator('list_migration_tasks')
                return paginator.paginate(), True
            else:
                return client.list_migration_tasks(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Migration Hub details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['migration_task_name']),
        progress_update_stream=dict(required=False),
        list_application_states=dict(required=False, type=bool),
        list_created_artifacts=dict(required=False, type=bool),
        list_discovered_resources=dict(required=False, type=bool),
        list_migration_tasks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_created_artifacts', True, ['name', 'progress_update_stream']),
            ('list_discovered_resources', True, ['name', 'progress_update_stream']),
        ),
        mutually_exclusive=[
            (
                'list_application_states',
                'list_created_artifacts',
                'list_discovered_resources',
                'list_migration_tasks',
            )
        ],
    )

    client = module.client('mgh', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _mgh(client, module)

    if module.params['list_application_states']:
        module.exit_json(application_states=aws_response_list_parser(paginate, it, 'ApplicationStateList'))
    elif module.params['list_created_artifacts']:
        module.exit_json(created_artifacts=aws_response_list_parser(paginate, it, 'CreatedArtifactList'))
    elif module.params['list_discovered_resources']:
        module.exit_json(discovered_resources=aws_response_list_parser(paginate, it, 'DiscoveredResourceList'))
    elif module.params['list_migration_tasks']:
        module.exit_json(migration_tasks=aws_response_list_parser(paginate, it, 'MigrationTaskSummaryList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
