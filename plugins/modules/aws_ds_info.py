#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_ds_info
short_description: Get Information about AWS Directory Service.
description:
  - Get Information about AWS Directory Service.
  - U(https://docs.aws.amazon.com/directoryservice/latest/devguide/API_Operations.html)
version_added: 0.0.5
options:
  id:
    description:
      - id of directory.
    required: false
    type: str
  describe_directories:
    description:
      - do you want to describe all directories?
    required: false
    type: bool
  list_certificates:
    description:
      - do you want to get list of certificates for given I(id)?
    required: false
    type: bool
  list_ip_routes:
    description:
      - do you want to get list of ip routes for given I(id)?
    required: false
    type: bool
  list_log_subscriptions:
    description:
      - do you want to get list of log subscriptions for given I(id)?
    required: false
    type: bool
  list_schema_extensions:
    description:
      - do you want to get list of schema extensions for given I(id)?
    required: false
    type: bool
  describe_conditional_forwarders:
    description:
      - do you want to describe conditional forwarders for given I(id)?
    required: false
    type: bool
  describe_domain_controllers:
    description:
      - do you want to describe domain controllers for given I(id)?
    required: false
    type: bool
  describe_event_topics:
    description:
      - do you want to describe event topics for given I(id)?
    required: false
    type: bool
  describe_snapshots:
    description:
      - do you want to describe snapshots for given I(id)?
    required: false
    type: bool
  describe_trusts:
    description:
      - do you want to describe trusts for given I(id)?
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
- name: "describe all directories"
  aws_ds_info:
    describe_directories: true

- name: "get list of certificates"
  aws_ds_info:
    list_certificates: true
    id: 'test-id'

- name: "get list of ip routes"
  aws_ds_info:
    list_ip_routes: true
    id: 'test-id'

- name: "get list of log subscriptions"
  aws_ds_info:
    list_log_subscriptions: true
    id: 'test-id'

- name: "get list of schema extensions"
  aws_ds_info:
    list_schema_extensions: true
    id: 'test-id'

- name: "describe domain controllers"
  aws_ds_info:
    describe_conditional_forwarders: true
    id: 'test-id'

- name: "describe event topics"
  aws_ds_info:
    describe_event_topics: true
    id: 'test-id'

- name: "describe snapshots"
  aws_ds_info:
    describe_snapshots: true
    id: 'test-id'

- name: "describe trusts"
  aws_ds_info:
    describe_trusts: true
    id: 'test-id'
"""

RETURN = """
directories:
  description: list of directories.
  returned: when `describe_directories` is defined and success
  type: list
certificates:
  description: list of certificates.
  returned: when `describe_certificates` is defined and success
  type: list
ip_routes:
  description: list of ip routes.
  returned: when `list_ip_routes` is defined and success
  type: list
log_subscriptions:
  description: list of log subscriptions.
  returned: when `list_log_subscriptions` is defined and success
  type: list
schema_extensions:
  description: list of schema extensions.
  returned: when `list_schema_extensions` is defined and success
  type: list
conditional_forwarders:
  description: list of conditional forwarders.
  returned: when `describe_conditional_forwarders` is defined and success
  type: list
domain_controllers:
  description: list of domain controllers.
  returned: when `describe_domain_controllers` is defined and success
  type: list
event_topics:
  description: list of event topics.
  returned: when `describe_event_topics` is defined and success
  type: list
snapshots:
  description: list of snapshots.
  returned: when `describe_snapshots` is defined and success
  type: list
trusts:
  description: list of trusts.
  returned: when `describe_trusts` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _ds(client, module):
    try:
        if module.params['describe_directories']:
            if client.can_paginate('describe_directories'):
                paginator = client.get_paginator('describe_directories')
                return paginator.paginate(), True
            else:
                return client.describe_directories(), False
        elif module.params['list_certificates']:
            if client.can_paginate('list_certificates'):
                paginator = client.get_paginator('list_certificates')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.list_certificates(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['list_ip_routes']:
            if client.can_paginate('list_ip_routes'):
                paginator = client.get_paginator('list_ip_routes')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.list_ip_routes(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['list_log_subscriptions']:
            if client.can_paginate('list_log_subscriptions'):
                paginator = client.get_paginator('list_log_subscriptions')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.list_log_subscriptions(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['list_schema_extensions']:
            if client.can_paginate('list_schema_extensions'):
                paginator = client.get_paginator('list_schema_extensions')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.list_schema_extensions(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['describe_conditional_forwarders']:
            if client.can_paginate('describe_conditional_forwarders'):
                paginator = client.get_paginator('describe_conditional_forwarders')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.describe_conditional_forwarders(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['describe_domain_controllers']:
            if client.can_paginate('describe_domain_controllers'):
                paginator = client.get_paginator('describe_domain_controllers')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.describe_domain_controllers(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['describe_event_topics']:
            if client.can_paginate('describe_event_topics'):
                paginator = client.get_paginator('describe_event_topics')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.describe_event_topics(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['describe_snapshots']:
            if client.can_paginate('describe_snapshots'):
                paginator = client.get_paginator('describe_snapshots')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.describe_snapshots(
                    DirectoryId=module.params['id'],
                ), False
        elif module.params['describe_trusts']:
            if client.can_paginate('describe_trusts'):
                paginator = client.get_paginator('describe_trusts')
                return paginator.paginate(
                    DirectoryId=module.params['id'],
                ), True
            else:
                return client.describe_trusts(
                    DirectoryId=module.params['id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Directory Service details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['directory_id']),
        describe_directories=dict(required=False, type=bool),
        list_certificates=dict(required=False, type=bool),
        list_ip_routes=dict(required=False, type=bool),
        list_log_subscriptions=dict(required=False, type=bool),
        list_schema_extensions=dict(required=False, type=bool),
        describe_conditional_forwarders=dict(required=False, type=bool),
        describe_domain_controllers=dict(required=False, type=bool),
        describe_event_topics=dict(required=False, type=bool),
        describe_snapshots=dict(required=False, type=bool),
        describe_trusts=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_certificates', True, ['id']),
            ('list_ip_routes', True, ['id']),
            ('list_log_subscriptions', True, ['id']),
            ('list_schema_extensions', True, ['id']),
            ('describe_conditional_forwarders', True, ['id']),
            ('describe_domain_controllers', True, ['id']),
            ('describe_event_topics', True, ['id']),
            ('describe_snapshots', True, ['id']),
            ('describe_trusts', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'describe_directories',
                'list_certificates',
                'list_ip_routes',
                'list_log_subscriptions',
                'list_schema_extensions',
                'describe_conditional_forwarders',
                'describe_domain_controllers',
                'describe_event_topics',
                'describe_snapshots',
                'describe_trusts',
            )
        ],
    )

    client = module.client('ds', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _ds(client, module)

    if module.params['describe_directories']:
        module.exit_json(directories=aws_response_list_parser(paginate, it, 'DirectoryDescriptions'))
    elif module.params['list_certificates']:
        module.exit_json(certificates=aws_response_list_parser(paginate, it, 'CertificatesInfo'))
    elif module.params['list_ip_routes']:
        module.exit_json(ip_routes=aws_response_list_parser(paginate, it, 'IpRoutesInfo'))
    elif module.params['list_log_subscriptions']:
        module.exit_json(log_subscriptions=aws_response_list_parser(paginate, it, 'LogSubscriptions'))
    elif module.params['list_schema_extensions']:
        module.exit_json(schema_extensions=aws_response_list_parser(paginate, it, 'SchemaExtensionsInfo'))
    elif module.params['describe_conditional_forwarders']:
        module.exit_json(conditional_forwarders=aws_response_list_parser(paginate, it, 'ConditionalForwarders'))
    elif module.params['describe_domain_controllers']:
        module.exit_json(domain_controllers=aws_response_list_parser(paginate, it, 'DomainControllers'))
    elif module.params['describe_event_topics']:
        module.exit_json(event_topics=aws_response_list_parser(paginate, it, 'EventTopics'))
    elif module.params['describe_snapshots']:
        module.exit_json(snapshots=aws_response_list_parser(paginate, it, 'Snapshots'))
    elif module.params['describe_trusts']:
        module.exit_json(trusts=aws_response_list_parser(paginate, it, 'Trusts'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
