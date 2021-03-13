#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_managedblockchain_info
short_description: Get Information about Amazon Managed Blockchain.
description:
  - Get Information about Amazon Managed Blockchain.
  - U(https://docs.aws.amazon.com/managed-blockchain/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  id:
    description:
      - member account id.
    required: false
    type: str
  list_invitations:
    description:
      - do you want to get list of invitations?
    required: false
    type: bool
  list_members:
    description:
      - do you want to get list of members for given I(id))?
    required: false
    type: bool
  list_networks:
    description:
      - do you want to get list of networks?
    required: false
    type: bool
  list_nodes:
    description:
      - do you want to get list of nodes for given I(id))?
    required: false
    type: bool
  list_proposal_votes:
    description:
      - do you want to get list of proposal_votes for given I(id) and I(proposal_id)?
    required: false
    type: bool
  list_proposals:
    description:
      - do you want to get list of proposals for given I(id))?
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
- name: "get list of invitations"
  aws_managedblockchain_info:
    list_invitations: true

- name: "get list of members"
  aws_managedblockchain_info:
    list_members: true
    id: 'network-id'

- name: "get list of networks"
  aws_managedblockchain_info:
    list_networks: true

- name: "get list of nodes"
  aws_managedblockchain_info:
    list_nodes: true
    id: 'network-id'

- name: "get list of proposal_votes"
  aws_managedblockchain_info:
    list_proposal_votes: true
    id: 'network-id'
    proposal_id: 'proposal-id'

- name: "get list of proposals"
  aws_managedblockchain_info:
    list_proposals: true
    id: 'network-id'
"""

RETURN = """
invitations:
  description: list of invitations.
  returned: when `list_invitations` is defined and success.
  type: list
members:
  description: list of members.
  returned: when `list_members` is defined and success.
  type: list
networks:
  description: list of networks.
  returned: when `list_networks` is defined and success.
  type: list
nodes:
  description: list of nodes.
  returned: when `list_members` is defined and success.
  type: list
proposal_votes:
  description: list of proposal_votes.
  returned: when `list_proposal_votes` is defined and success.
  type: list
proposals:
  description: list of proposals.
  returned: when `list_proposals` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _managedblockchain(client, module):
    try:
        if module.params['list_invitations']:
            if client.can_paginate('list_invitations'):
                paginator = client.get_paginator('list_invitations')
                return paginator.paginate(), True
            else:
                return client.list_invitations(), False
        elif module.params['list_members']:
            if client.can_paginate('list_members'):
                paginator = client.get_paginator('list_members')
                return paginator.paginate(
                    NetworkId=module.params['id'],
                ), True
            else:
                return client.list_members(
                    NetworkId=module.params['id'],
                ), False
        elif module.params['list_networks']:
            if client.can_paginate('list_networks'):
                paginator = client.get_paginator('list_networks')
                return paginator.paginate(), True
            else:
                return client.list_networks(), False
        elif module.params['list_nodes']:
            if client.can_paginate('list_nodes'):
                paginator = client.get_paginator('list_nodes')
                return paginator.paginate(
                    NetworkId=module.params['id'],
                ), True
            else:
                return client.list_nodes(
                    NetworkId=module.params['id'],
                ), False
        elif module.params['list_proposal_votes']:
            if client.can_paginate('list_proposal_votes'):
                paginator = client.get_paginator('list_proposal_votes')
                return paginator.paginate(
                    NetworkId=module.params['id'],
                    ProposalId=module.params['proposal_id']
                ), True
            else:
                return client.list_proposal_votes(
                    NetworkId=module.params['id'],
                    ProposalId=module.params['proposal_id']
                ), False
        elif module.params['list_proposals']:
            if client.can_paginate('list_proposals'):
                paginator = client.get_paginator('list_proposals')
                return paginator.paginate(
                    NetworkId=module.params['id'],
                ), True
            else:
                return client.list_proposals(
                    NetworkId=module.params['id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Managed Blockchain details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['network_id']),
        proposal_id=dict(required=False),
        list_invitations=dict(required=False, type=bool),
        list_members=dict(required=False, type=bool),
        list_networks=dict(required=False, type=bool),
        list_nodes=dict(required=False, type=bool),
        list_proposal_votes=dict(required=False, type=bool),
        list_proposals=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_members', True, ['id']),
            ('list_nodes', True, ['id']),
            ('list_proposal_votes', True, ['id', 'proposal_id']),
            ('list_proposals', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_invitations',
                'list_members',
                'list_networks',
                'list_nodes',
                'list_proposal_votes',
                'list_proposals',
            )
        ],
    )

    client = module.client('managedblockchain', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _managedblockchain(client, module)

    if module.params['list_invitations']:
        module.exit_json(invitations=aws_response_list_parser(paginate, it, 'Invitations'))
    elif module.params['list_members']:
        module.exit_json(members=aws_response_list_parser(paginate, it, 'Members'))
    elif module.params['list_networks']:
        module.exit_json(networks=aws_response_list_parser(paginate, it, 'Networks'))
    elif module.params['list_nodes']:
        module.exit_json(nodes=aws_response_list_parser(paginate, it, 'Nodes'))
    elif module.params['list_proposal_votes']:
        module.exit_json(proposal_votes=aws_response_list_parser(paginate, it, 'ProposalVotes'))
    elif module.params['list_proposals']:
        module.exit_json(proposals=aws_response_list_parser(paginate, it, 'Proposals'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
