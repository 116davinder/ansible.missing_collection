#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ecs_info
short_description: Get Information about Amazon EC2 Container Service (ECS).
description:
  - Get Information about Amazon EC2 Container Service (ECS).
  - U(https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  arn:
    description:
      - arn of ecs cluster.
    required: false
    type: str
  arns:
    description:
      - can be list of arn of tasks?
      - can be list of arn of container instances?
      - can be list of arn of ecs clusters?
    required: false
    type: list
  names:
    description:
      - list of name of ecs services.
    required: false
    type: list
  container_instance_status:
    description:
      - container instance status.
    required: false
    type: str
    choices: ['ACTIVE', 'DRAINING', 'REGISTERING', 'DEREGISTERING', 'REGISTRATION_FAILED']
    default: 'ACTIVE'
  launch_type:
    description:
      - type of launch.
    required: false
    type: str
    choices: ['EC2', 'FARGATE']
    default: 'EC2'
  task_definition_status:
    description:
      - task definition status.
    required: false
    type: str
    choices: ['ACTIVE', 'INACTIVE']
    default: 'ACTIVE'
  task_desired_status:
    description:
      - task desired status.
    required: false
    type: str
    choices: ['RUNNING', 'PENDING', 'STOPPED']
    default: 'RUNNING'
  list_container_instances:
    description:
      - do you want to get list of container instances for given cluster I(arn) and I(container_instance_status)?
    required: false
    type: bool
  list_services:
    description:
      - do you want to get list of services for given cluster I(arn) and I(launch_type)?
    required: false
    type: bool
  list_task_definitions:
    description:
      - do you want to get list of task definitions for given I(task_definition_status)?
    required: false
    type: bool
  list_tasks:
    description:
      - do you want to get list of tasks for given cluster I(arn), I(launch_type) and I(task_desired_status)?
    required: false
    type: bool
  describe_clusters:
    description:
      - do you want to get details of clusters for given cluster I(arns)?
    required: false
    type: bool
  describe_container_instances:
    description:
      - do you want to get details of container instances for given container instance I(arns)?
    required: false
    type: bool
  describe_services:
    description:
      - do you want to get details of services for given cluster I(arn) and service I(names)?
    required: false
    type: bool
  describe_task_definition:
    description:
      - do you want to get details of task definition for given task I(arn)?
    required: false
    type: bool
  describe_tasks:
    description:
      - do you want to get details of tasks for given cluster I(arn) and tasks I(arns)?
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
- name: "get list of cluster arns."
  aws_ecs_info:
  register: _reg

- name: "get list of container instance arns"
  aws_ecs_info:
    list_container_instances: true
    arn: '{{ _reg.cluster_arns[0] }}'
    container_instance_status: 'ACTIVE'

- name: "get list of service arns"
  aws_ecs_info:
    list_services: true
    arn: '{{ _reg.cluster_arns[0] }}'
    launch_type: 'EC2'

- name: "get list of task definition arns"
  aws_ecs_info:
    list_task_definitions: true
    task_definition_status: 'ACTIVE'

- name: "get list of task arns"
  aws_ecs_info:
    list_tasks: true
    arn: '{{ _reg.cluster_arns[0] }}'
    launch_type: 'EC2'
    task_desired_status: 'RUNNING'

- name: "get details of clusters"
  aws_ecs_info:
    describe_clusters: true
    arns: ['test-arn']

- name: "get details of container instances"
  aws_ecs_info:
    describe_container_instances: true
    arns: ['test-container-instance-arn']

- name: "get details of service"
  aws_ecs_info:
    describe_services: true
    arn: '{{ _reg.cluster_arns[0] }}'
    names: ['test-service-name']

- name: "get details of task definition"
  aws_ecs_info:
    describe_task_definition: true
    arn: '{{ _reg.cluster_arns[0] }}'
    arns: ['test-task-definition-arn']

- name: "get details of task"
  aws_ecs_info:
    describe_tasks: true
    arn: '{{ _reg.cluster_arns[0] }}'
    arns: ['test-task-arn']
"""

RETURN = """
cluster_arns:
  description: list of cluster arns.
  returned: when no arguments are defined and success
  type: list
container_instance_arns:
  description: list of container instance arns
  returned: when `list_container_instances` is defined and success
  type: list
service_arns:
  description: list of service arns.
  returned: when `list_services` is defined and success
  type: list
task_definition_arns:
  description: list of task definition arns.
  returned: when `list_task_definitions` is defined and success
  type: list
task_arns:
  description: list of task arns.
  returned: when `list_tasks` is defined and success
  type: list
clusters:
  description: details about clusters.
  returned: when `describe_clusters` is defined and success
  type: list
container_instances:
  description: details about container instances.
  returned: when `describe_container_instances` is defined and success
  type: list
services:
  description: details about services.
  returned: when `describe_services` is defined and success
  type: list
task_definition:
  description: details about task definitions.
  returned: when `describe_task_definition` is defined and success
  type: dict
tasks:
  description: details about tasks.
  returned: when `describe_tasks` is defined and success
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
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
    else:
        for _app in iterator[resource_field]:
            try:
                _return.append(camel_dict_to_snake_dict(_app))
            except AttributeError:
                _return.append(_app)
    return _return


def _ecs(client, module):
    try:
        if module.params['list_container_instances']:
            if client.can_paginate('list_container_instances'):
                paginator = client.get_paginator('list_container_instances')
                return paginator.paginate(
                    cluster=module.params['arn'],
                    status=module.params['container_instance_status'],
                ), True
            else:
                return client.list_container_instances(
                    cluster=module.params['arn'],
                    status=module.params['container_instance_status'],
                ), False
        elif module.params['list_services']:
            if client.can_paginate('list_services'):
                paginator = client.get_paginator('list_services')
                return paginator.paginate(
                    cluster=module.params['arn'],
                    launchType=module.params['launch_type'],
                ), True
            else:
                return client.list_services(
                    cluster=module.params['arn'],
                    launchType=module.params['launch_type'],
                ), False
        elif module.params['list_task_definitions']:
            if client.can_paginate('list_task_definitions'):
                paginator = client.get_paginator('list_task_definitions')
                return paginator.paginate(
                    status=module.params['task_definition_status'],
                ), True
            else:
                return client.list_task_definitions(
                    status=module.params['task_definition_status'],
                ), False
        elif module.params['list_tasks']:
            if client.can_paginate('list_tasks'):
                paginator = client.get_paginator('list_tasks')
                return paginator.paginate(
                    cluster=module.params['arn'],
                    launchType=module.params['launch_type'],
                    desiredStatus=module.params['task_desired_status'],
                ), True
            else:
                return client.list_tasks(
                    cluster=module.params['arn'],
                    launchType=module.params['launch_type'],
                    desiredStatus=module.params['task_desired_status'],
                ), False
        elif module.params['describe_clusters']:
            if client.can_paginate('describe_clusters'):
                paginator = client.get_paginator('describe_clusters')
                return paginator.paginate(
                    clusters=module.params['arns'],
                ), True
            else:
                return client.describe_clusters(
                    clusters=module.params['arns'],
                ), False
        elif module.params['describe_container_instances']:
            if client.can_paginate('describe_container_instances'):
                paginator = client.get_paginator('describe_container_instances')
                return paginator.paginate(
                    containerInstances=module.params['arns'],
                ), True
            else:
                return client.describe_container_instances(
                    containerInstances=module.params['arns'],
                ), False
        elif module.params['describe_services']:
            if client.can_paginate('describe_services'):
                paginator = client.get_paginator('describe_services')
                return paginator.paginate(
                    cluster=module.params['arn'],
                    services=module.params['names'],
                ), True
            else:
                return client.describe_services(
                    cluster=module.params['arn'],
                    services=module.params['names'],
                ), False
        elif module.params['describe_task_definition']:
            return client.describe_task_definition(
                taskDefinition=module.params['arn'],
            ), False
        elif module.params['describe_tasks']:
            if client.can_paginate('describe_tasks'):
                paginator = client.get_paginator('describe_tasks')
                return paginator.paginate(
                    cluster=module.params['arn'],
                    tasks=module.params['arns'],
                ), True
            else:
                return client.describe_tasks(
                    cluster=module.params['arn'],
                    tasks=module.params['arns'],
                ), False
        else:
            if client.can_paginate('list_clusters'):
                paginator = client.get_paginator('list_clusters')
                return paginator.paginate(), True
            else:
                return client.list_clusters(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS ECS details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        arns=dict(required=False, type=list),
        names=dict(required=False, type=list),
        container_instance_status=dict(
            required=False,
            choices=['ACTIVE', 'DRAINING', 'REGISTERING', 'DEREGISTERING', 'REGISTRATION_FAILED'],
            default='ACTIVE'
        ),
        launch_type=dict(
            required=False,
            choices=['EC2', 'FARGATE'],
            default='EC2'
        ),
        task_definition_status=dict(
            required=False,
            choices=['ACTIVE', 'INACTIVE'],
            default='ACTIVE'
        ),
        task_desired_status=dict(
            required=False,
            choices=['RUNNING', 'PENDING', 'STOPPED'],
            default='RUNNING'
        ),
        list_container_instances=dict(required=False, type=bool),
        list_services=dict(required=False, type=bool),
        list_task_definitions=dict(required=False, type=bool),
        list_tasks=dict(required=False, type=bool),
        describe_clusters=dict(required=False, type=bool),
        describe_container_instances=dict(required=False, type=bool),
        describe_services=dict(required=False, type=bool),
        describe_task_definition=dict(required=False, type=bool),
        describe_tasks=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_container_instances', True, ['arn']),
            ('list_services', True, ['arn']),
            ('list_tasks', True, ['arn']),
            ('describe_clusters', True, ['arns']),
            ('describe_container_instances', True, ['arns']),
            ('describe_services', True, ['arn', 'names']),
            ('describe_task_definition', True, ['arn']),
            ('describe_tasks', True, ['arn', 'arns']),
        ),
        mutually_exclusive=[
            (
                'list_container_instances',
                'list_services',
                'list_task_definitions',
                'list_tasks',
                'describe_clusters',
                'describe_container_instances',
                'describe_services',
                'describe_task_definition',
                'describe_tasks',
            )
        ],
    )

    client = module.client('ecs', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ecs(client, module)

    if module.params['list_container_instances']:
        module.exit_json(container_instance_arns=aws_response_list_parser(paginate, it, 'containerInstanceArns'))
    elif module.params['list_services']:
        module.exit_json(service_arns=aws_response_list_parser(paginate, it, 'serviceArns'))
    elif module.params['list_task_definitions']:
        module.exit_json(task_definition_arns=aws_response_list_parser(paginate, it, 'taskDefinitionArns'))
    elif module.params['list_tasks']:
        module.exit_json(task_arns=aws_response_list_parser(paginate, it, 'taskArns'))
    elif module.params['describe_clusters']:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'clusters'))
    elif module.params['describe_container_instances']:
        module.exit_json(container_instances=aws_response_list_parser(paginate, it, 'containerInstances'))
    elif module.params['describe_services']:
        module.exit_json(services=aws_response_list_parser(paginate, it, 'services'))
    elif module.params['describe_task_definition']:
        module.exit_json(task_definition=camel_dict_to_snake_dict(it['taskDefinition']))
    elif module.params['describe_tasks']:
        module.exit_json(tasks=aws_response_list_parser(paginate, it, 'tasks'))
    else:
        module.exit_json(cluster_arns=aws_response_list_parser(paginate, it, 'clusterArns'))


if __name__ == '__main__':
    main()
