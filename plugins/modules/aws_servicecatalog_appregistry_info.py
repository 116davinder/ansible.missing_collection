#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_servicecatalog_appregistry_info
short_description: Get Information about AWS Service Catalog App Registry.
description:
  - Get Information about AWS Service Catalog App Registry.
  - U(https://docs.aws.amazon.com/servicecatalog_appregistry/1.0/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  id:
    description:
      - application id.
    required: false
    type: str
    aliases: ['application_id']
  list_applications:
    description:
      - do you want to get list of applications?
    required: false
    type: bool
  list_associated_attribute_groups:
    description:
      - do you want to get associated_attribute_groups for given I(id)?
    required: false
    type: bool
  list_associated_resources:
    description:
      - do you want to get list of associated_resources for given I(id)?
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
- name: "get list of applications"
  aws_servicecatalog_appregistry_info:
    list_applications: true

- name: "get associated_attribute_groups"
  aws_servicecatalog_appregistry_info:
    list_associated_attribute_groups: true
    id: 'application_id'

- name: "get list of associated_resources"
  aws_servicecatalog_appregistry_info:
    list_associated_resources: true
    id: 'application_id'
"""

RETURN = """
applications:
  description: list of applications.
  returned: when `list_applications` is defined and success.
  type: list
associated_attribute_groups:
  description: get of associated_attribute_groups.
  returned: when `list_associated_attribute_groups` is defined and success.
  type: list
associated_resources:
  description: list of associated_resources.
  returned: when `list_associated_resources` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _servicecatalog_appregistry(client, module):
    try:
        if module.params['list_applications']:
            if client.can_paginate('list_applications'):
                paginator = client.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return client.list_applications(), False
        elif module.params['list_associated_attribute_groups']:
            if client.can_paginate('list_associated_attribute_groups'):
                paginator = client.get_paginator('list_associated_attribute_groups')
                return paginator.paginate(
                    application=module.params['id']
                ), True
            else:
                return client.list_associated_attribute_groups(
                    application=module.params['id']
                ), False
        elif module.params['list_associated_resources']:
            if client.can_paginate('list_associated_resources'):
                paginator = client.get_paginator('list_associated_resources')
                return paginator.paginate(
                    application=module.params['id']
                ), True
            else:
                return client.list_associated_resources(
                    application=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Service Catalog App Registry details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['application_id']),
        list_applications=dict(required=False, type=bool),
        list_associated_attribute_groups=dict(required=False, type=bool),
        list_associated_resources=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_associated_attribute_groups', True, ['id']),
            ('list_associated_resources', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_applications',
                'list_associated_attribute_groups',
                'list_associated_resources',
            )
        ],
    )

    client = module.client('servicecatalog-appregistry', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _servicecatalog_appregistry(client, module)

    if module.params['list_applications']:
        module.exit_json(applications=aws_response_list_parser(paginate, it, 'applications'))
    elif module.params['list_associated_attribute_groups']:
        module.exit_json(associated_attribute_groups=aws_response_list_parser(paginate, it, 'attributeGroups'))
    elif module.params['list_associated_resources']:
        module.exit_json(associated_resources=aws_response_list_parser(paginate, it, 'resources'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
