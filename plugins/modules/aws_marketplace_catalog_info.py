#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_marketplace_catalog_info
short_description: Get Information about AWS Marketplace Catalog Service.
description:
  - Get Information about AWS Marketplace Catalog Service.
  - U(https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/API_Operations.html)
version_added: 0.0.7
options:
  entity_type:
    description:
      - type of the entity.
    required: false
    type: str
  list_change_sets:
    description:
      - do you want to get list of change_sets for given I(catalog)?
    required: false
    type: bool
  list_entities:
    description:
      - do you want to get list of entities for given I(catalog)) and I(entity_type)?
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
- name: "get list of change_sets"
  aws_marketplace_catalog_info:
    list_change_sets: true
    catalog: 'AWSMarketplace'

- name: "get list of entities"
  aws_marketplace_catalog_info:
    list_entities: true
    catalog: 'AWSMarketplace'
    entity_type: 'test-entity-type'
"""

RETURN = """
change_sets:
  description: list of change_sets.
  returned: when `list_change_sets` is defined and success.
  type: list
entities:
  description: list of entities.
  returned: when `list_entities` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _marketplace_catalog(client, module):
    try:
        if module.params['list_change_sets']:
            if client.can_paginate('list_change_sets'):
                paginator = client.get_paginator('list_change_sets')
                return paginator.paginate(
                    Catalog=module.params['catalog']
                ), True
            else:
                return client.list_change_sets(
                    Catalog=module.params['catalog']
                ), False
        elif module.params['list_entities']:
            if client.can_paginate('list_entities'):
                paginator = client.get_paginator('list_entities')
                return paginator.paginate(
                    Catalog=module.params['catalog'],
                    EntityType=module.params['entity_type']
                ), True
            else:
                return client.list_entities(
                    Catalog=module.params['catalog'],
                    EntityType=module.params['entity_type']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Marketplace Catalog Service details')


def main():
    argument_spec = dict(
        entity_type=dict(required=False),
        catalog=dict(required=False, choices=['AWSMarketplace'], default='AWSMarketplace'),
        list_change_sets=dict(required=False, type=bool),
        list_entities=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_change_sets', True, ['catalog', 'entity_type']),
            ('list_entities', True, ['catalog']),
        ),
        mutually_exclusive=[
            (
                'list_change_sets',
                'list_entities',
            )
        ],
    )

    client = module.client('marketplace-catalog', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _marketplace_catalog(client, module)

    if module.params['list_change_sets']:
        module.exit_json(change_sets=aws_response_list_parser(paginate, it, 'ChangeSetSummaryList'))
    elif module.params['list_entities']:
        module.exit_json(entities=aws_response_list_parser(paginate, it, 'EntitySummaryList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
