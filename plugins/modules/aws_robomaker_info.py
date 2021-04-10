#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_robomaker_info
short_description: Get Information about Amazon Robomaker.
description:
  - Get Information about Amazon Robomaker.
  - U(https://docs.aws.amazon.com/robomaker/latest/dg/API_Operations.html)
version_added: 0.0.8
options:
  list_deployment_jobs:
    description:
      - do you want to get list of deployment_jobs?
    required: false
    type: bool
  list_fleets:
    description:
      - do you want to get fleets?
    required: false
    type: bool
  list_robot_applications:
    description:
      - do you want to get list of robot_applications?
    required: false
    type: bool
  list_robots:
    description:
      - do you want to get robots?
    required: false
    type: bool
  list_simulation_jobs:
    description:
      - do you want to get simulation_jobs?
    required: false
    type: bool
  list_worlds:
    description:
      - do you want to get worlds?
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
- name: "get list of deployment_jobs"
  aws_robomaker_info:
    list_deployment_jobs: true

- name: "get fleets"
  aws_robomaker_info:
    list_fleets: true

- name: "get list of robot_applications"
  aws_robomaker_info:
    list_robot_applications: true

- name: "get robots"
  aws_robomaker_info:
    list_robots: true

- name: "get simulation_jobs"
  aws_robomaker_info:
    list_simulation_jobs: true

- name: "get worlds"
  aws_robomaker_info:
    list_worlds: true
"""

RETURN = """
deployment_jobs:
  description: list of deployment_jobs.
  returned: when `list_deployment_jobs` is defined and success.
  type: list
fleets:
  description: get of fleets.
  returned: when `list_fleets` is defined and success.
  type: list
robot_applications:
  description: list of robot_applications.
  returned: when `list_robot_applications` is defined and success.
  type: list
robots:
  description: list of robots.
  returned: when `list_robots` is defined and success.
  type: list
simulation_jobs:
  description: list of simulation_jobs.
  returned: when `list_simulation_jobs` is defined and success.
  type: list
worlds:
  description: list of worlds.
  returned: when `list_worlds` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _robomaker(client, module):
    try:
        if module.params['list_deployment_jobs']:
            if client.can_paginate('list_deployment_jobs'):
                paginator = client.get_paginator('list_deployment_jobs')
                return paginator.paginate(), True
            else:
                return client.list_deployment_jobs(), False
        elif module.params['list_fleets']:
            if client.can_paginate('list_fleets'):
                paginator = client.get_paginator('list_fleets')
                return paginator.paginate(), True
            else:
                return client.list_fleets(), False
        elif module.params['list_robot_applications']:
            if client.can_paginate('list_robot_applications'):
                paginator = client.get_paginator('list_robot_applications')
                return paginator.paginate(), True
            else:
                return client.list_robot_applications(), False
        elif module.params['list_robots']:
            if client.can_paginate('list_robots'):
                paginator = client.get_paginator('list_robots')
                return paginator.paginate(), True
            else:
                return client.list_robots(), False
        elif module.params['list_simulation_jobs']:
            if client.can_paginate('list_simulation_jobs'):
                paginator = client.get_paginator('list_simulation_jobs')
                return paginator.paginate(), True
            else:
                return client.list_simulation_jobs(), False
        elif module.params['list_worlds']:
            if client.can_paginate('list_worlds'):
                paginator = client.get_paginator('list_worlds')
                return paginator.paginate(), True
            else:
                return client.list_worlds(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Robomaker details')


def main():
    argument_spec = dict(
        list_deployment_jobs=dict(required=False, type=bool),
        list_fleets=dict(required=False, type=bool),
        list_robot_applications=dict(required=False, type=bool),
        list_robots=dict(required=False, type=bool),
        list_simulation_jobs=dict(required=False, type=bool),
        list_worlds=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_deployment_jobs',
                'list_fleets',
                'list_robot_applications',
                'list_robots',
                'list_simulation_jobs',
                'list_worlds',
            )
        ],
    )

    client = module.client('robomaker', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _robomaker(client, module)

    if module.params['list_deployment_jobs']:
        module.exit_json(deployment_jobs=aws_response_list_parser(paginate, it, 'deploymentJobs'))
    elif module.params['list_fleets']:
        module.exit_json(fleets=aws_response_list_parser(paginate, it, 'fleetDetails'))
    elif module.params['list_robot_applications']:
        module.exit_json(robot_applications=aws_response_list_parser(paginate, it, 'robotApplicationSummaries'))
    elif module.params['list_robots']:
        module.exit_json(robots=aws_response_list_parser(paginate, it, 'robots'))
    elif module.params['list_simulation_jobs']:
        module.exit_json(simulation_jobs=aws_response_list_parser(paginate, it, 'simulationJobSummaries'))
    elif module.params['list_worlds']:
        module.exit_json(worlds=aws_response_list_parser(paginate, it, 'worldSummaries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
