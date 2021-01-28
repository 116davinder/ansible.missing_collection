#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_elasticbeanstalk_info
short_description: Get Information about AWS Elastic Beanstalk.
description:
  - Get Information about AWS Elastic Beanstalk.
  - U(https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_Operations.html)
version_added: 0.0.6
options:
  name:
    description:
      - can be name of application?
      - can be name of environment?
    required: false
    type: str
  names:
    description:
      - list of application names.
    required: false
    type: list
  describe_application_versions:
    description:
      - do you want to get details of application versions for given application I(name)?
    required: false
    type: bool
  describe_applications:
    description:
      - do you want to get details of applications for given I(names)?
    required: false
    type: bool
  describe_configuration_options:
    description:
      - do you want to get details of configuration options for given application I(name)?
    required: false
    type: bool
  describe_configuration_settings:
    description:
      - do you want to get details of configuration settings for given application I(name)?
    required: false
    type: bool
  describe_environment_health:
    description:
      - do you want to get details of environment health for given environment I(name)?
    required: false
    type: bool
  describe_environment_managed_actions:
    description:
      - do you want to get details of environment managed actions for given environment I(name)?
    required: false
    type: bool
  describe_environment_resources:
    description:
      - do you want to get details of environment resources for given environment I(name)?
    required: false
    type: bool
  describe_events:
    description:
      - do you want to get details of events for given application I(name)?
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
- name: "get list of all environments."
  aws_elasticbeanstalk_info:

- name: "get list of applications."
  aws_elasticbeanstalk_info:
    describe_applications: true
    names: []

- name: "get list of application versions."
  aws_elasticbeanstalk_info:
    describe_application_versions: true
    name: 'test-app'

- name: "get application configuration options."
  aws_elasticbeanstalk_info:
    describe_configuration_options: true
    name: 'test-app'

- name: "get application configuration settings."
  aws_elasticbeanstalk_info:
    describe_configuration_settings: true
    name: 'test-app'

- name: "get details of environment health."
  aws_elasticbeanstalk_info:
    describe_environment_health: true
    name: 'test-env'

- name: "get list of environment managed actions."
  aws_elasticbeanstalk_info:
    describe_environment_managed_actions: true
    name: 'test-env'

- name: "get environment resources."
  aws_elasticbeanstalk_info:
    describe_environment_resources: true
    name: 'test-env'

- name: "get application events."
  aws_elasticbeanstalk_info:
    describe_events: true
    name: 'test-app'
"""

RETURN = """
environments:
  description: list of all environments.
  returned: when no arguments are defined and success
  type: list
application_versions:
  description: list of application versions.
  returned: when `describe_application_versions` is defined and success
  type: list
applications:
  description: list of applications.
  returned: when `describe_applications` is defined and success
  type: list
configuration_options:
  description: application configuration options.
  returned: when `describe_configuration_options` is defined and success
  type: dict
configuration_settings:
  description: application configuration settings.
  returned: when `describe_configuration_settings` is defined and success
  type: dict
environment_health:
  description: details of environment health.
  returned: when `describe_environment_health` is defined and success
  type: list
environment_managed_actions:
  description: list of environment managed actions.
  returned: when `describe_environment_managed_actions` is defined and success
  type: list
environment_resources:
  description: environment resources.
  returned: when `describe_environment_resources` is defined and success
  type: dict
