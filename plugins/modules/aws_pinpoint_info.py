#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_pinpoint_info
short_description: Get Information about Amazon Pinpoint.
description:
  - Get Information about Amazon Pinpoint.
  - U(https://docs.aws.amazon.com/pinpoint/latest/apireference/resources.html)
version_added: 0.0.8
options:
  id:
    description:
      - id of application.
    required: false
    type: str
    aliases: ['application_id']
  get_adm_channel:
    description:
      - do you want to get adm_channel for given application I(id)?
    required: false
    type: bool
  get_apns_channel:
    description:
      - do you want to get apns_channel for given application I(id)?
    required: false
    type: bool
  get_application_settings:
    description:
      - do you want to get application_settings for given application I(id)?
    required: false
    type: bool
  get_apps:
    description:
      - do you want to get apps?
    required: false
    type: bool
  get_baidu_channel:
    description:
      - do you want to get baidu_channel for given application I(id)?
    required: false
    type: bool
  get_campaigns:
    description:
      - do you want to get campaigns for given application I(id)?
    required: false
    type: bool
  get_export_jobs:
    description:
      - do you want to get export_jobs for given application I(id)?
    required: false
    type: bool
  get_import_jobs:
    description:
      - do you want to get import_jobs for given application I(id)?
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
- name: "get adm_channel"
  aws_pinpoint_info:
    get_adm_channel: true
    id: 'application-id'

- name: "get apns_channel"
  aws_pinpoint_info:
    get_apns_channel: true
    id: 'application-id'

- name: "get application_settings"
  aws_pinpoint_info:
    get_application_settings: true
    id: 'application-id'

- name: "get list of apps"
  aws_pinpoint_info:
    get_apps: true

- name: "get baidu_channel"
  aws_pinpoint_info:
    get_baidu_channel: true
    id: 'application-id'

- name: "get list of campaigns"
  aws_pinpoint_info:
    get_campaigns: true
    id: 'application-id'

- name: "get export jobs"
  aws_pinpoint_info:
    get_export_jobs: true
    id: 'application-id'

- name: "get import jobs"
  aws_pinpoint_info:
    get_import_jobs: true
    id: 'application-id'
"""

RETURN = """
adm_channel:
  description: list of adm_channel.
  returned: when `get_adm_channel` is defined and success.
  type: dict
apns_channel:
  description: get of apns_channel.
  returned: when `get_apns_channel` is defined and success.
  type: dict
application_settings:
  description: list of application_settings.
  returned: when `get_application_settings` is defined and success.
  type: dict
apps:
  description: list of apps.
  returned: when `get_apps` is defined and success.
  type: list
baidu_channel:
  description: list of baidu_channel.
  returned: when `get_baidu_channel` is defined and success.
  type: dict
campaigns:
  description: list of campaigns.
  returned: when `get_campaigns` is defined and success.
  type: list
export_jobs:
  description: list of export_jobs.
  returned: when `get_export_jobs` is defined and success.
  type: list
import_jobs:
  description: list of import_jobs.
  returned: when `get_import_jobs` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_nested_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _pinpoint(client, module):
    try:
        if module.params['get_adm_channel']:
            return client.get_adm_channel(
                ApplicationId=module.params['id']
            ), False
        elif module.params['get_apns_channel']:
            return client.get_apns_channel(
                ApplicationId=module.params['id']
            ), False
        elif module.params['get_application_settings']:
            return client.get_application_settings(
                ApplicationId=module.params['id']
            ), False
        elif module.params['get_apps']:
            if client.can_paginate('get_apps'):
                paginator = client.get_paginator('get_apps')
                return paginator.paginate(), True
            else:
                return client.get_apps(), False
        elif module.params['get_baidu_channel']:
            return client.get_baidu_channel(
                ApplicationId=module.params['id']
            ), False
        elif module.params['get_campaigns']:
            if client.can_paginate('get_campaigns'):
                paginator = client.get_paginator('get_campaigns')
                return paginator.paginate(
                    ApplicationId=module.params['id']
                ), True
            else:
                return client.get_campaigns(
                    ApplicationId=module.params['id']
                ), False
        elif module.params['get_export_jobs']:
            if client.can_paginate('get_export_jobs'):
                paginator = client.get_paginator('get_export_jobs')
                return paginator.paginate(
                    ApplicationId=module.params['id']
                ), True
            else:
                return client.get_export_jobs(
                    ApplicationId=module.params['id']
                ), False
        elif module.params['get_import_jobs']:
            if client.can_paginate('get_import_jobs'):
                paginator = client.get_paginator('get_import_jobs')
                return paginator.paginate(
                    ApplicationId=module.params['id']
                ), True
            else:
                return client.get_import_jobs(
                    ApplicationId=module.params['id']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Pinpoint details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['application_id']),
        get_adm_channel=dict(required=False, type=bool),
        get_apns_channel=dict(required=False, type=bool),
        get_application_settings=dict(required=False, type=bool),
        get_apps=dict(required=False, type=bool),
        get_baidu_channel=dict(required=False, type=bool),
        get_campaigns=dict(required=False, type=bool),
        get_export_jobs=dict(required=False, type=bool),
        get_import_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_adm_channel', True, ['id']),
            ('get_apns_channel', True, ['id']),
            ('get_apps', True, ['id']),
            ('get_baidu_channel', True, ['id']),
            ('get_campaigns', True, ['id']),
            ('get_export_jobs', True, ['id']),
            ('get_import_jobs', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'get_adm_channel',
                'get_apns_channel',
                'get_application_settings',
                'get_apps',
                'get_baidu_channel',
                'get_campaigns',
                'get_export_jobs',
                'get_import_jobs',
            )
        ],
    )

    client = module.client('pinpoint', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _pinpoint(client, module)

    if module.params['get_adm_channel']:
        module.exit_json(adm_channel=camel_dict_to_snake_dict(it['ADMChannelResponse']))
    elif module.params['get_apns_channel']:
        module.exit_json(apns_channel=camel_dict_to_snake_dict(it['APNSChannelResponse']))
    elif module.params['get_application_settings']:
        module.exit_json(application_settings=camel_dict_to_snake_dict(it))
    elif module.params['get_apps']:
        module.exit_json(apps=aws_response_nested_list_parser(paginate, it, 'ApplicationsResponse', 'Item'))
    elif module.params['get_baidu_channel']:
        module.exit_json(baidu_channel=camel_dict_to_snake_dict(it['BaiduChannelResponse']))
    elif module.params['get_campaigns']:
        module.exit_json(campaigns=aws_response_nested_list_parser(paginate, it, 'CampaignsResponse', 'Item'))
    elif module.params['get_export_jobs']:
        module.exit_json(export_jobs=aws_response_nested_list_parser(paginate, it, 'ExportJobsResponse', 'Item'))
    elif module.params['get_import_jobs']:
        module.exit_json(import_jobs=aws_response_nested_list_parser(paginate, it, 'ImportJobsResponse', 'Item'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
