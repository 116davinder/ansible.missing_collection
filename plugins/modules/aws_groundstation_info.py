#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_groundstation_info
short_description: Get Information about AWS Ground Station.
description:
  - Get Information about AWS Ground Station.
  - U(https://docs.aws.amazon.com/ground-station/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  list_configs:
    description:
      - do you want to get list of configs for given component I(arn)?
    required: false
    type: bool
  list_dataflow_endpoint_groups:
    description:
      - do you want to get list of dataflow endpoint groups?
    required: false
    type: bool
  list_ground_stations:
    description:
      - do you want to get list of ground stations?
    required: false
    type: bool
  list_mission_profiles:
    description:
      - do you want to get list of mission profiles?
    required: false
    type: bool
  list_satellites:
    description:
      - do you want to get list of satellites?
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
- name: "get list of configs"
  aws_groundstation_info:
    list_configs: true

- name: "get list of dataflow_endpoint_groups"
  aws_groundstation_info:
    list_dataflow_endpoint_groups: true

- name: "get list of ground stations"
  aws_groundstation_info:
    list_ground_stations: true

- name: "get list of mission_profiles"
  aws_groundstation_info:
    list_mission_profiles: true

- name: "get list of satellites"
  aws_groundstation_info:
    list_satellites: true
"""

RETURN = """
configs:
  description: list of configs.
  returned: when `list_configs` is defined and success.
  type: list
dataflow_endpoint_groups:
  description: list of dataflow_endpoint_groups.
  returned: when `list_dataflow_endpoint_groups` is defined and success.
  type: list
ground_stations:
  description: list of ground stations.
  returned: when `list_ground_stations` is defined and success.
  type: list
mission_profiles:
  description: list of mission_profiles.
  returned: when `list_mission_profiles` is defined and success.
  type: list
satellites:
  description: list of satellites.
  returned: when `list_satellites` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _groundstation(client, module):
    try:
        if module.params['list_configs']:
            if client.can_paginate('list_configs'):
                paginator = client.get_paginator('list_configs')
                return paginator.paginate(), True
            else:
                return client.list_configs(), False
        elif module.params['list_dataflow_endpoint_groups']:
            if client.can_paginate('list_dataflow_endpoint_groups'):
                paginator = client.get_paginator('list_dataflow_endpoint_groups')
                return paginator.paginate(), True
            else:
                return client.list_dataflow_endpoint_groups(), False
        elif module.params['list_ground_stations']:
            if client.can_paginate('list_ground_stations'):
                paginator = client.get_paginator('list_ground_stations')
                return paginator.paginate(), True
            else:
                return client.list_ground_stations(), False
        elif module.params['list_mission_profiles']:
            if client.can_paginate('list_mission_profiles'):
                paginator = client.get_paginator('list_mission_profiles')
                return paginator.paginate(), True
            else:
                return client.list_mission_profiles(), False
        elif module.params['list_satellites']:
            if client.can_paginate('list_satellites'):
                paginator = client.get_paginator('list_satellites')
                return paginator.paginate(), True
            else:
                return client.list_satellites(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon groundstation details')


def main():
    argument_spec = dict(
        list_configs=dict(required=False, type=bool),
        list_dataflow_endpoint_groups=dict(required=False, type=bool),
        list_ground_stations=dict(required=False, type=bool),
        list_mission_profiles=dict(required=False, type=bool),
        list_satellites=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(),
        mutually_exclusive=[
            (
                'list_configs',
                'list_dataflow_endpoint_groups',
                'list_ground_stations',
                'list_mission_profiles',
                'list_satellites',
            )
        ],
    )

    client = module.client('groundstation', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _groundstation(client, module)

    if module.params['list_configs']:
        module.exit_json(configs=aws_response_list_parser(paginate, it, 'configList'))
    elif module.params['list_dataflow_endpoint_groups']:
        module.exit_json(dataflow_endpoint_groups=aws_response_list_parser(paginate, it, 'dataflowEndpointGroupList'))
    elif module.params['list_ground_stations']:
        module.exit_json(ground_stations=aws_response_list_parser(paginate, it, 'groundStationList'))
    elif module.params['list_mission_profiles']:
        module.exit_json(mission_profiles=aws_response_list_parser(paginate, it, 'missionProfileList'))
    elif module.params['list_satellites']:
        module.exit_json(satellites=aws_response_list_parser(paginate, it, 'satellites'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