events:
  description: application events.
  returned: when `describe_events` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _elasticbeanstalk(client, module):
    try:
        if module.params['describe_application_versions']:
            if client.can_paginate('describe_application_versions'):
                paginator = client.get_paginator('describe_application_versions')
                return paginator.paginate(
                    ApplicationName=module.params['name'],
                ), True
            else:
                return client.describe_application_versions(
                    ApplicationName=module.params['name'],
                ), False
        elif module.params['describe_applications']:
            if client.can_paginate('describe_applications'):
                paginator = client.get_paginator('describe_applications')
                return paginator.paginate(
                    ApplicationNames=module.params['names'],
                ), True
            else:
                return client.describe_applications(
                    ApplicationNames=module.params['names'],
                ), False
        elif module.params['describe_configuration_options']:
            return client.describe_configuration_options(
                ApplicationName=module.params['name'],
            ), False
        elif module.params['describe_configuration_settings']:
            return client.describe_configuration_options(
                ApplicationName=module.params['name'],
            ), False
        elif module.params['describe_environment_health']:
            return client.describe_environment_health(
                EnvironmentName=module.params['name'],
            ), False
        elif module.params['describe_environment_managed_actions']:
            if client.can_paginate('describe_environment_managed_actions'):
                paginator = client.get_paginator('describe_environment_managed_actions')
                return paginator.paginate(
                    EnvironmentName=module.params['name'],
                ), True
            else:
                return client.describe_environment_managed_actions(
                    EnvironmentName=module.params['name'],
                ), False
        elif module.params['describe_environment_resources']:
            return client.describe_environment_resources(
                EnvironmentName=module.params['name'],
            ), False
        elif module.params['describe_events']:
            if client.can_paginate('describe_events'):
                paginator = client.get_paginator('describe_events')
                return paginator.paginate(
                    ApplicationName=module.params['name'],
                ), True
            else:
                return client.describe_events(
                    ApplicationName=module.params['name'],
                ), False
        else:
            if client.can_paginate('describe_environments'):
                paginator = client.get_paginator('describe_environments')
                return paginator.paginate(), True
            else:
                return client.describe_environments(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Elastic Beanstalk details')


def main():
    argument_spec = dict(
        name=dict(required=False),
        names=dict(required=False, type=list),
        describe_application_versions=dict(required=False, type=bool),
        describe_applications=dict(required=False, type=bool),
        describe_configuration_options=dict(required=False, type=bool),
        describe_configuration_settings=dict(required=False, type=bool),
        describe_environment_health=dict(required=False, type=bool),
        describe_environment_managed_actions=dict(required=False, type=bool),
        describe_environment_resources=dict(required=False, type=bool),
        describe_events=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_application_versions', True, ['name']),
            ('describe_applications', True, ['names']),
            ('describe_configuration_options', True, ['name']),
            ('describe_configuration_settings', True, ['name']),
            ('describe_environment_health', True, ['name']),
            ('describe_environment_managed_actions', True, ['name']),
            ('describe_environment_resources', True, ['name']),
            ('describe_events', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'describe_application_versions',
                'describe_applications',
                'describe_configuration_options',
                'describe_configuration_settings',
                'describe_environment_health',
                'describe_environment_managed_actions',
                'describe_environment_resources',
                'describe_events',
            )
        ],
    )

    client = module.client('elasticbeanstalk', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _elasticbeanstalk(client, module)

    if module.params['describe_application_versions']:
        module.exit_json(application_versions=aws_response_list_parser(paginate, it, 'ApplicationVersions'))
    elif module.params['describe_applications']:
        module.exit_json(applications=aws_response_list_parser(paginate, it, 'Applications'))
    elif module.params['describe_configuration_options']:
        module.exit_json(configuration_options=camel_dict_to_snake_dict(it))
    elif module.params['describe_configuration_settings']:
        module.exit_json(configuration_settings=camel_dict_to_snake_dict(it['ConfigurationSettings']))
    elif module.params['describe_environment_health']:
        module.exit_json(environment_health=camel_dict_to_snake_dict(it))
    elif module.params['describe_environment_managed_actions']:
        module.exit_json(environment_managed_actions=aws_response_list_parser(paginate, it, 'ManagedActions'))
    elif module.params['describe_environment_resources']:
        module.exit_json(environment_resources=camel_dict_to_snake_dict(it['EnvironmentResources']))
    elif module.params['describe_events']:
        module.exit_json(events=aws_response_list_parser(paginate, it, 'Events'))
    else:
        module.exit_json(environments=aws_response_list_parser(paginate, it, 'Environments'))


if __name__ == '__main__':
    main()
