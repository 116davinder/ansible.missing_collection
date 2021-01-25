#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_docdb_info
short_description: Get Information about Amazon DocumentDB.
description:
  - Get Information about Amazon DocumentDB.
  - U(https://docs.aws.amazon.com/documentdb/latest/developerguide/API_Operations.html)
version_added: 0.0.5
options:
  name:
    description:
      - name of the parameter group.
    required: false
    type: str
  snapshot_type:
    description:
      - type of snapshot.
    required: false
    type: str
    choices: ['automated', 'manual', 'shared', 'public']
    default: 'automated'
  source_type:
    description:
      - type of source.
    required: false
    type: str
    choices: ['db-instance', 'db-parameter-group', 'db-security-group', 'db-snapshot']
    default: 'db-instance'
  end_time:
    description:
      - Time to filter results? Example: I(2021-12-01)
    required: false
    type: str
  start_time:
    description:
      - Time to filter results? Example: I(2021-12-01)
    required: false
    type: str
  describe_db_cluster_parameter_groups:
    description:
      - do you want to get list of db cluster parameter groups?
    required: false
    type: bool
  describe_certificates:
    description:
      - do you want to get list of certificates?
    required: false
    type: bool
  describe_db_cluster_parameters:
    description:
      - do you want to get list of db cluster parameters for given I(name)?
    required: false
    type: bool
  describe_db_cluster_snapshots:
    description:
      - do you want to get list of db cluster snapshots for given I(snapshot_type)?
    required: false
    type: bool
  describe_db_instances:
    description:
      - do you want to get list of db instances?
    required: false
    type: bool
  describe_db_subnet_groups:
    description:
      - do you want to get list of db subnet groups?
    required: false
    type: bool
  describe_event_categories:
    description:
      - do you want to get list of event categories for given I(source_type)?
    required: false
    type: bool
  describe_events:
    description:
      - do you want to get list of events for given I(start_time) and I(end_time)?
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
- name: "get list of db clusters"
  aws_docdb_info:

- name: "get list of db cluster parameter groups."
  aws_docdb_info:
    describe_db_cluster_parameter_groups: true

- name: "get list of certificates."
  aws_docdb_info:
    describe_certificates: true

- name: "get list of db cluster parameters."
  aws_docdb_info:
    describe_db_cluster_parameters: true
    name: 'test-parameter-group-name'

- name: "get list of db snapshots"
  aws_docdb_info:
    describe_db_cluster_snapshots: true
    snapshot_type: 'automated'

- name: "get list of db instances"
  aws_docdb_info:
    describe_db_instances: true

- name: "get list of db subnet groups"
  aws_docdb_info:
    describe_db_subnet_groups: true

- name: "get list of db event categories"
  aws_docdb_info:
    describe_event_categories: true
    source_type: 'db-instance'

- name: "get list of events."
  aws_docdb_info:
    describe_events: true
    start_time: '2020-12-30'
    end_time: '2021-12-30'
"""

RETURN = """
db_cluster_parameter_groups:
  description: list of db cluster parameter groups.
  returned: when `describe_db_cluster_parameter_groups` is defined and success
  type: list
certificates:
  description: list of certificates.
  returned: when `describe_certificates` is defined and success
  type: list
parameters:
  description: list of cluster parameters.
  returned: when `describe_db_cluster_parameters` is defined and success
  type: list
snapshots:
  description: list of db cluster snapshots.
  returned: when `describe_db_cluster_snapshots` is defined and success
  type: list
instances:
  description: list of db instances.
  returned: when `describe_db_instances` is defined and success
  type: list
events:
  description: list of db cluster events.
  returned: when `describe_events` is defined and success
  type: list
db_subnet_groups:
  description: list of db subnet groups.
  returned: when `describe_db_subnet_groups` is defined and success
  type: list
event_categories:
  description: list of db event categories.
  returned: when `describe_event_categories` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from datetime import datetime


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                try:
                    _return.append(camel_dict_to_snake_dict(_app))
                except AttributeError:
                    _return.append(_app)
    else:
        for _app in iterator[resource_field]:
            try:
                _return.append(camel_dict_to_snake_dict(_app))
            except AttributeError:
                _return.append(_app)
    return _return


def convert_str_to_datetime(time: str):
    try:
        return datetime.strptime(time, '%Y-%m-%d')
    except ValueError:
        return None


def _docdb(client, module):
    try:
        if module.params['describe_db_cluster_parameter_groups']:
            if client.can_paginate('describe_db_cluster_parameter_groups'):
                paginator = client.get_paginator('describe_db_cluster_parameter_groups')
                return paginator.paginate(), True
            else:
                return client.describe_db_cluster_parameter_groups(), False
        elif module.params['describe_certificates']:
            if client.can_paginate('describe_certificates'):
                paginator = client.get_paginator('describe_certificates')
                return paginator.paginate(), True
            else:
                return client.describe_certificates(), False
        elif module.params['describe_db_cluster_parameters']:
            if client.can_paginate('describe_db_cluster_parameters'):
                paginator = client.get_paginator('describe_db_cluster_parameters')
                return paginator.paginate(
                    DBClusterParameterGroupName=module.params['name'],
                ), True
            else:
                return client.describe_db_cluster_parameters(
                    DBClusterParameterGroupName=module.params['name'],
                ), False
        elif module.params['describe_db_cluster_snapshots']:
            if client.can_paginate('describe_db_cluster_snapshots'):
                paginator = client.get_paginator('describe_db_cluster_snapshots')
                return paginator.paginate(
                    SnapshotType=module.params['snapshot_type'],
                ), True
            else:
                return client.describe_db_cluster_snapshots(
                    SnapshotType=module.params['snapshot_type'],
                ), False
        elif module.params['describe_db_instances']:
            if client.can_paginate('describe_db_instances'):
                paginator = client.get_paginator('describe_db_instances')
                return paginator.paginate(), True
            else:
                return client.describe_db_instances(), False
        elif module.params['describe_db_subnet_groups']:
            if client.can_paginate('describe_db_subnet_groups'):
                paginator = client.get_paginator('describe_db_subnet_groups')
                return paginator.paginate(), True
            else:
                return client.describe_db_subnet_groups(), False
        elif module.params['describe_event_categories']:
            if client.can_paginate('describe_event_categories'):
                paginator = client.get_paginator('describe_event_categories')
                return paginator.paginate(
                    SourceType=module.params['source_type'],
                ), True
            else:
                return client.describe_event_categories(
                    SourceType=module.params['source_type'],
                ), False
        elif module.params['describe_events']:
            _end_time = convert_str_to_datetime(module.params['end_time'])
            _start_time = convert_str_to_datetime(module.params['start_time'])
            if _start_time is None or _end_time is None:
                module.fail_json("date format is wrong, correct format: '2020-06-01'")

            if client.can_paginate('describe_events'):
                paginator = client.get_paginator('describe_events')
                return paginator.paginate(
                    EndTime=_end_time,
                    StartTime=_start_time,
                ), True
            else:
                return client.describe_events(
                    EndTime=_end_time,
                    StartTime=_start_time,
                ), False
        else:
            if client.can_paginate('describe_db_clusters'):
                paginator = client.get_paginator('describe_db_clusters')
                return paginator.paginate(), True
            else:
                return client.describe_db_clusters(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Doc DB details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['parameter_group_name']),
        snapshot_type=dict(
            required=False,
            choices=['automated', 'manual', 'shared', 'public'],
            default='automated'
        ),
        source_type=dict(
            required=False,
            choices=['db-instance', 'db-parameter-group', 'db-security-group', 'db-snapshot'],
            default='db-instance'
        ),
        start_time=dict(required=False),
        end_time=dict(required=False),
        describe_db_cluster_parameter_groups=dict(required=False, type=bool),
        describe_certificates=dict(required=False, type=bool),
        describe_db_cluster_parameters=dict(required=False, type=bool),
        describe_db_cluster_snapshots=dict(required=False, type=bool),
        describe_db_instances=dict(required=False, type=bool),
        describe_db_subnet_groups=dict(required=False, type=bool),
        describe_event_categories=dict(required=False, type=bool),
        describe_events=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_db_cluster_parameters', True, ['name']),
            ('describe_events', True, ['start_time', 'end_time']),
        ),
        mutually_exclusive=[
            (
                'describe_db_cluster_parameter_groups',
                'describe_certificates',
                'describe_db_cluster_parameters',
                'describe_db_cluster_snapshots',
                'describe_db_instances',
                'describe_db_subnet_groups',
                'describe_event_categories',
                'describe_events',
            )
        ],
    )

    client = module.client('docdb', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _docdb(client, module)

    if module.params['describe_db_cluster_parameter_groups']:
        module.exit_json(db_cluster_parameter_groups=aws_response_list_parser(paginate, it, 'DBClusterParameterGroups'))
    elif module.params['describe_certificates']:
        module.exit_json(certificates=aws_response_list_parser(paginate, it, 'Certificates'))
    elif module.params['describe_db_cluster_parameters']:
        module.exit_json(parameters=aws_response_list_parser(paginate, it, 'Parameters'))
    elif module.params['describe_db_cluster_snapshots']:
        module.exit_json(snapshots=aws_response_list_parser(paginate, it, 'DBClusterSnapshots'))
    elif module.params['describe_db_instances']:
        module.exit_json(instances=aws_response_list_parser(paginate, it, 'DBInstances'))
    elif module.params['describe_db_subnet_groups']:
        module.exit_json(db_subnet_groups=aws_response_list_parser(paginate, it, 'DBSubnetGroups'))
    elif module.params['describe_event_categories']:
        module.exit_json(event_categories=aws_response_list_parser(paginate, it, 'EventCategoriesMapList'))
    elif module.params['describe_events']:
        module.exit_json(events=aws_response_list_parser(paginate, it, 'Events'))
    else:
        module.exit_json(clusters=aws_response_list_parser(paginate, it, 'DBClusters'))


if __name__ == '__main__':
    main()
