#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_devicefarm_info
short_description: Get Information about AWS Device Farm.
description:
  - Get Information about AWS Device Farm.
  - U(https://docs.aws.amazon.com/devicefarm/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  arn:
    description:
      - can be arn of the run, job, suite, or test ARN?
      - can be arn of the project?
      - can be arn of the session?
    required: false
    type: str
  artifact_type:
    description:
      -  type of artifact.
    required: false
    type: str
    choices: ['SCREENSHOT', 'FILE', 'LOG']
    default: 'FILE'
  device_pool_type:
    description:
      -  type of device pool.
    required: false
    type: str
    choices: ['CURATED', 'PRIVATE']
    default: 'CURATED'
  network_profile_type:
    description:
      -  type of network profile.
    required: false
    type: str
    choices: ['CURATED', 'PRIVATE']
    default: 'CURATED'
  test_grid_session_status:
    description:
      -  status of test grid session.
    required: false
    type: str
    choices: ['ACTIVE', 'CLOSED', 'ERRORED']
    default: 'ACTIVE'
  list_artifacts:
    description:
      - do you want to get list of artifacts of given I(arn)?
    required: false
    type: bool
  list_device_instances:
    description:
      - do you want to get list device instances?
    required: false
    type: bool
  list_device_pools:
    description:
      - do you want to get list of device pools of given I(arn) and I(device_pool_type)?
    required: false
    type: bool
  list_devices:
    description:
      - do you want to get list of devices of given I(arn)?
    required: false
    type: bool
  list_instance_profiles:
    description:
      - do you want to get list of instance profiles?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs of given I(arn)?
    required: false
    type: bool
  list_network_profiles:
    description:
      - do you want to get list of network profiles of given I(arn) and I(network_profile_type)?
    required: false
    type: bool
  list_offering_promotions:
    description:
      - do you want to get list of offering promotions?
    required: false
    type: bool
  list_offering_transactions:
    description:
      - do you want to get list of offering transactions?
    required: false
    type: bool
  list_offerings:
    description:
      - do you want to get list of offerings?
    required: false
    type: bool
  list_remote_access_sessions:
    description:
      - do you want to get list of remote access sessions of given I(arn)?
    required: false
    type: bool
  list_runs:
    description:
      - do you want to get list of runs of given I(arn)?
    required: false
    type: bool
  list_samples:
    description:
      - do you want to get list of samples of given I(arn)?
    required: false
    type: bool
  list_suites:
    description:
      - do you want to get list of suites of given I(arn)?
    required: false
    type: bool
  list_test_grid_projects:
    description:
      - do you want to get list of test grid projects?
    required: false
    type: bool
  list_test_grid_session_actions:
    description:
      - do you want to get list of test grid session actions of given I(arn)?
    required: false
    type: bool
  list_test_grid_session_artifacts:
    description:
      - do you want to get list of test grid session artifacts of given I(arn)?
    required: false
    type: bool
  list_test_grid_sessions:
    description:
      - do you want to get list of test grid sessions of given I(arn) and I(test_grid_session_status)?
    required: false
    type: bool
  list_tests:
    description:
      - do you want to get list of tests of given I(arn)?
    required: false
    type: bool
  list_uploads:
    description:
      - do you want to get list of uploads of given I(arn)?
    required: false
    type: bool
  list_vpce_configurations:
    description:
      - do you want to get list of vpce configurations?
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
- name: "Lists all the projects."
  aws_devicefarm_info:

- name: "Lists all of artifacts"
  aws_devicefarm_info:
    list_artifacts: true
    arn: 'test-arn'
    artifact_type: 'FILE'

- name: "Lists all of device instances"
  aws_devicefarm_info:
    list_device_instances: true

- name: "Lists all of device pools"
  aws_devicefarm_info:
    list_device_pools: true
    arn: 'test-arn'
    device_pool_type: 'CURATED'

- name: "Lists all of devices"
  aws_devicefarm_info:
    list_devices: true
    arn: 'test-arn'

- name: "Lists all of jobs"
  aws_devicefarm_info:
    list_jobs: true
    arn: 'test-arn'

- name: "Lists all of network profiles"
  aws_devicefarm_info:
    list_network_profiles: true
    arn: 'test-arn'
    network_profile_type: 'CURATED'

- name: "Lists all of offering promotions"
  aws_devicefarm_info:
    list_offering_promotions: true

- name: "Lists all of offering transactions"
  aws_devicefarm_info:
    list_offering_transactions: true

- name: "Lists all of offerings"
  aws_devicefarm_info:
    list_offerings: true

- name: "Lists all of remote access sessions"
  aws_devicefarm_info:
    list_remote_access_sessions: true
    arn: 'test-arn'

- name: "Lists all of runs"
  aws_devicefarm_info:
    list_runs: true
    arn: 'test-arn'

- name: "Lists all of samples"
  aws_devicefarm_info:
    list_samples: true
    arn: 'test-arn'

- name: "Lists all of suites"
  aws_devicefarm_info:
    list_suites: true
    arn: 'test-arn'

- name: "Lists all of test grid projects"
  aws_devicefarm_info:
    list_test_grid_projects: true

- name: "Lists all of test grid session actions"
  aws_devicefarm_info:
    list_test_grid_session_actions: true
    arn: 'test-session-arn'

- name: "Lists all of test grid session artifacts"
  aws_devicefarm_info:
    list_test_grid_session_artifacts: true
    arn: 'test-session-arn'

- name: "Lists all of test grid sessions"
  aws_devicefarm_info:
    list_test_grid_sessions: true
    arn: 'test-arn'
    test_grid_session_status: 'ACTIVE'

- name: "Lists all of tests"
  aws_devicefarm_info:
    list_tests: true
    arn: 'test-arn'

- name: "Lists all of uploads"
  aws_devicefarm_info:
    list_uploads: true
    arn: 'test-arn'

- name: "Lists all of vpce configurations"
  aws_devicefarm_info:
    list_vpce_configurations: true
"""

RETURN = """
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


def _devicefarm(client, module):
    try:
        if module.params['list_artifacts']:
            if client.can_paginate('list_artifacts'):
                paginator = client.get_paginator('list_artifacts')
                return paginator.paginate(
                    arn=module.params['arn'],
                    type=module.params['artifact_type'],
                ), True
            else:
                return client.list_artifacts(
                    arn=module.params['arn'],
                    type=module.params['artifact_type'],
                ), False
        elif module.params['list_device_instances']:
            if client.can_paginate('list_device_instances'):
                paginator = client.get_paginator('list_device_instances')
                return paginator.paginate(), True
            else:
                return client.list_device_instances(), False
        elif module.params['list_device_pools']:
            if client.can_paginate('list_device_pools'):
                paginator = client.get_paginator('list_device_pools')
                return paginator.paginate(
                    arn=module.params['arn'],
                    type=module.params['device_pool_type'],
                ), True
            else:
                return client.list_device_pools(
                    arn=module.params['arn'],
                    type=module.params['device_pool_type'],
                ), False
        elif module.params['list_devices']:
            if client.can_paginate('list_devices'):
                paginator = client.get_paginator('list_devices')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_devices(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_instance_profiles']:
            if client.can_paginate('list_instance_profiles'):
                paginator = client.get_paginator('list_instance_profiles')
                return paginator.paginate(), True
            else:
                return client.list_instance_profiles(), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_jobs(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_network_profiles']:
            if client.can_paginate('list_network_profiles'):
                paginator = client.get_paginator('list_network_profiles')
                return paginator.paginate(
                    arn=module.params['arn'],
                    type=module.params['network_profile_type'],
                ), True
            else:
                return client.list_network_profiles(
                    arn=module.params['arn'],
                    type=module.params['network_profile_type'],
                ), False
        elif module.params['list_offering_promotions']:
            if client.can_paginate('list_offering_promotions'):
                paginator = client.get_paginator('list_offering_promotions')
                return paginator.paginate(), True
            else:
                return client.list_offering_promotions(), False
        elif module.params['list_offering_transactions']:
            if client.can_paginate('list_offering_transactions'):
                paginator = client.get_paginator('list_offering_transactions')
                return paginator.paginate(), True
            else:
                return client.list_offering_transactions(), False
        elif module.params['list_offerings']:
            if client.can_paginate('list_offerings'):
                paginator = client.get_paginator('list_offerings')
                return paginator.paginate(), True
            else:
                return client.list_offerings(), False
        elif module.params['list_remote_access_sessions']:
            if client.can_paginate('list_remote_access_sessions'):
                paginator = client.get_paginator('list_remote_access_sessions')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_remote_access_sessions(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_runs']:
            if client.can_paginate('list_runs'):
                paginator = client.get_paginator('list_runs')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_runs(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_samples']:
            if client.can_paginate('list_samples'):
                paginator = client.get_paginator('list_samples')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_samples(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_suites']:
            if client.can_paginate('list_suites'):
                paginator = client.get_paginator('list_suites')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_suites(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_test_grid_projects']:
            if client.can_paginate('list_test_grid_projects'):
                paginator = client.get_paginator('list_test_grid_projects')
                return paginator.paginate(), True
            else:
                return client.list_test_grid_projects(), False
        elif module.params['list_test_grid_session_actions']:
            if client.can_paginate('list_test_grid_session_actions'):
                paginator = client.get_paginator('list_test_grid_session_actions')
                return paginator.paginate(
                    sessionArn=module.params['arn'],
                ), True
            else:
                return client.list_test_grid_session_actions(
                    sessionArn=module.params['arn'],
                ), False
        elif module.params['list_test_grid_session_artifacts']:
            if client.can_paginate('list_test_grid_session_artifacts'):
                paginator = client.get_paginator('list_test_grid_session_artifacts')
                return paginator.paginate(
                    sessionArn=module.params['arn'],
                ), True
            else:
                return client.list_test_grid_session_artifacts(
                    sessionArn=module.params['arn'],
                ), False
        elif module.params['list_test_grid_sessions']:
            if client.can_paginate('list_test_grid_sessions'):
                paginator = client.get_paginator('list_test_grid_sessions')
                return paginator.paginate(
                    projectArn=module.params['arn'],
                    status=module.params['test_grid_session_status'],
                ), True
            else:
                return client.list_test_grid_sessions(
                    projectArn=module.params['arn'],
                    status=module.params['test_grid_session_status'],
                ), False
        elif module.params['list_tests']:
            if client.can_paginate('list_tests'):
                paginator = client.get_paginator('list_tests')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_tests(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_uploads']:
            if client.can_paginate('list_uploads'):
                paginator = client.get_paginator('list_uploads')
                return paginator.paginate(
                    arn=module.params['arn'],
                ), True
            else:
                return client.list_uploads(
                    arn=module.params['arn'],
                ), False
        elif module.params['list_vpce_configurations']:
            if client.can_paginate('list_vpce_configurations'):
                paginator = client.get_paginator('list_vpce_configurations')
                return paginator.paginate(), True
            else:
                return client.list_vpce_configurations(), False
        else:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(), True
            else:
                return client.list_projects(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Device Farm details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        artifact_type=dict(required=False, choices=['SCREENSHOT', 'FILE', 'LOG'], default='FILE'),
        device_pool_type=dict(required=False, choices=['CURATED', 'PRIVATE'], default='CURATED'),
        network_profile_type=dict(required=False, choices=['CURATED', 'PRIVATE'], default='CURATED'),
        test_grid_session_status=dict(required=False, choices=['ACTIVE', 'CLOSED', 'ERRORED'], default='ACTIVE'),
        list_artifacts=dict(required=False, type=bool),
        list_device_instances=dict(required=False, type=bool),
        list_device_pools=dict(required=False, type=bool),
        list_devices=dict(required=False, type=bool),
        list_instance_profiles=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
        list_network_profiles=dict(required=False, type=bool),
        list_offering_promotions=dict(required=False, type=bool),
        list_offering_transactions=dict(required=False, type=bool),
        list_offerings=dict(required=False, type=bool),
        list_remote_access_sessions=dict(required=False, type=bool),
        list_runs=dict(required=False, type=bool),
        list_samples=dict(required=False, type=bool),
        list_suites=dict(required=False, type=bool),
        list_test_grid_projects=dict(required=False, type=bool),
        list_test_grid_session_actions=dict(required=False, type=bool),
        list_test_grid_session_artifacts=dict(required=False, type=bool),
        list_test_grid_sessions=dict(required=False, type=bool),
        list_tests=dict(required=False, type=bool),
        list_uploads=dict(required=False, type=bool),
        list_vpce_configurations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_artifacts', True, ['arn']),
            ('list_device_pools', True, ['arn']),
            ('list_devices', True, ['arn']),
            ('list_jobs', True, ['arn']),
            ('list_network_profiles', True, ['arn']),
            ('list_remote_access_sessions', True, ['arn']),
            ('list_runs', True, ['arn']),
            ('list_samples', True, ['arn']),
            ('list_suites', True, ['arn']),
            ('list_test_grid_session_actions', True, ['arn']),
            ('list_test_grid_session_artifacts', True, ['arn']),
            ('list_test_grid_sessions', True, ['arn']),
            ('list_tests', True, ['arn']),
            ('list_uploads', True, ['arn']),
        ),
        mutually_exclusive=[
            (
                'list_artifacts',
                'list_device_instances',
                'list_device_pools',
                'list_devices',
                'list_instance_profiles',
                'list_jobs',
                'list_network_profiles',
                'list_offering_promotions',
                'list_offering_transactions',
                'list_offerings',
                'list_remote_access_sessions',
                'list_runs',
                'list_samples',
                'list_suites',
                'list_test_grid_projects',
                'list_test_grid_session_actions',
                'list_test_grid_session_artifacts',
                'list_test_grid_sessions',
                'list_tests',
                'list_uploads',
                'list_vpce_configurations',
            )
        ],
    )

    client = module.client('devicefarm', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _devicefarm(client, module)

    if module.params['list_artifacts']:
        module.exit_json(artifacts=aws_response_list_parser(paginate, it, 'artifacts'))
    elif module.params['list_device_instances']:
        module.exit_json(device_instances=aws_response_list_parser(paginate, it, 'deviceInstances'))
    elif module.params['list_device_pools']:
        module.exit_json(device_pools=aws_response_list_parser(paginate, it, 'devicePools'))
    elif module.params['list_devices']:
        module.exit_json(devices=aws_response_list_parser(paginate, it, 'devices'))
    elif module.params['list_instance_profiles']:
        module.exit_json(instance_profiles=aws_response_list_parser(paginate, it, 'instanceProfiles'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'jobs'))
    elif module.params['list_network_profiles']:
        module.exit_json(network_profiles=aws_response_list_parser(paginate, it, 'networkProfiles'))
    elif module.params['list_offering_promotions']:
        module.exit_json(offering_promotions=aws_response_list_parser(paginate, it, 'offeringPromotions'))
    elif module.params['list_offering_transactions']:
        module.exit_json(offering_transactions=aws_response_list_parser(paginate, it, 'offeringTransactions'))
    elif module.params['list_offerings']:
        module.exit_json(offerings=aws_response_list_parser(paginate, it, 'offerings'))
    elif module.params['list_remote_access_sessions']:
        module.exit_json(remote_access_sessions=aws_response_list_parser(paginate, it, 'remoteAccessSessions'))
    elif module.params['list_runs']:
        module.exit_json(runs=aws_response_list_parser(paginate, it, 'runs'))
    elif module.params['list_samples']:
        module.exit_json(samples=aws_response_list_parser(paginate, it, 'samples'))
    elif module.params['list_suites']:
        module.exit_json(suites=aws_response_list_parser(paginate, it, 'suites'))
    elif module.params['list_test_grid_projects']:
        module.exit_json(test_grid_projects=aws_response_list_parser(paginate, it, 'testGridProjects'))
    elif module.params['list_test_grid_session_actions']:
        module.exit_json(test_grid_session_actions=aws_response_list_parser(paginate, it, 'actions'))
    elif module.params['list_test_grid_session_artifacts']:
        module.exit_json(test_grid_session_artifacts=aws_response_list_parser(paginate, it, 'artifacts'))
    elif module.params['list_test_grid_sessions']:
        module.exit_json(test_grid_sessions=aws_response_list_parser(paginate, it, 'testGridSessions'))
    elif module.params['list_tests']:
        module.exit_json(tests=aws_response_list_parser(paginate, it, 'tests'))
    elif module.params['list_uploads']:
        module.exit_json(uploads=aws_response_list_parser(paginate, it, 'uploads'))
    elif module.params['list_vpce_configurations']:
        module.exit_json(vpce_configurations=aws_response_list_parser(paginate, it, 'vpceConfigurations'))
    else:
        module.exit_json(projects=aws_response_list_parser(paginate, it, 'projects'))


if __name__ == '__main__':
    main()
