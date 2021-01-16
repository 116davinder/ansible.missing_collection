#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_customer_profiles_info
short_description: Get Information about Amazon Connect Customer Profiles.
description:
  - Get Information about Amazon Connect Customer Profiles.
  - U(https://docs.aws.amazon.com/customerprofiles/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  uri:
    description:
      -  The URI of the S3 bucket or any other type of data source.
    required: false
    type: str
  domain_name:
    description:
      - The unique name of the domain.
    required: false
    type: str
  list_account_integrations:
    description:
      - do you want to get list of account integrations of given I(uri)?
    required: false
    type: bool
  list_integrations:
    description:
      - do you want to get list of integrations of given I(domain_name)?
    required: false
    type: bool
  list_profile_object_type_templates:
    description:
      - do you want to get list of profile object type templates?
    required: false
    type: bool
  list_profile_object_types:
    description:
      - do you want to get list of profile object types of given I(domain_name)?
    required: false
    type: bool
  get_domain:
    description:
      - do you want to get details of given I(domain_name)?
    required: false
    type: bool
  get_integration:
    description:
      - do you want to get details of given I(domain_name) integration?
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
- name: "list of connect domains."
  aws_customer_profiles_info:

- name: "Lists all of the integrations associated to a specific URI in the AWS account."
  aws_customer_profiles_info:
    list_account_integrations: true
    uri: 'test'

- name: "Lists all of the integrations in your domain."
  aws_customer_profiles_info:
    list_integrations: true
    domain_name: 'test'

- name: "Lists all of the template information for object types."
  aws_customer_profiles_info:
    list_profile_object_type_templates: true

- name: "Lists all of the templates available within the service."
  aws_customer_profiles_info:
    domain_name: 'test'
    list_profile_object_types: true

- name: "get information about a specific domain."
  aws_customer_profiles_info:
    domain_name: 'test'
    get_domain: true

- name: "get an integration for a domain."
  aws_customer_profiles_info:
    domain_name: 'test'
    get_integration: true
"""

RETURN = """
domains:
  description: list of connect domains.
  returned: when no arguments are defined and success
  type: list
  sample: [
    {
        'domain_name': 'string',
        'created_at': datetime(2016, 6, 6),
        'last_updated_at': datetime(2015, 1, 1),
        'tags': {
            'string': 'string'
        }
    },
  ]
account_integrations:
  description: Lists all of the integrations associated to a specific URI in the AWS account.
  returned: when `list_account_integrations`, and `uri` are defined and success
  type: list
  sample: [
    {
        'domain_name': 'string',
        'uri': 'string',
        'object_type_name': 'string',
        'created_at': datetime(2016, 6, 6),
        'last_updated_at': datetime(2015, 1, 1),
        'tags': {
            'string': 'string'
        }
    },
  ]
integrations:
  description: Lists all of the integrations in your domain.
  returned: when `list_integrations`, and `domain_name` are defined and success
  type: list
  sample: [
    {
        'domain_name': 'string',
        'uri': 'string',
        'object_type_name': 'string',
        'created_at': datetime(2016, 6, 6),
        'last_updated_at': datetime(2015, 1, 1),
        'tags': {
            'string': 'string'
        }
    },
  ]
profile_object_type_templates:
  description: Lists all of the template information for object types.
  returned: when `list_profile_object_type_templates` is  defined and success
  type: list
  sample: [
    {
        'template_id': 'string',
        'source_name': 'string',
        'source_object': 'string'
    },
  ]
profile_object_types:
  description: Lists all of the templates available within the service.
  returned: when `list_profile_object_types`, and `domain_name` are defined and success
  type: list
  sample: [
    {
        'object_type_name': 'string',
        'description': 'string',
        'created_at': datetime(2016, 6, 6),
        'last_updated_at': datetime(2015, 1, 1),
        'tags': {
            'string': 'string'
        }
    },
  ]
domain:
  description: Returns information about a specific domain.
  returned: when `get_domain`, and `domain_name` are defined and success
  type: dict
  sample: {
    'domain_name': 'string',
    'default_expiration_days': 123,
    'default_encryption_key': 'string',
    'dead_letter_queue_url': 'string',
    'stats': {
        'profile_count': 123,
        'metering_profile_count': 123,
        'object_count': 123,
        'total_size': 123
    },
    'created_at': datetime(2016, 6, 6),
    'last_updated_at': datetime(2015, 1, 1),
    'tags': {
        'string': 'string'
    }
  }
integration:
  description: Returns an integration for a domain.
  returned: when `get_integration`, and `domain_name` are defined and success
  type: dict
  sample: {
    'domain_name': 'string',
    'uri': 'string',
    'object_type_name': 'string',
    'created_at': datetime(2016, 6, 6),
    'last_updated_at': datetime(2015, 1, 1),
    'tags': {
        'string': 'string'
    }
  }
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


def _connect(client, module):
    try:
        if module.params['list_account_integrations']:
            if client.can_paginate('list_account_integrations'):
                paginator = client.get_paginator('list_account_integrations')
                return paginator.paginate(
                    Uri=module.params['uri'],
                ), True
            else:
                return client.list_account_integrations(
                    Uri=module.params['uri'],
                ), False
        elif module.params['list_integrations']:
            if client.can_paginate('list_integrations'):
                paginator = client.get_paginator('list_integrations')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                ), True
            else:
                return client.list_integrations(
                    DomainName=module.params['domain_name'],
                ), False
        elif module.params['list_profile_object_type_templates']:
            if client.can_paginate('list_profile_object_type_templates'):
                paginator = client.get_paginator('list_profile_object_type_templates')
                return paginator.paginate(), True
            else:
                return client.list_profile_object_type_templates(), False
        elif module.params['list_profile_object_types']:
            if client.can_paginate('list_profile_object_types'):
                paginator = client.get_paginator('list_profile_object_types')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                ), True
            else:
                return client.list_profile_object_types(
                    DomainName=module.params['domain_name'],
                ), False
        elif module.params['get_domain']:
            return client.get_domain(
                DomainName=module.params['domain_name'],
            ), False
        elif module.params['get_integration']:
            return client.get_integration(
                DomainName=module.params['domain_name'],
            ), False
        else:
            if client.can_paginate('list_domains'):
                paginator = client.get_paginator('list_domains')
                return paginator.paginate(), True
            else:
                return client.list_domains(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws connect customer profiles details')


def main():
    argument_spec = dict(
        uri=dict(required=False),
        domain_name=dict(required=False),
        list_account_integrations=dict(required=False, type=bool),
        list_integrations=dict(required=False, type=bool),
        list_profile_object_type_templates=dict(required=False, type=bool),
        list_profile_object_types=dict(required=False, type=bool),
        get_domain=dict(required=False, type=bool),
        get_integration=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_account_integrations', True, ['uri']),
            ('list_integrations', True, ['domain_name']),
            ('list_profile_object_types', True, ['domain_name']),
            ('get_domain', True, ['domain_name']),
            ('get_integration', True, ['domain_name']),
        ),
        mutually_exclusive=[
            (
                'list_account_integrations',
                'list_integrations',
                'list_profile_object_type_templates',
                'list_profile_object_types',
                'get_domain',
                'get_integration',
            )
        ],
    )

    client = module.client('customer-profiles', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _connect(client, module)

    if module.params['list_account_integrations']:
        module.exit_json(account_integrations=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['list_integrations']:
        module.exit_json(integrations=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['list_profile_object_type_templates']:
        module.exit_json(profile_object_type_templates=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['list_profile_object_types']:
        module.exit_json(profile_object_types=aws_response_list_parser(paginate, _it, 'Items'))
    elif module.params['get_domain']:
        module.exit_json(domain=camel_dict_to_snake_dict(_it))
    elif module.params['get_integration']:
        module.exit_json(integration=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(domains=aws_response_list_parser(paginate, _it, 'Items'))


if __name__ == '__main__':
    main()
