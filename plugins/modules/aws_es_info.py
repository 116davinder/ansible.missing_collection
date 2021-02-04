#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_es_info
short_description: Get Information about Amazon Elasticsearch Service.
description:
  - Get Information about Amazon Elasticsearch Service.
  - U(https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-configuration-api.html)
version_added: 0.0.6
options:
  name:
    description:
      - name of elastic search domain.
    required: false
    type: str
  list_packages_for_domain:
    description:
      - do you want to get list of packages for given I(name)?
    required: false
    type: bool
  describe_elasticsearch_domain:
    description:
      - do you want to get domain details of given I(name)?
    required: false
    type: bool
  describe_elasticsearch_domain_config:
    description:
      - do you want to get domain config details of given I(name)?
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
- name: "get list of all es domains"
  aws_es_info:

- name: "get list of packages"
  aws_es_info:
    list_packages_for_domain: true
    name: 'test'

- name: "get details of domain"
  aws_es_info:
    describe_elasticsearch_domain: true
    name: 'test'

- name: "get details of domain config"
  aws_es_info:
    describe_elasticsearch_domain_config: true
    name: 'test'
"""

RETURN = """
domain_names:
  description: list of all es domains.
  returned: when no arguments are defined and success
  type: list
packages:
  description: list of packages.
  returned: when `list_packages_for_domain` is defined and success
  type: list
domain_status:
  description: details about given domain.
  returned: when `describe_elasticsearch_domain` is defined and success
  type: dict
domain_config:
  description: details about given domain config.
  returned: when `describe_elasticsearch_domain_config` is defined and success
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


def _es(client, module):
    try:
        if module.params['list_packages_for_domain']:
            if client.can_paginate('list_packages_for_domain'):
                paginator = client.get_paginator('list_packages_for_domain')
                return paginator.paginate(
                    DomainName=module.params['name'],
                ), True
            else:
                return client.list_packages_for_domain(
                    DomainName=module.params['name'],
                ), False
        elif module.params['describe_elasticsearch_domain']:
            return client.describe_elasticsearch_domain(
                DomainName=module.params['name'],
            ), False
        elif module.params['describe_elasticsearch_domain_config']:
            return client.describe_elasticsearch_domain_config(
                DomainName=module.params['name'],
            ), False
        else:
            if client.can_paginate('list_domain_names'):
                paginator = client.get_paginator('list_domain_names')
                return paginator.paginate(), True
            else:
                return client.list_domain_names(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon ES details')


def main():
    argument_spec = dict(
        name=dict(required=False),
        list_packages_for_domain=dict(required=False, type=bool),
        describe_elasticsearch_domain=dict(required=False, type=bool),
        describe_elasticsearch_domain_config=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_packages_for_domain', True, ['name']),
            ('describe_elasticsearch_domain', True, ['name']),
            ('describe_elasticsearch_domain_config', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_packages_for_domain',
                'describe_elasticsearch_domain',
                'describe_elasticsearch_domain_config',
            )
        ],
    )

    client = module.client('es', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _es(client, module)

    if module.params['list_packages_for_domain']:
        module.exit_json(packages=aws_response_list_parser(paginate, it, 'DomainPackageDetailsList'))
    elif module.params['describe_elasticsearch_domain']:
        module.exit_json(domain_status=camel_dict_to_snake_dict(it['DomainStatus']))
    elif module.params['describe_elasticsearch_domain_config']:
        module.exit_json(domain_config=camel_dict_to_snake_dict(it['DomainConfig']))
    else:
        module.exit_json(domain_names=aws_response_list_parser(paginate, it, 'DomainNames'))


if __name__ == '__main__':
    main()
