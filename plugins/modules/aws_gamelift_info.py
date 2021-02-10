#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_gamelift_info
short_description: Get Information about Amazon Gamelift.
description:
  - Get Information about Amazon Gamelift.
  - U(https://docs.aws.amazon.com/gamelift/latest/apireference/API_Operations.html)
version_added: 0.0.6
options:
  build_id:
    description:
      - id of build.
    required: false
    type: str
  game_server_group_name:
    description:
      - name of game server group.
    required: false
    type: str
  routing_strategy_type:
    description:
      - type of routing strategy.
    required: false
    type: str
    choices: ['SIMPLE', 'TERMINAL']
    default: 'SIMPLE'
  status:
    description:
      - status of build.
    required: false
    type: str
    choices: ['INITIALIZED', 'READY', 'FAILED']
    default: 'READY'
  list_aliases:
    description:
      - do you want to get list of aliases?
    required: false
    type: bool
  list_builds:
    description:
      - do you want to get list of builds?
    required: false
    type: bool
  list_fleets:
    description:
      - do you want to get list of fleets for given I(build_id)?
    required: false
    type: bool
  list_game_server_groups:
    description:
      - do you want to get list of game server groups?
    required: false
    type: bool
  list_game_servers:
    description:
      - do you want to get list of game servers?
    required: false
    type: bool
  list_scripts:
    description:
      - do you want to get details of scripts?
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
- name: "get details of aliases"
  aws_gamelift_info:
    list_aliases: true
    routing_strategy_type: 'SIMPLE'

- name: "get details of builds"
  aws_gamelift_info:
    list_builds: true
    status: 'READY'

- name: "get details of fleets"
  aws_gamelift_info:
    list_fleets: true
    build_id: 'test'

- name: "get details of game server groups"
  aws_gamelift_info:
    list_game_server_groups: true

- name: "get details of game server"
  aws_gamelift_info:
    list_game_servers: true
    game_server_group_name: 'test'

- name: "get details of scripts"
  aws_gamelift_info:
    list_scripts: true
"""

RETURN = """
aliases:
  description: list of aliases.
  returned: when `list_aliases` is defined and success.
  type: list
builds:
  description: list of builds.
  returned: when `list_builds` is defined and success.
  type: list
fleets:
  description: list of fleets.
  returned: when `list_fleets` is defined and success.
  type: list
game_server_groups:
  description: list of game_server_groups.
  returned: when `list_game_server_groups` is defined and success.
  type: list
game_servers:
  description: list of game_servers.
  returned: when `list_game_servers` is defined and success.
  type: list
scripts:
  description: list of scripts.
  returned: when `list_scripts` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _gamelift(client, module):
    try:
        if module.params['list_aliases']:
            if client.can_paginate('list_aliases'):
                paginator = client.get_paginator('list_aliases')
                return paginator.paginate(
                    RoutingStrategyType=module.params['routing_strategy_type'],
                ), True
            else:
                return client.list_aliases(
                    RoutingStrategyType=module.params['routing_strategy_type'],
                ), False
        elif module.params['list_builds']:
            if client.can_paginate('list_builds'):
                paginator = client.get_paginator('list_builds')
                return paginator.paginate(
                    Status=module.params['status'],
                ), True
            else:
                return client.list_builds(
                    Status=module.params['status'],
                ), False
        elif module.params['list_fleets']:
            if client.can_paginate('list_fleets'):
                paginator = client.get_paginator('list_fleets')
                return paginator.paginate(
                    BuildId=module.params['build_id'],
                ), True
            else:
                return client.list_fleets(
                    BuildId=module.params['build_id'],
                ), False
        elif module.params['list_game_server_groups']:
            if client.can_paginate('list_game_server_groups'):
                paginator = client.get_paginator('list_game_server_groups')
                return paginator.paginate(), True
            else:
                return client.list_game_server_groups(), False
        elif module.params['list_game_servers']:
            if client.can_paginate('list_game_servers'):
                paginator = client.get_paginator('list_game_servers')
                return paginator.paginate(
                    GameServerGroupName=module.params['game_server_group_name'],
                    SortOrder='ASCENDING'
                ), True
            else:
                return client.list_game_servers(
                    GameServerGroupName=module.params['game_server_group_name'],
                    SortOrder='ASCENDING'
                ), False
        elif module.params['list_scripts']:
            if client.can_paginate('list_scripts'):
                paginator = client.get_paginator('list_scripts')
                return paginator.paginate(), True
            else:
                return client.list_scripts(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon gamelift details')


def main():
    argument_spec = dict(
        routing_strategy_type=dict(required=False, choices=['SIMPLE', 'TERMINAL'], default='SIMPLE'),
        status=dict(required=False, choices=['INITIALIZED', 'READY', 'FAILED'], default='READY'),
        build_id=dict(required=False),
        game_server_group_name=dict(required=False),
        list_aliases=dict(required=False, type=bool),
        list_builds=dict(required=False, type=bool),
        list_fleets=dict(required=False, type=bool),
        list_game_server_groups=dict(required=False, type=bool),
        list_game_servers=dict(required=False, type=bool),
        list_scripts=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_fleets', True, ['build_id']),
            ('list_game_servers', True, ['game_server_group_name']),
        ),
        mutually_exclusive=[
            (
                'list_aliases',
                'list_builds',
                'list_fleets',
                'list_game_server_groups',
                'list_game_servers',
                'list_scripts',
            )
        ],
    )

    client = module.client('gamelift', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _gamelift(client, module)

    if module.params['list_aliases']:
        module.exit_json(aliases=aws_response_list_parser(paginate, it, 'Aliases'))
    elif module.params['list_builds']:
        module.exit_json(builds=aws_response_list_parser(paginate, it, 'Builds'))
    elif module.params['list_fleets']:
        module.exit_json(fleets=aws_response_list_parser(paginate, it, 'FleetIds'))
    elif module.params['list_game_server_groups']:
        module.exit_json(game_server_groups=aws_response_list_parser(paginate, it, 'GameServerGroups'))
    elif module.params['list_game_servers']:
        module.exit_json(game_servers=aws_response_list_parser(paginate, it, 'GameServers'))
    elif module.params['list_scripts']:
        module.exit_json(scripts=aws_response_list_parser(paginate, it, 'Scripts'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
