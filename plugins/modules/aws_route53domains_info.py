#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_route53domains_info
short_description: Get Information about Amazon Route 53 Domains.
description:
  - Get Information about Amazon Route 53 Domains.
  - U(https://docs.aws.amazon.com/Route53/latest/APIReference/API_Operations_Amazon_Route_53_Domains.html)
version_added: 0.0.8
options:
  name:
    description:
      - name of domain.
    required: false
    type: str
    aliases: ['domain_name']
  list_domains:
    description:
      - do you want to get list of domains?
    required: false
    type: bool
  get_domain_detail:
    description:
      - do you want to get domain_detail for given domain I(name)?
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
- name: "get list of domains"
  aws_route53domains_info:
    list_domains: true

- name: "get domain_detail"
  aws_route53domains_info:
    get_domain_detail: true
    name: 'example.com'
"""

RETURN = """
domains:
  description: list of domains.
  returned: when `list_domains` is defined and success.
  type: list
domain_detail:
  description: get of domain_detail.
  returned: when `get_domain_detail` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _route53domains(client, module):
    try:
        if module.params['list_domains']:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(), True
            else:
                return client.list_domains(), False
        elif module.params['get_domain_detail']:
            return client.get_domain_detail(
                DomainName=module.params['name']
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Route 53 Domains details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['domain_name']),
        list_domains=dict(required=False, type=bool),
        get_domain_detail=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_domain_detail', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_domains',
                'get_domain_detail',
            )
        ],
    )

    client = module.client('route53domains', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _route53domains(client, module)

    if module.params['list_domains']:
        module.exit_json(domains=aws_response_list_parser(paginate, it, 'Domains'))
    elif module.params['get_domain_detail']:
        module.exit_json(domain_detail=camel_dict_to_snake_dict(it))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
