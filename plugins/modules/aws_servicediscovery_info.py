#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_servicediscovery_info
short_description: Get Information about AWS Cloud Map (ServiceDiscovery).
description:
  - Get Information about AWS Cloud Map (ServiceDiscovery).
  - U(https://docs.aws.amazon.com/cloud-map/latest/api/API_Operations.html)
version_added: 0.0.9
options:
  id:
    description:
      - can be service id?
      - can be namespace id?
    required: false
    type: str
    aliases: ['service_id', 'namespace_id']
  list_instances:
    description:
      - do you want to get list of instances for given service I(id)?
    required: false
    type: bool
  list_namespaces:
    description:
      - do you want to get namespaces?
    required: false
    type: bool
  list_services:
    description:
      - do you want to get list of services for given namespace I(id)?
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
- name: "get list of instances"
  aws_servicediscovery_info:
    list_instances: true
    id: 'service_id'

- name: "get list of namespaces"
  aws_servicediscovery_info:
    list_namespaces: true

- name: "get list of services"
  aws_servicediscovery_info:
    list_services: true
    id: 'namespace_id'
"""

RETURN = """
instances:
  description: list of instances.
  returned: when `list_instances` is defined and success.
  type: list
namespaces:
  description: list of namespaces.
  returned: when `list_namespaces` is defined and success.
  type: list
services:
  description: list of services.
  returned: when `list_services` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _servicediscovery(client, module):
    try:
        if module.params['list_instances']:
            if client.can_paginate('list_instances'):
                paginator = client.get_paginator('list_instances')
                return paginator.paginate(
                    ServiceId=module.params['id']
                ), True
            else:
                return client.list_instances(
                    ServiceId=module.params['id']
                ), False
        elif module.params['list_namespaces']:
            if client.can_paginate('list_namespaces'):
                paginator = client.get_paginator('list_namespaces')
                return paginator.paginate(), True
            else:
                return client.list_namespaces(), False
        elif module.params['list_services']:
            if client.can_paginate('list_services'):
                paginator = client.get_paginator('list_services')
                return paginator.paginate(
                    Filters=[
                        {
                            'Name': 'NAMESPACE_ID',
                            'Values': [module.params['id']],
                            'Condition': 'EQ'
                        },
                    ]
                ), True
            else:
                return client.list_services(
                    Filters=[
                        {
                            'Name': 'NAMESPACE_ID',
                            'Values': [module.params['id']],
                            'Condition': 'EQ'
                        },
                    ]
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Cloud Map details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['service_id', 'namespace_id']),
        list_instances=dict(required=False, type=bool),
        list_namespaces=dict(required=False, type=bool),
        list_services=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_instances', True, ['id']),
            ('list_services', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_instances',
                'list_namespaces',
                'list_services',
            )
        ],
    )

    client = module.client('servicediscovery', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _servicediscovery(client, module)

    if module.params['list_instances']:
        module.exit_json(instances=aws_response_list_parser(paginate, it, 'Instances'))
    elif module.params['list_namespaces']:
        module.exit_json(namespaces=aws_response_list_parser(paginate, it, 'Namespaces'))
    elif module.params['list_services']:
        module.exit_json(services=aws_response_list_parser(paginate, it, 'Services'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
